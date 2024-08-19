import sys
import utils.helpers as helpers
import utils.rag_pipeline as rag
import utils.ollama as ollama
import utils.logs as logs
from utils.session_state import SessionState


def chat_loop(session_state):
    if not session_state.query_engine:
        logs.log.error(f"Query engine not set.")
        sys.exit(1)

    while True:
        user_input = input("Question: ")
        if user_input.strip().upper() == "EOF":
            logs.log.info("Ending chat...")
            break
        ollama.context_chat(prompt=user_input, query_engine=session_state.query_engine)
        print()

def run(repo="krmeljalen/kdeploy"):
    session_state = SessionState()

    helpers.clone_github_repo(repo)

    error = rag.rag_pipeline(session_state)
    if error is not None:
        logs.log.error(f"{error}")
        sys.exit(1)
    else:
        logs.log.info(
            "AI is ready! Proceed with asking questions. Type 'EOF' to end conversation."
        )

    chat_loop(session_state)


if __name__ == "__main__":
    run()
