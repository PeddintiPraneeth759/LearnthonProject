"""
Google Search Agent for web verification
Uses Google Custom Search API to find reliable sources
"""
import httpx
from typing import List, Dict, Any
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID


class SearchAgent:
    """Agent for performing web searches to verify claims"""
    
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.cse_id = GOOGLE_CSE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        # Preferred domains for fact-checking
        self.preferred_domains = [
            "bbc.com", "bbc.co.uk",
            "reuters.com",
            "apnews.com",
            "snopes.com",
            "politifact.com",
            "factcheck.org",
            "gov.uk", "gov",
            "who.int",
            "un.org"
        ]
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a Google Custom Search
        
        Args:
            query: Search query string
            num_results: Number of results to return (max 10 per request)
            
        Returns:
            List of search results with title, url, snippet, and publisher
        """
        if not self.cse_id:
            # Fallback to web search simulation if no CSE ID
            return await self._fallback_search(query, num_results)
        
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "num": min(num_results, 10)
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                results = []
                for item in data.get("items", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "publisher": self._extract_publisher(item.get("link", ""))
                    })
                
                return results
            except Exception as e:
                print(f"Search error: {e}")
                return await self._fallback_search(query, num_results)
    
    async def _fallback_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Fallback search using a simple web scraping approach
        This is used when Google CSE is not configured
        """
        # Use DuckDuckGo HTML as fallback (no API key needed)
        search_url = "https://html.duckduckgo.com/html/"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    search_url,
                    data={"q": query},
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=30.0
                )
                
                # Parse simple results from HTML
                results = self._parse_ddg_results(response.text, num_results)
                return results
            except Exception as e:
                print(f"Fallback search error: {e}")
                return []
    
    def _parse_ddg_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse DuckDuckGo HTML results"""
        import re
        
        results = []
        
        # Simple regex to extract links and titles
        pattern = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
        snippet_pattern = r'<a[^>]+class="result__snippet"[^>]*>([^<]+)</a>'
        
        matches = re.findall(pattern, html)
        snippets = re.findall(snippet_pattern, html)
        
        for i, (url, title) in enumerate(matches[:num_results]):
            snippet = snippets[i] if i < len(snippets) else ""
            results.append({
                "title": title.strip(),
                "url": url,
                "snippet": snippet.strip(),
                "publisher": self._extract_publisher(url)
            })
        
        return results
    
    def _extract_publisher(self, url: str) -> str:
        """Extract publisher name from URL"""
        from urllib.parse import urlparse
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            
            # Map common domains to publisher names
            publisher_map = {
                "bbc.com": "BBC",
                "bbc.co.uk": "BBC",
                "reuters.com": "Reuters",
                "apnews.com": "Associated Press",
                "snopes.com": "Snopes",
                "politifact.com": "PolitiFact",
                "factcheck.org": "FactCheck.org",
                "nytimes.com": "The New York Times",
                "washingtonpost.com": "The Washington Post",
                "theguardian.com": "The Guardian",
                "cnn.com": "CNN",
                "nbcnews.com": "NBC News",
                "abcnews.go.com": "ABC News",
                "who.int": "World Health Organization",
                "un.org": "United Nations"
            }
            
            return publisher_map.get(domain, domain.split(".")[0].title())
        except:
            return "Unknown"
    
    def format_results_for_llm(self, results: List[Dict[str, Any]]) -> str:
        """Format search results for LLM consumption"""
        if not results:
            return "No search results found."
        
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"""
Result {i}:
Title: {result['title']}
URL: {result['url']}
Publisher: {result['publisher']}
Snippet: {result['snippet']}
""")
        
        return "\n".join(formatted)


# Create singleton instance
search_agent = SearchAgent()
