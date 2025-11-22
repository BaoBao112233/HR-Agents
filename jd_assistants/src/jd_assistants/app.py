import gradio as gr
import asyncio
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from jd_assistants.database import (
    init_db, async_session_maker,
    create_candidate, get_all_candidates,
    create_job_description, get_active_jd,
    save_candidate_score, get_candidate_scores
)
from jd_assistants.cache import get_redis_client, close_redis_client
from jd_assistants.inference.groq import ChatGroq
from jd_assistants.agent.read_cv import ReadCVAgent
from jd_assistants.agent.summarization import SummarizationAgent
from jd_assistants.agent.score import ScoreAgent
from jd_assistants.agent.jd_rewriter import JDRewriterAgent
from jd_assistants.tools.read_pdf_tool import ReadPDFTool
from jd_assistants.models import Candidate

# Initialize LLM
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not set")

llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)

# Initialize agents
read_cv_agent = ReadCVAgent(llm)
summarization_agent = SummarizationAgent(llm)
score_agent = ScoreAgent(llm)
jd_rewriter_agent = JDRewriterAgent(llm)
read_pdf_tool = ReadPDFTool()

# Global state
current_jd = {"description": "", "skills": "", "title": ""}

async def process_cvs(files):
    """Process uploaded CV files"""
    if not files:
        return "No files uploaded", None
    
    results = []
    async with async_session_maker() as session:
        for idx, file in enumerate(files):
            try:
                file_name = Path(file.name).stem
                pdf_content = read_pdf_tool._run(file.name)
                
                # Extract data
                extracted_data = read_cv_agent.process(pdf_content, file_name)
                
                name = extracted_data.get("personal_info", {}).get("name", "Unknown")
                email = extracted_data.get("personal_info", {}).get("email", "")
                skills_list = extracted_data.get("skills", [])
                skills = ", ".join([s.get("name", "") for s in skills_list if isinstance(s, dict)])
                
                # Summarize
                candidate_info = {
                    "name": name,
                    "education": extracted_data.get("education"),
                    "work_experience": extracted_data.get("work_experience"),
                    "skills": skills
                }
                bio = summarization_agent.process(candidate_info)
                
                # Save to database
                candidate_data = {
                    "id": str(idx),
                    "name": name,
                    "email": email,
                    "bio": bio,
                    "skills": skills
                }
                await create_candidate(session, candidate_data)
                
                results.append(f"✓ {name}")
            except Exception as e:
                results.append(f"✗ Error processing {Path(file.name).name}: {str(e)}")
    
    return "\n".join(results), await get_candidates_table()

def get_candidates_table():
    """Get candidates as DataFrame for display"""
    async def _get():
        async with async_session_maker() as session:
            candidates = await get_all_candidates(session)
            if not candidates:
                return pd.DataFrame()
            
            data = {
                "Name": [c.name for c in candidates],
                "Email": [c.email for c in candidates],
                "Skills": [c.skills[:100] + "..." if len(c.skills) > 100 else c.skills for c in candidates],
                "Date": [c.created_at.strftime("%Y-%m-%d %H:%M") for c in candidates]
            }
            return pd.DataFrame(data)
    
    return asyncio.run(_get())

async def save_jd(title, description, skills):
    """Save job description"""
    global current_jd
    async with async_session_maker() as session:
        jd_data = {
            "title": title,
            "description": description,
            "skills": skills
        }
        await create_job_description(session, jd_data)
        current_jd = jd_data
    return f"✓ Job Description '{title}' saved successfully!"

async def score_all_candidates():
    """Score all candidates against active JD"""
    async with async_session_maker() as session:
        # Get active JD
        jd = await get_active_jd(session)
        if not jd:
            return "No active job description found. Please create one first.", None
        
        # Get all candidates
        candidates = await get_all_candidates(session)
        if not candidates:
            return "No candidates found. Please upload CVs first.", None
        
        results = []
        for candidate in candidates:
            cand_obj = Candidate(
                id=candidate.candidate_id,
                name=candidate.name,
                email=candidate.email,
                bio=candidate.bio,
                skills=candidate.skills
            )
            
            score_data = score_agent.process(cand_obj, jd.description, jd.skills)
            
            if isinstance(score_data, dict):
                await save_candidate_score(session, score_data, jd.id)
                results.append(f"{candidate.name}: {score_data.get('score', 0)}/100")
        
        return "✓ Scoring completed!\n" + "\n".join(results), await get_scores_table()

def get_scores_table():
    """Get scores as DataFrame"""
    async def _get():
        async with async_session_maker() as session:
            scores = await get_candidate_scores(session)
            if not scores:
                return pd.DataFrame()
            
            data = {
                "Name": [s.name for s in scores],
                "Score": [s.score for s in scores],
                "Reason": [s.reason[:200] + "..." if len(s.reason) > 200 else s.reason for s in scores],
                "Date": [s.created_at.strftime("%Y-%m-%d %H:%M") for s in scores]
            }
            return pd.DataFrame(data)
    
    return asyncio.run(_get())

def analyze_jd_text(jd_text):
    """Analyze JD and provide suggestions"""
    if not jd_text:
        return "Please enter a job description to analyze."
    
    analysis = jd_rewriter_agent.analyze_jd(jd_text)
    
    if isinstance(analysis, dict):
        improvements = analysis.get("improvements", [])
        score = analysis.get("overall_score", 0)
        recommendations = analysis.get("key_recommendations", [])
        
        output = f"## Analysis Results\n\n**Overall Score:** {score}/100\n\n"
        output += "### Key Recommendations:\n"
        for rec in recommendations:
            output += f"- {rec}\n"
        output += "\n### Detailed Improvements:\n"
        for imp in improvements[:5]:  # Show top 5
            output += f"\n**{imp.get('section', 'Section')}**\n"
            output += f"- **Original:** {imp.get('original', '')[:100]}...\n"
            output += f"- **Improved:** {imp.get('improved', '')[:100]}...\n"
            output += f"- **Reason:** {imp.get('reason', '')}\n"
        
        return output
    
    return str(analysis)

def rewrite_full_jd(jd_text):
    """Rewrite the complete JD"""
    if not jd_text:
        return "Please enter a job description to rewrite."
    
    rewritten = jd_rewriter_agent.rewrite_jd(jd_text)
    return rewritten

def create_analytics():
    """Create analytics visualizations"""
    async def _create():
        async with async_session_maker() as session:
            candidates = await get_all_candidates(session)
            scores = await get_candidate_scores(session)
            
            if not candidates:
                return None, None, "No data available"
            
            # Score distribution
            if scores:
                score_values = [s.score for s in scores]
                fig1 = px.histogram(x=score_values, nbins=20, title="Score Distribution",
                                   labels={"x": "Score", "y": "Count"})
            else:
                fig1 = None
            
            # Candidates over time
            dates = [c.created_at.date() for c in candidates]
            date_counts = pd.Series(dates).value_counts().sort_index()
            fig2 = px.line(x=date_counts.index, y=date_counts.values,
                          title="Candidates Over Time",
                          labels={"x": "Date", "y": "Number of Candidates"})
            
            # Summary stats
            total = len(candidates)
            avg_score = sum(score_values) / len(score_values) if scores else 0
            stats = f"""
            **Total Candidates:** {total}
            **Average Score:** {avg_score:.1f}/100
            **Scored Candidates:** {len(scores)}
            """
            
            return fig1, fig2, stats
    
    return asyncio.run(_create())

# Initialize database on startup
asyncio.run(init_db())

# Create Gradio Interface
with gr.Blocks(title="HR Recruitment Assistant") as app:
    gr.Markdown("# 🎯 HR Recruitment Assistant")
    gr.Markdown("Upload CVs, manage job descriptions, and analyze candidates with AI")
    
    with gr.Tabs():
        # Tab 1: Upload CVs
        with gr.Tab("📄 Upload CVs"):
            gr.Markdown("### Upload Candidate CVs")
            cv_files = gr.File(label="Select PDF files", file_count="multiple", file_types=[".pdf"])
            process_btn = gr.Button("Process CVs", variant="primary")
            process_output = gr.Textbox(label="Results", lines=10)
            candidates_preview = gr.Dataframe(label="Uploaded Candidates", interactive=False)
            
            process_btn.click(
                fn=lambda files: asyncio.run(process_cvs(files)),
                inputs=[cv_files],
                outputs=[process_output, candidates_preview]
            )
        
        # Tab 2: Manage JD
        with gr.Tab("📋 Job Description"):
            gr.Markdown("### Create/Update Job Description")
            jd_title = gr.Textbox(label="Job Title", placeholder="e.g., Senior Backend Developer")
            jd_description = gr.Textbox(label="Job Description", lines=10, placeholder="Enter full job description...")
            jd_skills = gr.Textbox(label="Required Skills (comma-separated)", placeholder="Python, FastAPI, PostgreSQL, Docker...")
            save_jd_btn = gr.Button("Save Job Description", variant="primary")
            jd_output = gr.Textbox(label="Status")
            
            save_jd_btn.click(
                fn=lambda t, d, s: asyncio.run(save_jd(t, d, s)),
                inputs=[jd_title, jd_description, jd_skills],
                outputs=[jd_output]
            )
        
        # Tab 3: Dashboard
        with gr.Tab("👥 Candidates Dashboard"):
            gr.Markdown("### All Candidates")
            refresh_btn = gr.Button("🔄 Refresh", size="sm")
            candidates_table = gr.Dataframe(label="Candidates", interactive=False)
            
            gr.Markdown("### Scoring")
            score_btn = gr.Button("Score All Candidates", variant="primary")
            score_output = gr.Textbox(label="Scoring Results", lines=10)
            scores_table = gr.Dataframe(label="Scores", interactive=False)
            
            refresh_btn.click(fn=get_candidates_table, outputs=[candidates_table])
            score_btn.click(
                fn=lambda: asyncio.run(score_all_candidates()),
                outputs=[score_output, scores_table]
            )
        
        # Tab 4: Analytics
        with gr.Tab("📊 Analytics"):
            gr.Markdown("### Recruitment Analytics")
            analytics_btn = gr.Button("Generate Analytics", variant="primary")
            stats_md = gr.Markdown()
            with gr.Row():
                score_dist = gr.Plot(label="Score Distribution")
                timeline = gr.Plot(label="Candidates Timeline")
            
            analytics_btn.click(
                fn=create_analytics,
                outputs=[score_dist, timeline, stats_md]
            )
        
        # Tab 5: JD Rewriting
        with gr.Tab("✍️ JD Rewriting"):
            gr.Markdown("### AI-Powered JD Improvement")
            with gr.Row():
                with gr.Column():
                    input_jd = gr.Textbox(label="Original JD", lines=15, placeholder="Paste your job description here...")
                    analyze_btn = gr.Button("Analyze & Suggest Improvements", variant="primary")
                    rewrite_btn = gr.Button("Rewrite Complete JD", variant="secondary")
                
                with gr.Column():
                    analysis_output = gr.Markdown(label="Analysis")
                    rewritten_output = gr.Textbox(label="Rewritten JD", lines=15)
            
            analyze_btn.click(fn=analyze_jd_text, inputs=[input_jd], outputs=[analysis_output])
            rewrite_btn.click(fn=rewrite_full_jd, inputs=[input_jd], outputs=[rewritten_output])


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
