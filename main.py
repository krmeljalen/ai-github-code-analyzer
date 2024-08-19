import sys
import utils.helpers as helpers
import utils.rag_pipeline as rag
import utils.ollama as ollama
import utils.logs as logs
from utils.session_state import SessionState

"""
from utils.ollama import chat, context_chat


def chatbox():
    if prompt := st.chat_input("How can I help?"):
        # Prevent submission if Ollama endpoint is not set
        if not st.session_state["query_engine"]:
            st.warning("Please confirm settings and upload files before proceeding.")
            st.stop()

        # Add the user input to messages state
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate llama-index stream with user input
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = st.write_stream(
                    context_chat(
                        prompt=prompt, query_engine=st.session_state["query_engine"]
                    )
                )

        # Add the final response to messages state
        st.session_state["messages"].append({"role": "assistant", "content": response})
"""
def chat_loop(session_state):
    while True:
        user_input = input("Question: ")
        if user_input.strip().upper() == "EOF":
            print("Ending chat...")
            break

        ollama.context_chat(
            prompt=user_input, query_engine=session_state.query_engine
        )

def run(repo="krmeljalen/kdeploy"):
    session_state = SessionState()

    helpers.clone_github_repo(repo)

    error = rag.rag_pipeline(session_state)
    if error is not None:
        logs.log.error(f"{error}")
        sys.exit(1)
    else:
        logs.log.info("AI is ready! Proceed with asking questions. Type 'EOF' to end conversation.")

    chat_loop(session_state)

if __name__ == "__main__":
    run()
