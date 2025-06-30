import asyncio
from google.adk.runners import InMemoryRunner
from agent import wine_support_agent
from wine_schema import SCHEMA
from logging_utils import logger
from agent import (
    STATE_USER_QUESTION,
    STATE_DB_SCHEMA,
    STATE_INVESTIGATION_HISTORY,
    STATE_FINAL_ANSWER,
    STATE_SESSION_INFO
)
from google.genai.types import Content, Part

async def main():
    while True:
        user_question = input("Enter your wine question (or type 'exit' to quit): ")
        if user_question.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        initial_state = {
            STATE_USER_QUESTION: user_question,
            STATE_DB_SCHEMA: SCHEMA,
            STATE_INVESTIGATION_HISTORY: [],
            STATE_SESSION_INFO: {
                "user_name": "Natarajan",
                "accessible_stations": "DXB, MAA"
            }
        }

        logger.info(f"Starting agent with question: '{user_question}'")
        logger.info(f"Session info: {initial_state[STATE_SESSION_INFO]}")

        runner = InMemoryRunner(agent=wine_support_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="Natarajan",
            state=initial_state
        )
        new_message = Content(role="user", parts=[Part(text=user_question)])
        final_state = None
        for event in runner.run(
            user_id="Natarajan",
            session_id=session.id,
            new_message=new_message
        ):
            if hasattr(event, "state"):
                final_state = event.state

        final_answer = final_state.get(STATE_FINAL_ANSWER, "Sorry, I could not find an answer.")
        logger.info("Agent run finished.")
        print("\n" + "="*50)
        print("Final Answer:")
        print(final_answer)
        print("="*50 + "\n")

if __name__ == '__main__':
    # Before running, ensure you have:
    # 1. Created a .env file from env_template.txt and filled in your credentials.
    # 2. Installed all packages from requirements.txt (pip install -r requirements.txt).
    # 3. A running MariaDB instance with the described schema and data.
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}") 