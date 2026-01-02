from langchain_core.tools import tool
from tavily import TavilyClient
import os

@tool
def tavily_search_tool(query: str) -> str:
    """
    Searches ONLY the Revnix website using Tavily Search.
    """
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        response = tavily_client.search(
            query=query,
            max_results=3,
            include_domains=["revnix.com"]
            )

        results = response.get("results", [])

        if not results:
            return "No relevant information found on the Revnix website."

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}]\n"
                f"{result.get('snippet', '')}\n"
                f"URL: {result.get('url', '')}\n"
            )

        return "\n".join(context_parts)

    except Exception as e:
        return f"Error during Tavily search: {str(e)}"
