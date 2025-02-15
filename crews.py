from crewai import Crew, Process
from agents.agent import *
from agents.task import *


from typing import Dict, Any

class CrewDefinition:
    def __init__(self, crew, required_inputs, optional_inputs=None):
        self.crew = crew
        self.required_inputs = required_inputs  # Define the expected inputs
        self.optional_inputs = optional_inputs or {}  # Define the optional inputs

# Define available crews and their required inputs
crews = {
    "financial report agent": CrewDefinition(
        Crew(
            agents=[financial_report_agent],
            tasks=[financial_report_task],
            process=Process.sequential,
        ),
        required_inputs={"symbol": str},
        optional_inputs={"query": str},
        
    ),

    "investment advisor agent": CrewDefinition(
        Crew(
            agents=[investment_advisor_agent],
            tasks=[investment_advisor_task],
            process=Process.sequential,
        ),
        required_inputs={"symbol": str},
        optional_inputs={"query": str},
    ),
    "financial query answer agent": CrewDefinition(
        Crew(
            agents=[query_answerer_agent_financial],
            tasks=[query_answerer_task_financial],
            process=Process.sequential,
        ),
        required_inputs={"symbol": str, "query": str},
    ),

    "news researcher": CrewDefinition(
        Crew(
            agents=[news_researcher],
            tasks=[research_task],
            process=Process.sequential,
        ),
        required_inputs={"topic": str},
    ),

    "new reporting analyst": CrewDefinition(
        Crew(
            agents=[reporting_analyst],
            tasks=[reporting_task],
            process=Process.sequential,
        ),
        required_inputs={"topic": str},
    ),


    # "crew5": CrewDefinition(
    #     Crew(
    #         agents=[stock_market_agent],
    #         tasks=[stock_market_task],
    #         process=Process.sequential,
    #     ),
    #     required_inputs={"symbol": str, "function": str},
    #     optional_inputs={"query": str},
    # ),

    
    "medical agent": CrewDefinition(
        Crew(
            agents=[medical_agent],
            tasks=[medical_task],
            process=Process.sequential,
        ),
        required_inputs={"term": str},
        optional_inputs={"retmax" : str , "query": str},
    ),

    "medical query answerer agent" : CrewDefinition(
        Crew(
            agents=[medical_query_response_agent],
            tasks=[medical_query_answerer_task],
            process = Process.sequential,

        ),
        required_inputs={"term": str, "query": str},
        optional_inputs={"retmax" : str}
    ),
    
}