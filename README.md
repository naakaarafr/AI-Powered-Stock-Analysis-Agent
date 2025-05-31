# AI-Powered Stock Analysis Tool 🚀

*Maintained by: naakaarafr 👤*

This project leverages the CrewAI framework and Google's Gemini Large Language Model to perform comprehensive stock analysis. It utilizes a team of specialized AI agents, each focusing on different aspects of financial research, analysis, and advisory, to provide insights and recommendations based on user-defined stocks and investor profiles. 📈🤖

## Table of Contents 📚

1. [Features ✨](#features-)
2. [Tech Stack 🛠️](#tech-stack-)
3. [Prerequisites ✅](#prerequisites-)
4. [Setup and Installation 🖥️](#setup-and-installation-)
5. [Configuration 🔧](#configuration-)
6. [Usage 🚀](#usage-)

   * [CLI Mode 🖥️](#cli-mode-)
   * [Interactive Mode 🗣️](#interactive-mode-)
   * [Output 📄](#output-)
7. [Running Diagnostics 🩺](#running-diagnostics-)
8. [Project Structure 🗂️](#project-structure-)
9. [Key Components 🔑](#key-components-)

   * [Agents 🤖](#agents-)
   * [Tasks 📋](#tasks-)
   * [Tools 🧰](#tools-)
10. [Error Handling and Timeouts ⏱️](#error-handling-and-timeouts-)
11. [Potential Future Enhancements 🚀](#potential-future-enhancements-)

## Features ✨

* **Multi-Stock Analysis 📊:** Analyze one or more stock ticker symbols simultaneously. 🔄
* **Quick & Comprehensive Modes ⏩/🔍:**

  * **Quick Analysis 💨:** Provides a fast, high-level overview and recommendation.
  * **Comprehensive Analysis 🧐:** Conducts a deep dive into financials, market trends, SEC filings (if enabled), and provides detailed reports.
* **Investor Profile Customization 🧑‍💼:** Tailors analysis and recommendations based on investor goals, risk tolerance, investment horizon, and amount. 🎯
* **Specialized AI Agents 🤖:**

  * `Senior Stock Research Analyst` 🔍: Gathers and analyzes financial data, market trends, and industry insights.
  * `Expert Financial Analyst` 📈: Focuses on financial metrics, ratios, and valuation models.
  * `Senior Investment Advisor` 💡: Provides personalized recommendations and strategic advice.
  * `Chief Market Strategist` 🌐: Analyzes macroeconomic conditions and market dynamics.
* **Tool Integration 🔗:**

  * **Web Search 🌐:** Uses SerperDevTool for up-to-date information.
  * **Financial Calculator 🧮:** Performs basic financial calculations.
  * **Stock Metrics Analyzer 📑:** Parses and presents basic stock data.
  * **SEC Filings Analysis 🏛️:** (Optional) Extracts and searches information from 10-K and 10-Q filings using `sec-api`.
* **CLI and Interactive Modes 💻🤝:** Offers flexibility for users to run analyses via command-line arguments or an interactive prompt.
* **Robust API Key Management 🔒:** Securely loads API keys using `.env` files.
* **Detailed Logging & Error Handling 📝⚠️:** Provides step-by-step execution feedback and graceful error management.
* **Configurable Timeouts ⏲️:** Allows users to set timeouts for analysis tasks to manage execution time.
* **Output Saving 💾:** Automatically saves analysis results to a timestamped file in an `analysis` directory, with an option for custom filenames.

## Tech Stack 🛠️

* **Programming Language 🐍:** Python 3.9+.
* **Core AI Framework 🤖:** CrewAI.
* **Large Language Model 🧠:** Google Gemini (specifically `gemini-2.0-flash` as configured, can be changed).
* **Key Libraries 📦:**

  * `python-dotenv` 🌱: For managing environment variables.
  * `crewai`, `crewai-tools` 🤝: For building and managing AI agent crews.
  * `langchain-google-genai` 🌊: For integrating Google's generative AI models.
  * `requests`,  `html2text` 🔍: For web scraping and content processing (used by SEC tools).
  * `sec-api` 🏢: (Optional) For accessing SEC filing data.
  * `argparse` 📚: For command-line interface.
  * `colorama`, `rich` 🎨: For enhanced console output (implicitly used by CrewAI).

## Prerequisites ✅

* **Python 🐍:** Version 3.9 or higher recommended.
* **API Keys 🔑:**

  * **Google API Key 🌐 (Critical):** For accessing Google Gemini LLM.

    * Enable the "Generative Language API" (sometimes referred to as "Vertex AI API" or similar for Gemini models) in your Google Cloud Console.
  * **Serper API Key 🌐 (Optional, Recommended):** For enabling web search capabilities for agents. Get one from [serper.dev](https://serper.dev/).
  * **SEC API Key 🏛️ (Optional):** For enabling tools to analyze SEC 10-K and 10-Q filings. Get one from [sec-api.io](https://sec-api.io/).
* **Git 🧑‍💻:** For cloning the repository.

## Setup and Installation 🖥️

1. **Clone the Repository 🐙:**

   ```bash
   git clone <repository_url> 🚀
   cd <repository_directory>
   ```

2. **Create a Virtual Environment (Recommended) 🛡️:**

   ```bash
   python -m venv venv 🔧
   source venv/bin/activate  # On Windows: venv\Scripts\activate 🚪
   ```

3. **Install Dependencies 📥:**

   ```bash
   pip install -r requirements.txt 📦
   ```

## Configuration 🔧

The application uses a `.env` file to manage API keys and other configurations.

1. **Create a ****************`.env`**************** file** in the root directory of the project. 📄
2. **Add your API keys** to the `.env` file. See `config.py` for variables used.

   ```env
   # .env file 🌱
   GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"  🔑
   SERPER_API_KEY="YOUR_SERPER_API_KEY_HERE"  🌐  # Optional, for web search
   SEC_API_API_KEY="YOUR_SEC_API_KEY_HERE"    🏛️  # Optional, for SEC filing tools

   # The following are set by config.py to force Gemini usage with CrewAI
   # You typically do not need to set these in your .env file
   # OPENAI_API_KEY=""
   # OPENAI_MODEL_NAME=""
   # OPENAI_API_BASE=""
   ```

   * Replace `"YOUR_..._KEY_HERE"` with your actual API keys.
   * If you don't have/want to use `SERPER_API_KEY` or `SEC_API_API_KEY`, you can omit them or leave them blank. The application will issue warnings but continue with limited functionality.

## Usage 🚀

The application can be run in two modes: CLI mode or Interactive mode.

### CLI Mode 🖥️

Run `main.py` with arguments. Use `python main.py -h` or `python main.py --help` to see all available options.

**Syntax:**

````bash
python main.py -s <STOCK1> [STOCK2 ...] [options] ⚙️

Common Options:

-s, --stocks: (Required) List of stock ticker symbols (e.g., AAPL MSFT GOOGL). 🏷️
-q, --quick: Run quick analysis. ⚡
-c, --comprehensive: Run comprehensive analysis (slower, more detailed, enables SEC tools if API key is present). 🏊‍♂️
-g, --goals: Investment goals (default: "long-term growth"). 🎯
-r, --risk: Risk tolerance (choices: conservative, moderate, aggressive, high; default: moderate). 📉
-t, --horizon: Investment time horizon (choices: short-term, medium-term, long-term, 5+ years; default: long-term). ⏳
-a, --amount: Investment amount (default: "$10,000"). 💵
--timeout: Analysis timeout in seconds (default: 300; comprehensive analysis gets 2x this value). ⏲️
--no-timeout: Disable timeout for analysis. ❌⏲️
-o, --output: Save results to a specific file. 💾
-v, --verbose: Enable verbose output during execution. 🗣️

Examples:

Quick analysis for Apple and Microsoft with default investor profile:

```bash
python main.py -s AAPL MSFT -q 🚀
````

Comprehensive analysis for Tesla, specifying investor profile and a longer timeout:

```bash
python main.py -s TSLA -c --goals "aggressive growth" --risk high --timeout 600 🏁
```

Comprehensive analysis for multiple stocks with no timeout and saving to a custom file:

```bash
python main.py -s NVDA AMD INTC -c --no-timeout -o ./analysis_reports/semiconductors_report.txt 💾
```

### Interactive Mode 🗣️

If you run `main.py` without any arguments, it will start in interactive mode.

```bash
python main.py 🗨️
```

The application will then guide you through:

1. Entering stock symbols. 💹
2. Setting up your investor profile (goals, risk tolerance, horizon, amount). 🎯
3. Choosing the analysis type (Quick or Comprehensive). ⚡🧐
4. Selecting timeout options for comprehensive analysis. ⏳

### Output 📄

* **Console:** Analysis progress and final results are printed to the console. 🖨️
* **File:**

  * If the `-o` flag is used in CLI mode, results are saved to the specified file. 📂
  * Otherwise (and in interactive mode if chosen), results are automatically saved to a timestamped `.txt` file in an `analysis` directory created in the project root (e.g., `analysis/quick_analysis_20250530_143000.txt`). 📅

## Running Diagnostics 🩺

Before running the main application, especially if you encounter issues, you can run the `debug_api.py` script. This script tests:

* Internet connectivity. 🌐
* Validity and connectivity for Google, Serper, and SEC API keys. 🔑
* Basic CrewAI and Gemini integration. 🤝
* Custom tool functionality. 🧰
* Agent and task creation. 🤖

```bash
python debug_api.py 🛠️
```

This will provide a summary of which components are working correctly and offer troubleshooting tips for failed tests. 📝

## Project Structure 🗂️

```
.
├── .env                   # API keys and environment variables (user-created) 🌱
├── analysis/              # Default directory for saving analysis reports (auto-created) 📂
├── agents.py              # Defines the AI agents (Research Analyst, Financial Analyst, etc.) 👥
├── config.py              # Handles configuration, API key loading, and LLM setup 🔄
├── crew.py                # Orchestrates the agents and tasks into a CrewAI crew 🏋️‍♂️
├── debug_api.py           # Script to test API connections and core setup 🩺
├── main.py                # Main entry point for CLI and interactive mode 🚀
├── main_test.py           # A simplified test script for basic workflow validation ✅
├── requirements.txt       # Python dependencies 📦
├── tasks.py               # Defines the tasks for the AI agents 📋
├── tools.py               # Defines custom tools (Financial Calculator, SEC Search, etc.) 🧰
└── README.md              # This file 📖
```

## Key Components 🔑

### Agents 🤖

Specialized AI entities with specific roles, goals, and backstories. They use the configured LLM (Gemini) and tools to perform their duties:

* **Research Analyst 🔍:** Focuses on data gathering.
* **Financial Analyst 📊:** Focuses on metrics and valuation.
* **Investment Advisor 💼:** Focuses on recommendations.
* **Market Strategist 🌍:** Focuses on macro trends.

### Tasks 📋

Specific assignments given to agents. Each task has a description, an expected output, and is assigned to an agent:

* **Research Task 📰:** Gather comprehensive information.
* **Financial Analysis Task 📑:** Perform in-depth financial evaluation.
* **Investment Recommendation Task 📝:** Generate advice based on analysis and profile.
* **Market Analysis Task 🌐:** Assess market conditions.

Workflows (`create_analysis_workflow`, `create_quick_analysis_workflow`) assemble these tasks. 🔄

### Tools 🧰

Functions that agents can use to interact with the external world or perform specific calculations:

* **financial\_calculator 🧮:** For math operations.
* **analyze\_stock\_metrics 📈:** Basic stock data parsing.
* **SerperDevTool 🌐:** For web searches (if Serper API key is provided).
* **SEC10KTool / SEC10QTool 🏛️:** RAG tools to search within SEC filings (if SEC API key and `sec-api` package are available). These tools fetch the latest 10-K/10-Q filing for a stock, process its content, and allow agents to query it.

## Error Handling and Timeouts ⏱️

* `main.py` includes robust error handling to catch common issues like missing API keys, connection failures, and task execution errors. ⚠️
* It implements a cross-platform timeout mechanism for long-running analysis tasks, which can be configured via CLI arguments or disabled. ⏲️🔒
* The `debug_api.py` script is the first line of defense for diagnosing setup and API key problems. 🩺

## Potential Future Enhancements 🚀

* **More Advanced Tools 🔧:**

  * Integration with financial data APIs (e.g., Alpha Vantage, IEX Cloud) for real-time price data, historical data, and more detailed fundamentals. 🌐
  * Chart generation or technical analysis indicator calculation tools. 📈
* **Expanded Agent Capabilities 🤖:**

  * Sentiment analysis agent for news and social media. 📰
  * Risk modeling agent. ⚖️
* **User Interface 🖥️:** A web-based GUI (e.g., using Streamlit or FastAPI) for easier interaction. 🌐🎨
* **Sophisticated Financial Models 📊:** Implement more complex valuation models (e.g., detailed DCF) directly within tools or tasks.
* **Portfolio Management Features 💼:** Allow users to track a portfolio and get rebalancing advice. 🔄
* **Backtesting 🕰️:** Add functionality to backtest strategies based on agent recommendations. 🧪
* **Caching 📀:** Implement caching for API calls (e.g., SEC filings, search results) to speed up repeated analyses and reduce API usage. ⚡
* **Asynchronous Operations 🔄:** For improved performance when handling multiple stocks or long-running tasks.

---

*Happy analyzing! 📈💼*
