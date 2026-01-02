def ask(agent, question: str) -> str:
    """
    Ask a question to the agent and return the answer
    
    Args:
        agent: Agent executor instance
        question: User's question
        
    Returns:
        str: Agent's answer
    """
    try:
        # Invoke the agent
        response = agent.invoke({"input": question})
        
        # Extract the answer
        if isinstance(response, dict) and "output" in response:
            return response["output"]
        else:
            return str(response)
            
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try asking your question again."

def format_sources(docs):
    """
    Format retrieved documents as sources
    
    Args:
        docs: List of retrieved documents
        
    Returns:
        str: Formatted sources string
    """
    if not docs:
        return "No sources found."
    
    sources = []
    for i, doc in enumerate(docs, 1):
        source = f"[{i}] {doc.page_content[:200]}..."
        sources.append(source)
    
    return "\n\n".join(sources)