# Open Researcher AI Assistant 🔍

An open-source implementation of an AI-powered research assistant that helps gather and synthesize information on any topic using multiple decentralized AI models.

## 🌟 Features

- **Multi-Model Support**: Leverages various AI models through OpenRouter, including:
  - Claude 3 (Opus, Sonnet, Haiku)
  - GPT-4 Turbo
  - Mixtral 8x7B
  - DeepSeek
  - Qwen
  - And more...
- **Adaptive Research Depth**: Choose between Quick, Standard, and Deep research modes
- **Intelligent Query Generation**: Automatically generates and refines search queries
- **Smart Content Filtering**: Evaluates webpage relevance before inclusion
- **Detailed Process Logging**: Track the research progress in real-time
- **User-Friendly Interface**: Built with Gradio for easy interaction

## 🚀 Getting Started

### Prerequisites

- Python 3.12.5
- Poetry (for dependency management)

### Installation

1. Clone the repository:

bash
git clone https://github.com/yourusername/free-deep-researcher.git
cd free-deep-researcher

2. Install dependencies using Poetry:
bash
poetry install


3. Copy the environment template and add your API keys: 
bash
cp .dev_env .env

Edit `.env` with your API keys:

env
OPENROUTER_API_KEY = "your_openrouter_key"
SERPAPI_API_KEY = "your_serpapi_key"
JINA_API_KEY = "your_jina_key"


### Required API Keys

- **OpenRouter**: Sign up at [OpenRouter](https://openrouter.ai/) to access multiple AI models
- **SerpAPI**: Get your key from [SerpAPI](https://serpapi.com/) for web search capabilities
- **Jina**: Obtain your key from [Jina](https://jina.ai/) for content extraction

## 🎮 Usage

1. Start the application:


2. Open your web browser and navigate to the local Gradio interface (typically `http://localhost:7860`)

3. Enter your research query and configure:
   - Select an AI model
   - Adjust the maximum iterations
   - Choose research depth (Quick/Standard/Deep)

4. Click "Begin Research" and watch the assistant work!

## 🛠️ Architecture

The project consists of several key components:

- `src/main.py`: Main application and Gradio interface
- `src/api_clients.py`: API client implementations for various services
- `src/research_agents.py`: Core research logic and AI prompting
- `src/config.py`: Configuration management

## 📊 Research Process

1. **Query Analysis**: The AI analyzes the user's query to generate initial search queries
2. **Web Search**: Utilizes SerpAPI to find relevant web pages
3. **Content Extraction**: Uses Jina to extract clean text from web pages
4. **Relevance Evaluation**: AI evaluates content relevance to the query
5. **Information Synthesis**: Combines findings into a comprehensive report
6. **Iterative Refinement**: Generates new queries based on findings until satisfied

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenRouter for providing access to multiple AI models
- SerpAPI for web search capabilities
- Jina for content extraction services
- The open-source community for various tools and libraries used in this project

## ⚠️ Disclaimer

This is an independent, open-source implementation and is not officially affiliated with OpenAI or any other AI providers mentioned.

## 📧 Contact

For questions and support, please open an issue in the GitHub repository or contact the maintainers directly.

---
Made with ❤️ by the open-source community