"""Web search tool using Tavily."""

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for current, real-time information about the given query.
    Use this when the user asks about news, prices, current events, or anything
    that requires up-to-date information."""
    try:
        import os
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY", "")
        if not api_key:
            return (
                "Web search is not configured yet. "
                f"Captured search query for later: {query}"
            )

        client = TavilyClient(api_key=api_key)
        result = client.search(query, max_results=3)

        if not result.get("results"):
            return f"No results found for: {query}"

        formatted = []
        for r in result["results"]:
            title = r.get("title", "Untitled")
            content = r.get("content", "")[:300]
            url = r.get("url", "")
            formatted.append(f"**{title}**\n{content}\n🔗 {url}")

        return "\n\n".join(formatted)

    except ImportError:
        return (
            "Web search is not available — tavily-python is not installed. "
            f"Captured search query for later: {query}"
        )
    except Exception as e:
        return f"Search failed: {e}"
