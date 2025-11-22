import os
from typing import List, TypedDict, Annotated
import operator
from pathlib import Path
from datetime import datetime
import pandas as pd
import asyncio
import re

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END, START

from jd_assistants.inference.groq import ChatGroq
from jd_assistants.agent.read_cv import ReadCVAgent
from jd_assistants.agent.summarization import SummarizationAgent
from jd_assistants.agent.score import ScoreAgent
from jd_assistants.agent.response import ResponseAgent
from jd_assistants.tools.read_pdf_tool import ReadPDFTool
from jd_assistants.models import Candidate, CandidateScore, ScoredCandidate
from jd_assistants.jd import jd_junior_react_dev
from jd_assistants.tools.candidateUtils import combine_candidates_with_scores


from dotenv import load_dotenv

load_dotenv()

# Constants
JOB_DESCRIPTION = jd_junior_react_dev.JOB_DESCRIPTION
SKILLS = jd_junior_react_dev.SKILLS

# State Definition
class AgentState(TypedDict):
    candidates: List[Candidate]
    candidate_scores: List[CandidateScore]
    hydrated_candidates: List[ScoredCandidate]
    scored_leads_feedback: str
    pdf_paths: List[str]
    current_pdf_index: int

# Helper Functions
def get_pdf_paths(folder_path):
    pdf_paths = list(Path(folder_path).glob("*.pdf"))
    return [str(pdf_path) for pdf_path in pdf_paths]

# Nodes
def load_leads(state: AgentState):
    print("Loading leads...")
    pdf_folders = '/media/baobao/DataLAP2/Projects/CrewAI_Gemini/jd_assistants/src/jd_assistants/pdfs/'
    # Fallback to local pdfs folder if absolute path doesn't exist (for portability)
    if not os.path.exists(pdf_folders):
        pdf_folders = os.path.join(os.path.dirname(__file__), 'pdfs')
    
    pdf_paths = get_pdf_paths(pdf_folders)
    return {"pdf_paths": pdf_paths, "candidates": [], "current_pdf_index": 0}

def process_cvs(state: AgentState):
    print("Processing CVs...")
    api_key = os.environ.get("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    read_cv_agent = ReadCVAgent(llm)
    summarization_agent = SummarizationAgent(llm)
    read_pdf_tool = ReadPDFTool()

    candidates = []
    for i, pdf_path in enumerate(state['pdf_paths']):
        print(f"Processing {pdf_path}...")
        file_name = pdf_path.split("/")[-1].split(".")[0]
        pdf_content = read_pdf_tool._run(pdf_path)
        
        # Extract Info
        extracted_data = read_cv_agent.process(pdf_content, file_name)
        print(f"Extracted Data for {file_name}: {extracted_data}")
        
        name = extracted_data.get("personal_info", {}).get("name", "Unknown")
        email = extracted_data.get("personal_info", {}).get("email", "")
        skills_list = extracted_data.get("skills", [])
        skills = ", ".join([s.get("name") for s in skills_list]) if isinstance(skills_list, list) else str(skills_list)
        
        # Summarize
        candidate_info = {
            "name": name,
            "education": extracted_data.get("education"),
            "work_experience": extracted_data.get("work_experience"),
            "skills": skills
        }
        bio = summarization_agent.process(candidate_info)
        
        candidate = Candidate(
            id=str(i),
            name=name,
            email=email,
            bio=bio,
            skills=skills
        )
        candidates.append(candidate)
        print(f"Processed {name}")

    return {"candidates": candidates}

def score_leads(state: AgentState):
    print("Scoring leads...")
    api_key = os.environ.get("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    score_agent = ScoreAgent(llm)
    
    candidate_scores = []
    for candidate in state['candidates']:
        print(f"Scoring {candidate.name}...")
        score_data = score_agent.process(
            candidate, 
            JOB_DESCRIPTION, 
            SKILLS, 
            state.get('scored_leads_feedback', "")
        )
        # Ensure score_data fits CandidateScore model
        if isinstance(score_data, dict):
            # Map fields if necessary or instantiate directly
            try:
                score_obj = CandidateScore(
                    id=candidate.id,
                    name=candidate.name,
                    score=int(score_data.get('score', 0)),
                    reason=score_data.get('reason', '')
                )
                candidate_scores.append(score_obj)
            except Exception as e:
                print(f"Error creating score object for {candidate.name}: {e}")
        else:
            print(f"Invalid score data for {candidate.name}: {score_data}")

    # Save to CSV
    output_file = Path(__file__).parent / "results.csv"
    sorted_scores = sorted(candidate_scores, key=lambda cs: cs.score, reverse=True)
    data = {
        "Name": [score.name for score in sorted_scores],
        "Score": [score.score for score in sorted_scores],
        "Reason": [score.reason for score in sorted_scores],
    }
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

    return {"candidate_scores": candidate_scores}

def human_review(state: AgentState):
    print("Human Review...")
    hydrated_candidates = combine_candidates_with_scores(
        state['candidates'], state['candidate_scores']
    )
    sorted_candidates = sorted(hydrated_candidates, key=lambda c: c.score, reverse=True)
    top_candidates = sorted_candidates[:3]
    
    print("Here are the top 3 candidates:")
    for candidate in top_candidates:
        print(f"Name: {candidate.name}, Score: {candidate.score}, Reason: {candidate.reason}")

    print("\nPlease choose an option:")
    print("1. Quit")
    print("2. Redo lead scoring with additional feedback")
    print("3. Proceed with writing emails to all leads")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        return {"action": "quit"}
    elif choice == "2":
        feedback = input("\nPlease provide additional feedback:\n")
        return {"scored_leads_feedback": feedback, "action": "redo"}
    elif choice == "3":
        return {"hydrated_candidates": sorted_candidates, "action": "email"}
    else:
        return {"action": "retry"} # Simple retry loop

def generate_emails(state: AgentState):
    print("Generating Emails...")
    api_key = os.environ.get("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    response_agent = ResponseAgent(llm)
    
    top_candidate_ids = {c.id for c in state['hydrated_candidates'][:3]}
    output_dir = Path(__file__).parent / "email_responses"
    output_dir.mkdir(parents=True, exist_ok=True)

    for candidate in state['hydrated_candidates']:
        proceed = candidate.id in top_candidate_ids
        email_content = response_agent.process(candidate, proceed)
        
        safe_name = re.sub(r"[^a-zA-Z0-9_\- ]", "", candidate.name)
        filename = f"{safe_name}.txt"
        file_path = output_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(email_content)
        print(f"Email saved for {candidate.name}")
        
    return {}

# Router
def route_human_review(state: AgentState):
    action = state.get("action")
    if action == "quit":
        return END
    elif action == "redo":
        return "score_leads"
    elif action == "email":
        return "generate_emails"
    else:
        return "human_review"

# Graph Construction
def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("load_leads", load_leads)
    workflow.add_node("process_cvs", process_cvs)
    workflow.add_node("score_leads", score_leads)
    workflow.add_node("human_review", human_review)
    workflow.add_node("generate_emails", generate_emails)
    
    workflow.add_edge(START, "load_leads")
    workflow.add_edge("load_leads", "process_cvs")
    workflow.add_edge("process_cvs", "score_leads")
    workflow.add_edge("score_leads", "human_review")
    
    workflow.add_conditional_edges(
        "human_review",
        route_human_review,
        {
            END: END,
            "score_leads": "score_leads",
            "generate_emails": "generate_emails",
            "human_review": "human_review"
        }
    )
    
    workflow.add_edge("generate_emails", END)
    
    return workflow.compile()

def run():
    graph = create_graph()
    initial_state = {
        "candidates": [],
        "candidate_scores": [],
        "hydrated_candidates": [],
        "scored_leads_feedback": "",
        "pdf_paths": [],
        "current_pdf_index": 0
    }
    graph.invoke(initial_state)

if __name__ == "__main__":
    run()