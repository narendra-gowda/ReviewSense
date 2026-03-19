from langchain.agents import Tool
from langchain.tools import tool
from vectorstore.query_engine import app_store_retriever, play_store_retriever, in_store_retriever


@tool
def general_chat_tool():
    """Handles general chat"""
    return True

tools = [
    Tool(
        name="App Store retriever",
        func=app_store_retriever,
        description="Use this to search App Store reviews"
                     "Input should be in dict with keys:"
                     "'query' should be the question what user asks."
                     "Add 'app_name' filter only if the user query has an app name."
                     "Add 'app_version' filter only if the user query mentions an app version."
                     "Add 'rating' filter only if the user query for details about the app rating."
                     "Add 'timeframe' filter only if the user query has time expression and convert them into these formats only (e.g. '3 months ago', 'april 2025', 'a year ago')."
                     "Add 'is_competitor' filter only if the user query asks for the competitor data.",
        return_direct=True
    ),
    Tool(
        name="Play Store retriever",
        func=play_store_retriever,
        description="Use this to search Play Store reviews"
                     "Input should be in dict with keys:"
                     "'query' should be the question what user asks."
                     "Add 'app_name' filter only if the user query has an app name."
                     "Add 'app_version' filter only if the user query mentions an app version."
                     "Add 'rating' filter only if the user query for details about the app rating."
                     "Add 'timeframe' filter only if the user query has time expression and convert them into these formats only (e.g. '3 months ago', 'april 2025', 'a year ago')."
                     "Add 'is_competitor' filter only if the user query asks for the competitor data.",
        return_direct=True
    ),
    Tool(
        name="General chat tool",
        func=general_chat_tool,
        description="Handles general conversations. Action input should be your final answer.",
        return_direct=True
    )
]
