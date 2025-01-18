from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from jd_assistants.types import CandidateProfile
from jd_assistants.tools.read_pdf_tool import ReadPDFTool


@CrewBase
class LeadReadCVCrew:
    """
    Lead Read CV Crew:
    - Using PyMuPDF and pdfplumber to read CV
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def hr_evaluation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_extraction_agent"],
            verbose=True,
            tools=[
                ReadPDFTool()
            ]
        )

    @task
    def evaluate_candidate_task(self) -> Task:
        return Task(
            config=self.tasks_config["extract_candidate"],
            output_pydantic=CandidateProfile,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Lead Read CV Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
