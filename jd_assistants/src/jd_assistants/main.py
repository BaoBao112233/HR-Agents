#!/usr/bin/env python
import sys
import warnings
import pandas as pd
from typing import List
import asyncio
import time
from pathlib import Path

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel
from jd_assistants.jd import jd_junior_react_dev
from jd_assistants.crews.lead_score_crew.crew import LeadScoreCrew
from jd_assistants.crews.lead_response_crew.crew import LeadResponseCrew
from jd_assistants.types import Candidate, CandidateScore, ScoredCandidate
from jd_assistants.tools.candidateUtils import combine_candidates_with_scores

# Chỗ này có thể thay đổi tuỳ thuộc vào vị trí công việc mà công ty muốn ứng tuyển.
# Ví dụ tôi muốn ứng tuyển vị trí Junior React Dev cho công ty.
JOB_DESCRIPTION = jd_junior_react_dev.JOB_DESCRIPTION
SKILLS = jd_junior_react_dev.SKILLS

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


class LeadScoreState(BaseModel):
    candidates: List[Candidate] = []
    candidate_score: List[CandidateScore] = []
    hydrated_candidates: List[ScoredCandidate] = []
    scored_leads_feedback: str = ""
 
class LeadScoreFlow(Flow[LeadScoreState]):
    initial_state = LeadScoreState

    @start()
    def load_leads(self):
        import csv

        # Get the path to leads.csv in the same directory
        current_dir = Path(__file__).parent
        csv_file = current_dir / "leads_1.csv"

        candidates = []
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                candidate = Candidate(**row)
                candidates.append(candidate)

        # Update the state with the loaded candidates
        self.state.candidates = candidates

    @listen(or_(load_leads, "scored_leads_feedback"))
    def score_leads(self):
        print("Scoring leads")
        tasks = []

        def score_single_candidate(candidate: Candidate):
            result = (
                LeadScoreCrew()
                .crew()
                .kickoff(
                    inputs={
                        "candidate_id": candidate.id,
                        "name": candidate.name,
                        "bio": candidate.bio,
                        "job_description": JOB_DESCRIPTION,
                        "skills": SKILLS,
                        "additional_instructions": self.state.scored_leads_feedback,
                    }
                )
            )

            self.state.candidate_score.append(result.pydantic)

        for candidate in self.state.candidates:
            print("Scoring candidate:", candidate.name)
            score_single_candidate(candidate)
            # Thêm thời gian chờ giữa các lần chạy
            time.sleep(3)

        print("Finished scoring leads: ", len(self.state.candidate_score))
        
        # Save results to CSV
        self.save_results_to_csv()

    @router(score_leads)
    def human_in_the_loop(self):
        print("Finding the top 3 candidates for human to review")

        # Combine candidates with their scores using the helper function
        self.state.hydrated_candidates = combine_candidates_with_scores(
            self.state.candidates, self.state.candidate_score
        )

        # Sort the scored candidates by their score in descending order
        sorted_candidates = sorted(
            self.state.hydrated_candidates, key=lambda c: c.score, reverse=True
        )
        self.state.hydrated_candidates = sorted_candidates

        # Select the top 3 candidates
        top_candidates = sorted_candidates[:3]

        print("Here are the top 3 candidates:")
        for candidate in top_candidates:
            print(
                f"ID: {candidate.id}, Name: {candidate.name}, Score: {candidate.score}, Reason: {candidate.reason}"
            )

        # Present options to the user
        print("\nPlease choose an option:")
        print("1. Quit")
        print("2. Redo lead scoring with additional feedback")
        print("3. Proceed with writing emails to all leads")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            print("Exiting the program.")
            exit()
        elif choice == "2":
            feedback = input(
                "\nPlease provide additional feedback on what you're looking for in candidates:\n"
            )
            self.state.scored_leads_feedback = feedback
            print("\nRe-running lead scoring with your feedback...")
            return "scored_leads_feedback"
        elif choice == "3":
            print("\nProceeding to write emails to all leads.")
            return "generate_emails"
        else:
            print("\nInvalid choice. Please try again.")
            return "human_in_the_loop"

    @listen("generate_emails")
    def write_and_save_emails(self):
        import re
        from pathlib import Path

        print("Writing and saving emails for all leads.")

        # Determine the top 3 candidates to proceed with
        top_candidate_ids = {
            candidate.id for candidate in self.state.hydrated_candidates[:3]
        }

        tasks = []

        # Create the directory 'email_responses' if it doesn't exist
        output_dir = Path(__file__).parent / "email_responses"
        print("output_dir:", output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        def write_email(candidate):
            # Check if the candidate is among the top 3
            proceed_with_candidate = candidate.id in top_candidate_ids

            # Kick off the LeadResponseCrew for each candidate
            result = (
                LeadResponseCrew()
                .crew()
                .kickoff(
                    inputs={
                        "candidate_id": candidate.id,
                        "name": candidate.name,
                        "bio": candidate.bio,
                        "proceed_with_candidate": proceed_with_candidate,
                    }
                )
            )

            # Sanitize the candidate's name to create a valid filename
            safe_name = re.sub(r"[^a-zA-Z0-9_\- ]", "", candidate.name)
            filename = f"{safe_name}.txt"
            print("Filename:", filename)

            # Write the email content to a text file
            file_path = output_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result.raw)

            # Return a message indicating the email was saved
            return f"Email saved for {candidate.name} as {filename}"

        # Create tasks for all candidates
        for candidate in self.state.hydrated_candidates:
            write_email(candidate)
            time.sleep(3)

        # Run all email-writing tasks concurrently and collect results
        email_results = asyncio.gather(*tasks)

        # After all emails have been generated and saved
        print("\nAll emails have been written and saved to 'email_responses' folder.")
        for message in email_results:
            print(message)

    def save_results_to_csv(self):
        output_file = Path(__file__).parent / "results.csv"
        
        # Sort candidate scores in descending order
        sorted_scores = sorted(self.state.candidate_score, key=lambda cs: cs.score, reverse=True)

        # Create a DataFrame from the sorted scores
        data = {
            "Candidate ID": [score.id for score in sorted_scores],
            "Name": [score.name for score in sorted_scores],
            "Score": [score.score for score in sorted_scores],
            "Reason": [score.reason for score in sorted_scores],
        }
        df = pd.DataFrame(data)

        # Write the DataFrame to a CSV file
        df.to_csv(output_file, index=False)

        print(f"Results saved to {output_file}")
   
def run():
    lead_score_flow = LeadScoreFlow()
    lead_score_flow.kickoff()