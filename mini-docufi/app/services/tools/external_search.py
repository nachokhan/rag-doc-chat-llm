"""
External search tool with AI-powered summarization.
"""
import os
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# In a real scenario, the google_web_search and web_fetch tools would be provided by the environment.
# For this implementation, we will use mock versions.
class MockGoogleWebSearch:
    def search(self, query: str, num_results: int = 5):
        print(f"Mock Google Search for: {query}")
        return {"results": [
            {"url": "https://www.mocksite.com/report1", "title": "Market Report 1"},
            {"url": "https://www.mocksite.com/report2", "title": "Market Report 2"},
        ]}

class MockWebFetch:
    def fetch(self, url: str):
        print(f"Mock Web Fetch for: {url}")
        return {"content": f"This is the mock content for {url}. It contains data about market size and top players."}

google_web_search = MockGoogleWebSearch()
web_fetch = MockWebFetch()

# --- Summarization Chain --- #
SUMMARIZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at summarizing web content. Extract the key information relevant to the user's original query."),
    ("user", "Original Query: {query}\n\nContent:\n{content}"),
])
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview", api_key=os.getenv("OPENAI_API_KEY"))
summarizer_chain = SUMMARIZER_PROMPT | llm | StrOutputParser()

# --- Credible Sources --- #
CREDIBLE_SOURCES = [
    "gartner.com", "idc.com", "forrester.com", "bloomberg.com", "reuters.com",
    "worldbank.org", "statista.com", "forbes.com", "mckinsey.com",
]

@tool
def external_search(query: str) -> str:
    """Performs a web search on credible sources, fetches the content of the top results, 
    and returns a summarized version of their content."""
    print(f"Executing AI-powered external search for: {query}")
    
    # 1. Perform Web Search
    site_queries = " OR ".join([f"site:{source}" for source in CREDIBLE_SOURCES])
    full_query = f'"{query}" ({site_queries})'
    search_results = google_web_search.search(query=full_query, num_results=5)

    if not search_results or not search_results.get("results"):
        return "No relevant external sources found."

    summaries = []
    for result in search_results["results"]:
        url = result["url"]
        try:
            # 2. Fetch Content
            fetched_content = web_fetch.fetch(url=url)
            if not fetched_content or not fetched_content.get("content"):
                continue

            # 3. Summarize Content
            summary = summarizer_chain.invoke({
                "query": query,
                "content": fetched_content["content"]
            })
            summaries.append(f"Source: {url}\nSummary: {summary}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue

    # 4. Compile Final Result
    if not summaries:
        return "Could not process any of the found external sources."
    
    return "\n\n---\n\n".join(summaries)
