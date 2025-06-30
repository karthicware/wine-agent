import pymysql
import json
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
from google.adk.tools.tool_context import ToolContext
from logging_utils import logger

def execute_db_query(query: str) -> str:
    """
    Executes a SQL query against the database and returns the result.
    Args:
        query: The SQL query to execute.
    Returns:
        A JSON string representing the query result or an error message.
    """
    logger.info(f"Executing query: {query}")
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        connection.close()
        logger.info(f"Query result: {result}")
        return json.dumps(result, indent=4, default=str)
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return json.dumps({"error": str(e)})

def exit_loop(tool_context: ToolContext, final_answer: str) -> dict:
  """
  Call this function ONLY when a final answer has been formulated.
  This signals that the iterative investigation process should end.
  """
  logger.info(f"exit_loop triggered by {tool_context.agent_name} with final answer.")
  tool_context.actions.escalate = True
  tool_context.state["final_answer"] = final_answer
  return {"status": "Loop terminated", "final_answer": final_answer} 