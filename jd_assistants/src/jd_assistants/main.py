import sys
from jd_assistants.crews.lead_read_cv_crew.crew import LeadReadCVCrew

def run():
    inputs = {
        'path': '/media/baobao/DataLAP2/Projects/CrewAI_Gemini/jd_assistants/src/jd_assistants/pdfs/NguyenThiNgocHuyen.pdf'
    }
    return LeadReadCVCrew().crew().kickoff(inputs=inputs)
    
if __name__ == "__main__":
    print("## Welcome to Stock Analysis Crew")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)