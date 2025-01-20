from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class LeadSummarizationCrew:
    """Lead Summarization Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def summarization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarization_agent"],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary"],
            verbose=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Lead Summarization Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
