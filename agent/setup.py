from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama
from agent.tools import tools
from config import LLM

llm = ChatOllama(model=LLM, temperature=0)
agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)