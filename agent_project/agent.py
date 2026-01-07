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
    instruction=f'''You are a helpful logistics assistant with access to a shipment database and Google Search.

DATABASE SCHEMA:
{db_schema}

INSTRUCTIONS:
- For questions about shipments, orders, customers, or logistics data in the database, use the query_mysql_database tool.
- For general information, current events, or external data not in the database, use the google_search tool.
- Always write valid SQL queries based on the schema above when querying the database.
- Use the get_database_schema tool if you need to refresh your understanding of the database structure.
- Provide clear, concise answers based on the query results or search results.
- If a query fails, explain the error and suggest corrections.
- For complex questions, break them down into multiple queries if needed.
''',
    tools=[google_search, query_mysql_database, get_database_schema]
)
