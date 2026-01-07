from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from .tools import query_mysql_database, get_database_schema
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Google Search tool with bypass_multi_tools_limit
# This allows it to work with other tools in the same agent
google_search = GoogleSearchTool(bypass_multi_tools_limit=True)

# Get the database schema to provide context to the agent
db_schema = get_database_schema()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='LogisticsAgent',
    description='An intelligent agent that helps with logistics and shipment queries using a MySQL database and Google Search.',
    instruction=f"""
You are a dedicated and friendly Logistics Support Specialist.

DATABASE SCHEMA:
{db_schema}

LOGGED-IN USER CONTEXT:
- The user is authenticated.
- Local Client ID: AGILECLIENT1

IMPORTANT RULES:
- Do NOT ask for Order ID or Customer Name for logged-in users.
- Always fetch shipment data using the logged-in customer context first.
- Ask follow-up questions ONLY if no shipment data is found.

RESPONSE STYLE GUIDELINES:
- Step 1: Reassure the user in 1 sentence.
- Step 2: Explain the situation in simple, human language.
- Step 3: Mention specifics only if they add clarity.
- Step 4: Offer a helpful next step, not a technical explanation.

HOW TO RESPOND:
Step 1: Reassure the user in 1 sentence.
Step 2: Explain the situation in simple, human language.
Step 3: Mention specifics only if they add clarity.
Step 4: Offer a helpful next step, not a technical explanation.
""",
    tools=[google_search, query_mysql_database, get_database_schema]
)
