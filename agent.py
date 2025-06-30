import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
import config
from tools import execute_db_query, exit_loop
from wine_schema import SCHEMA

# --- State Keys ---
STATE_USER_QUESTION = "user_question"
STATE_DB_SCHEMA = "db_schema"
STATE_CURRENT_QUERY = "current_query"
STATE_QUERY_RESULT = "query_result"
STATE_INVESTIGATION_HISTORY = "investigation_history"
STATE_FINAL_ANSWER = "final_answer"
STATE_SESSION_INFO = "session_info"

# --- LLM Setup ---
LITE_LLM = LiteLlm(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_base=os.environ["AZURE_OPENAI_ENDPOINT"],
    deployment_id=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-05-15"),
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"]
)

# --- Agent Definitions ---

# STEP 1: Initial SQL Query Generator
sql_generator_agent = LlmAgent(
    name="SQLGeneratorAgent",
    model=LITE_LLM,
    instruction=f"""
    You are an expert SQL writer. Your task is to generate a single, read-only SQL query based on the user's question and the provided database schema.
    Adhere to the following rules precisely:
    - **Session Information**: The user is {{session_info.user_name}} and their accessible stations are {{session_info.accessible_stations}}. Use this information to filter queries where applicable (e.g., on CMST_WN_DEP_STN).
    - **Schema**:
    ```sql
    {{db_schema}}
    ```
    - **User Question**: "{{user_question}}"

    Generate only the SQL query. Do not add any explanations, introductions, or markdown formatting.
    """,
    output_key=STATE_CURRENT_QUERY,
    description="Generates the initial SQL query from the user's question."
)

# STEP 2a: Query Executor and Analyzer (inside the loop)
query_and_analyze_agent = LlmAgent(
    name="QueryAndAnalyzeAgent",
    model=LITE_LLM,
    instruction="""
    You are a data analyst. Your job is to execute a SQL query and analyze its result.
    - **Current Query**: `{{current_query}}`

    1. First, execute the query by calling the `execute_db_query` tool.
    2. Analyze the result from the tool.
       - If the result contains an 'error' key, call the `exit_loop` tool with an error message and stop the investigation.
       - If the result contains data, formulate a clear, user-friendly answer based on the data. Then, you MUST call the `exit_loop` tool with this final answer.
       - If the result is empty, do not call the exit tool. Simply output the raw result from the `execute_db_query` tool.
    """,
    tools=[execute_db_query, exit_loop],
    output_key=STATE_QUERY_RESULT,
    description="Executes the current SQL query and analyzes the result, exiting if data is found or if a DB error occurs."
)

# STEP 2b: Investigator Agent (inside the loop)
investigator_agent = LlmAgent(
    name="InvestigatorAgent",
    model=LITE_LLM,
    instruction=f"""
    You are an expert database investigator. Your goal is to figure out why a query returned no results and formulate a new query to dig deeper.

    - **User Question**: "{{user_question}}"
    - **Investigation History**: {{investigation_history}}
    - **Schema**:
    ```sql
    {{db_schema}}
    ```

    The last query in the investigation history failed to return any data. Based on this history and the schema, formulate a NEW SQL query to investigate the reason.
    For example, you could check for the existence of a specific wine, its status, or its schedule.

    Output *only* the new SQL query to try. Do not add any other text or explanations.
    """,
    output_key=STATE_CURRENT_QUERY,
    description="Generates a new, investigative SQL query when the previous one returned no data."
)

# STEP 2: Refinement Loop Agent
investigation_loop = LoopAgent(
    name="InvestigationLoop",
    sub_agents=[
        query_and_analyze_agent,
        investigator_agent,
    ],
    max_iterations=10
)

# STEP 3: Overall Sequential Pipeline
wine_support_agent = SequentialAgent(
    name="WineSupportAgent",
    sub_agents=[
        sql_generator_agent,
        investigation_loop
    ],
    description="Handles wine-related support questions by generating and iteratively investigating SQL queries."
) 