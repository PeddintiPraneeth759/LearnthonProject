"""
LangGraph-based News Verification Agent
Uses a multi-step workflow to verify news claims
"""
import json
import re
from datetime import date
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL
from utils.prompts import SYSTEM_PROMPT, VERIFICATION_PROMPT
from agents.search_agent import search_agent
from models.schemas import VerificationResponse, TrustedSource


class VerificationState(TypedDict):
    """State for the verification workflow"""
    claim: str
    search_query: str
    search_results: str
    raw_results: list
    llm_response: str
    final_response: dict
    error: str


class NewsVerifier:
    """LangGraph-based news verification agent"""
    
    def __init__(self):
        # Initialize LLM with OpenRouter
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base=OPENROUTER_BASE_URL,
            temperature=0.1,
            default_headers={
                "HTTP-Referer": "https://factcheck-ai.vercel.app",
                "X-Title": "Fake News Verify"
            },
            model_kwargs={
                "extra_headers": {
                    "HTTP-Referer": "https://factcheck-ai.vercel.app",
                    "X-Title": "Fake News Verify"
                }
            }
        )
        
        # Build the verification graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(VerificationState)
        
        # Add nodes
        workflow.add_node("prepare_search", self._prepare_search)
        workflow.add_node("web_search", self._web_search)
        workflow.add_node("analyze_and_verify", self._analyze_and_verify)
        workflow.add_node("format_response", self._format_response)
        
        # Define edges
        workflow.set_entry_point("prepare_search")
        workflow.add_edge("prepare_search", "web_search")
        workflow.add_edge("web_search", "analyze_and_verify")
        workflow.add_edge("analyze_and_verify", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    async def _prepare_search(self, state: VerificationState) -> VerificationState:
        """Prepare search query from the claim"""
        claim = state["claim"]
        
        # Create an effective search query
        # Add fact-check keywords to prioritize reliable sources
        search_query = f"{claim} fact check verification"
        
        return {**state, "search_query": search_query}
    
    async def _web_search(self, state: VerificationState) -> VerificationState:
        """Perform web search for verification"""
        try:
            # Perform search
            results = await search_agent.search(state["search_query"], num_results=10)
            
            # Also search with just the claim for broader results
            additional_results = await search_agent.search(state["claim"], num_results=5)
            
            # Combine and deduplicate
            all_urls = set()
            combined_results = []
            
            for result in results + additional_results:
                if result["url"] not in all_urls:
                    all_urls.add(result["url"])
                    combined_results.append(result)
            
            formatted_results = search_agent.format_results_for_llm(combined_results[:10])
            
            return {
                **state,
                "search_results": formatted_results,
                "raw_results": combined_results[:10]
            }
        except Exception as e:
            return {**state, "error": f"Search failed: {str(e)}", "search_results": "", "raw_results": []}
    
    async def _analyze_and_verify(self, state: VerificationState) -> VerificationState:
        """Use LLM to analyze search results and verify claim"""
        if state.get("error"):
            return state
        
        if not state["search_results"] or state["search_results"] == "No search results found.":
            # No search results - return unverified
            return {
                **state,
                "llm_response": json.dumps({
                    "verdict": "UNVERIFIED",
                    "confidence_score": 0.0,
                    "summary": "Unable to verify this claim due to insufficient search results. Please try rephrasing your query or check back later.",
                    "verified_facts": [],
                    "incorrect_or_misleading_parts": [],
                    "trusted_sources": []
                })
            }
        
        # Prepare the verification prompt
        prompt = VERIFICATION_PROMPT.format(
            claim=state["claim"],
            search_results=state["search_results"]
        )
        
        try:
            # Call LLM
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm.ainvoke(messages)
            llm_response = response.content
            
            return {**state, "llm_response": llm_response}
        except Exception as e:
            return {**state, "error": f"LLM analysis failed: {str(e)}"}
    
    async def _format_response(self, state: VerificationState) -> VerificationState:
        """Format the final response"""
        if state.get("error"):
            return {
                **state,
                "final_response": {
                    "verdict": "UNVERIFIED",
                    "confidence_score": 0.0,
                    "summary": f"Verification could not be completed: {state['error']}",
                    "verified_facts": [],
                    "incorrect_or_misleading_parts": [],
                    "trusted_sources": [],
                    "last_verified_date": date.today().isoformat()
                }
            }
        
        try:
            # Parse LLM response as JSON
            llm_response = state["llm_response"]
            
            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', llm_response)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = json.loads(llm_response)
            
            # Ensure we have exactly 5 trusted sources
            sources = parsed.get("trusted_sources", [])
            
            # If we don't have enough sources from LLM, supplement from raw results
            if len(sources) < 5 and state.get("raw_results"):
                existing_urls = {s.get("url") for s in sources}
                for result in state["raw_results"]:
                    if result["url"] not in existing_urls:
                        sources.append({
                            "title": result["title"],
                            "url": result["url"],
                            "publisher": result["publisher"]
                        })
                        if len(sources) >= 5:
                            break
            
            final_response = {
                "verdict": parsed.get("verdict", "UNVERIFIED"),
                "confidence_score": min(1.0, max(0.0, float(parsed.get("confidence_score", 0.0)))),
                "summary": parsed.get("summary", "Unable to provide summary."),
                "verified_facts": parsed.get("verified_facts", []),
                "incorrect_or_misleading_parts": parsed.get("incorrect_or_misleading_parts", []),
                "trusted_sources": sources[:5],
                "last_verified_date": date.today().isoformat()
            }
            
            return {**state, "final_response": final_response}
        except json.JSONDecodeError as e:
            return {
                **state,
                "final_response": {
                    "verdict": "UNVERIFIED",
                    "confidence_score": 0.0,
                    "summary": "Unable to parse verification results. The claim could not be verified at this time.",
                    "verified_facts": [],
                    "incorrect_or_misleading_parts": [],
                    "trusted_sources": [],
                    "last_verified_date": date.today().isoformat()
                }
            }
    
    async def verify(self, claim: str) -> dict:
        """
        Verify a news claim
        
        Args:
            claim: The news headline, paragraph, or claim to verify
            
        Returns:
            Verification response dictionary
        """
        initial_state: VerificationState = {
            "claim": claim,
            "search_query": "",
            "search_results": "",
            "raw_results": [],
            "llm_response": "",
            "final_response": {},
            "error": ""
        }
        
        # Run the verification workflow
        result = await self.graph.ainvoke(initial_state)
        
        return result["final_response"]


# Create singleton instance
news_verifier = NewsVerifier()
