import aiohttp
from typing import List, Dict, Optional
from config import *

async def call_openrouter_async(session: aiohttp.ClientSession, 
                              messages: List[dict], 
                              model_config: dict = None) -> Optional[str]:
    """
    Makes an async call to the OpenRouter API.
    
    Args:
        session: aiohttp client session
        messages: List of message dictionaries
        model_config: Configuration for the selected model
    """
    if not model_config:
        model_config = AVAILABLE_MODELS[DEFAULT_MODEL]
        
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "X-Title": "Research Assistant"  # Optional - your app's name
    }
    
    data = {
        "model": model_config.get("model_id", DEFAULT_MODEL),  # Use model_id from config or default
        "messages": messages,
        "temperature": DEFAULT_TEMPERATURE,
        "max_tokens": model_config.get("max_tokens", DEFAULT_MAX_TOKENS)
    }
    
    try:
        async with session.post(OPENROUTER_URL, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                print(f"OpenRouter API error: {response.status}")
                print(f"Error details: {error_text}")
                return None
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return None

async def perform_search_async(session: aiohttp.ClientSession, 
                             query: str) -> List[str]:
    """
    Performs an async search using SERPAPI.
    
    Args:
        session: aiohttp client session
        query: Search query string
        
    Returns:
        List of URLs from search results
    """
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google"
    }
    try:
        async with session.get(SERPAPI_URL, params=params) as resp:
            if resp.status == 200:
                results = await resp.json()
                return [item.get("link") for item in results.get("organic_results", [])]
            return []
    except Exception as e:
        print("Error performing SERPAPI search:", e)
        return []

async def fetch_webpage_text_async(session: aiohttp.ClientSession, 
                                 url: str) -> str:
    """
    Fetches webpage content using Jina API.
    
    Args:
        session: aiohttp client session
        url: Target webpage URL
        
    Returns:
        Extracted text content from webpage
    """
    full_url = f"{JINA_BASE_URL}{url}"
    headers = {"Authorization": f"Bearer {JINA_API_KEY}"}
    try:
        async with session.get(full_url, headers=headers) as resp:
            return await resp.text() if resp.status == 200 else ""
    except Exception as e:
        print("Error fetching webpage text:", e)
        return ""