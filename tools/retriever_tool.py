from langchain_core.tools import tool

def create_retriever_tool(vector_store):
    """
    Create a retriever tool for the agent
    
    Args:
        vector_store: Pinecone vector store instance
    
    Returns:
        tool: Retriever tool function
    """
    
    @tool
    def retrieve_revnix_info(query: str) -> str:
        """
        Retrieves relevant information about Revnix from the knowledge base.
        Use this tool to search for information about Revnix Technologies, its products, services, team, career opportunities, or any other related topics.
        
        Args:
            query: The search query to find relevant information
            
        Returns:
            str: Relevant information from the Revnix knowledge base
        """
        try:
            # Create retriever with top 3 results
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            
            # Retrieve documents
            docs = retriever.invoke(query)
            
            # Format the context
            if not docs:
                return "No relevant information found in the knowledge base."
            
            context_parts = []
            for i, doc in enumerate(docs, 1):
                context_parts.append(f"[Source {i}]:\n{doc.page_content}\n")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Error retrieving information: {str(e)}"
    
    return retrieve_revnix_info