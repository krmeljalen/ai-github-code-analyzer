import os
import sys
import shutil

import utils.config as cfg
import utils.ollama as ollama
import utils.llama_index as llama_index
import utils.logs as logs


def rag_pipeline(session_state):
    """
    RAG pipeline for Llama-based chatbots.

    Yields:
        - str: Successive chunks of conversation from the Ollama model with context.

    Raises:
        - Exception: If there is an error retrieving answers from the Ollama model or creating the service context.

    Notes:
        This function initiates a chat with context using the Llama-Index library and the Ollama language model. The function returns an iterable yielding successive chunks of conversation from the Ollama model with context. If there is an error retrieving answers from the Ollama model or creating the service context, the function raises an exception.

    Context:
        - logs.log: A logger for logging events related to this function.

    Side Effects:
        - Creates a service context using the provided Ollama model and embedding file.
        - Loads documents from the current working directory or the provided list of files.
        - Removes the loaded documents and any temporary files created during processing.
    """
    error = None

    ######################################
    # Create Llama-Index service-context #
    # to use local LLMs and embeddings   #
    ######################################

    try:
        print(cfg.config["selected_model"])
        ollama.create_ollama_llm(
            cfg.config["selected_model"],
            cfg.config["ollama_endpoint"],
            cfg.config["system_prompt"],
        )
    except Exception as err:
        logs.log.error(f"Failed to setup LLM: {str(err)}")
        sys.exit(1)

    ####################################
    # Determine embedding model to use #
    ####################################

    embedding_model = cfg.config["embedding_model"]

    try:
        llama_index.setup_embedding_model(
            embedding_model,
        )
    except Exception as err:
        logs.log.error(f"Setting up Embedding Model failed: {str(err)}")
        sys.exit(1)

    #######################################
    # Load files from the data/ directory #
    #######################################

    # if documents already exists in state
    if session_state.documents is not None and len(session_state.documents) > 0:
        logs.log.info("Documents are already available; skipping document loading")
        logs.log.info("Processed File Data")
    else:
        try:
            save_dir = os.getcwd() + "/data"
            documents = llama_index.load_documents(save_dir)
            session_state.documents = documents
            logs.log.info("Data Processed")
        except Exception as err:
            logs.log.error(f"Document Load Error: {str(err)}")
            sys.exit(1)

    ###########################################
    # Create an index from ingested documents #
    ###########################################

    try:
        session_state.query_engine = llama_index.create_query_engine(
            session_state.documents,
        )
        logs.log.info("Created File Index")
    except Exception as err:
        logs.log.error(f"Index Creation Error: {str(err)}")
        sys.exit(1)

    #####################
    # Remove data files #
    #####################

    try:
        save_dir = os.getcwd() + "/data"
        shutil.rmtree(save_dir)
        logs.log.info("Removed Temp Files")
    except Exception as err:
        logs.log.warning(
            f"Unable to delete data files, you may want to clean-up manually: {str(err)}"
        )
        pass

    return error  # If no errors occurred, None is returned
