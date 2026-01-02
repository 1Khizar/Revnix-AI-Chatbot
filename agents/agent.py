from langchain_classic.agents import create_react_agent, AgentExecutor
from model.llm import llm
from prompt.system_prompt import get_agent_prompt

from tools.retriever_tool import create_retriever_tool
from tools.tavily_search_tool import tavily_search_tool

def create_rag_agent(vector_store):
    retriever_tool = create_retriever_tool(vector_store)
    prompt = get_agent_prompt()

    agent = create_react_agent(
        llm=llm,
        tools=[retriever_tool, tavily_search_tool],
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[retriever_tool, tavily_search_tool],
        verbose=False,
        handle_parsing_errors=True,
    )

    return agent_executor
