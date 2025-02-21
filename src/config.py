import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys from environment variables
JINA_API_KEY = os.getenv('JINA_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# API endpoints
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SERPAPI_URL = "https://serpapi.com/search"
JINA_BASE_URL = "https://r.jina.ai/"

# Validate required API keys
if not all([JINA_API_KEY, SERPAPI_API_KEY, OPENROUTER_API_KEY]):
    raise ValueError(
        "Missing required API keys. Please ensure JINA_API_KEY, SERPAPI_API_KEY, "
        "and OPENROUTER_API_KEY are set in your .env file."
    )

# Model Configurations
AVAILABLE_MODELS = {
     "deepseek-ai/deepseek-llm-67b": {
        "name": "DeepSeek R1",
        "description": "High-performance model for deep analysis",
        "max_tokens": 8192,
        "cost": "High"
    },
    "deepseek-ai/deepseek-llm-7b": {
        "name": "DeepSeek LLM 7B",
        "description": "Smaller version, efficient for common tasks",
        "max_tokens": 4096,
        "cost": "Medium"
    },
    "qwen/qwen-72b": {
        "name": "Qwen 72B",
        "description": "Large-scale model with strong capabilities",
        "max_tokens": 8192,
        "cost": "High"
    },
    "qwen/qwen-14b": {
        "name": "Qwen 14B",
        "description": "Balanced performance for cost efficiency",
        "max_tokens": 4096,
        "cost": "Medium"
    },
    "mistral/mistral-7b": {
        "name": "Mistral 7B",
        "description": "Lightweight model with strong reasoning skills",
        "max_tokens": 4096,
        "cost": "Medium"
    },
    "mistral/mixtral-8x7b": {
        "name": "Mixtral 8x7B",
        "description": "Sparse mixture of experts for optimal balance",
        "max_tokens": 8192,
        "cost": "High"
    },
    "anthropic/claude-3-opus-20240229": {
        "name": "Claude 3 Opus",
        "description": "Most capable model, best for complex research",
        "max_tokens": 4096,
        "cost": "High"
    },
    "anthropic/claude-3-sonnet-20240229": {
        "name": "Claude 3 Sonnet",
        "description": "Balanced performance and speed",
        "max_tokens": 4096,
        "cost": "Medium"
    },
    "anthropic/claude-3-haiku-20240229": {
        "name": "Claude 3 Haiku",
        "description": "Fastest model, good for quick research",
        "max_tokens": 4096,
        "cost": "Low"
    },
    "openai/gpt-4-turbo-preview": {
        "name": "GPT-4 Turbo",
        "description": "Alternative high-capability model",
        "max_tokens": 4096,
        "cost": "High"
    },
    "openai/gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "description": "Fast and cost-effective",
        "max_tokens": 4096,
        "cost": "Very Low"
    }
}

# Default settings
DEFAULT_MODEL = "anthropic/claude-3-sonnet-20240229"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000