from typing import List, Optional
import aiohttp
from api_clients import call_openrouter_async

async def generate_search_queries_async(session: aiohttp.ClientSession, 
                                     user_query: str,
                                     model_config: dict) -> List[str]:
    """
    Generates search queries based on user input using LLM.
    
    Args:
        session: aiohttp client session
        user_query: Original user query
        model_config: Configuration for the selected model
        
    Returns:
        List of generated search queries
    """
    prompt = (
        "You are an expert research assistant. Given the user's query, generate up to four distinct, "
        "precise search queries that would help gather complete information on the topic. "
        "Return only a Python list of strings, for example: ['query1', 'query2', 'query3']."
    )
    messages = [
        {"role": "system", "content": "You are a helpful and precise research assistant."},
        {"role": "user", "content": f"User Query: {user_query}\n\n{prompt}"}
    ]
    
    response = await call_openrouter_async(session, messages, model_config)
    if response:
        try:
            return eval(response)
        except Exception as e:
            print("Error parsing search queries:", e)
    return []

async def is_page_useful_async(session: aiohttp.ClientSession, 
                             user_query: str, 
                             page_text: str,
                             model_config: dict) -> str:
    """
    Evaluates if a webpage is relevant to the user query.
    
    Args:
        session: aiohttp client session
        user_query: Original user query
        page_text: Webpage content
        model_config: Configuration for the selected model
        
    Returns:
        'Yes' or 'No' indicating page usefulness
    """
    prompt = (
        "You are a critical research evaluator. Given the user's query and the content of a webpage, "
        "determine if the webpage contains information that is useful for addressing the query. "
        "Respond with exactly one word: 'Yes' if the page is useful, or 'No' if it is not."
    )
    messages = [
        {"role": "system", "content": "You are a strict and concise evaluator of research relevance."},
        {"role": "user", "content": f"User Query: {user_query}\n\nWebpage Content:\n{page_text[:20000]}\n\n{prompt}"}
    ]
    
    response = await call_openrouter_async(session, messages, model_config)
    return "Yes" if response and "Yes" in response else "No"
