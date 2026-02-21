# Travel Planner AI: Agentic Architecture

This is an autonomous, multi-agent travel intelligence system that moves beyond standard LLM outputs. By leveraging CrewAI and Groq-powered Llama 3 models, the application orchestrates a sequence of specialized AI agents to perform real-time research, curate local experiences, and construct logic-driven travel blueprints.

## The Agentic Engine

The system is built on a specialized intelligence model where three distinct agents collaborate through a sequential process. Rather than a single prompt attempt, the work is divided into specialized roles that build upon each other's outputs.

### 1. Local Researcher
The researcher scours the web using the Serper API to find high-signal information about destinations. It identifies current trends, seasonal nuances, and essential logistical data that static models might miss.

### 2. Cultural Concierge
This agent synthesizes the raw research into a curated selection of experiences. It focuses on authentic local vibes and hidden gems, filtering out standard tourist traps to provide more meaningful travel suggestions.

### 3. Master Strategist
The strategist is the final architect who maps out the day-by-day plan. It handles geographic optimization by grouping nearby spots, manages budget-tiering, and ensures practical timing for all activities.

## Core Technical Concepts

*   **Deterministic Orchestration**: A sequential task flow ensures the itinerary is always grounded in verified research before planning begins.
*   **Real-Time Data Injection**: By using the Serper API, the system bypasses LLM knowledge cutoffs to fetch live pricing and local availability.
*   **Geospatial Integration**: The system automatically generates deep-linked Google Maps queries for every location mentioned in the final report.
*   **Multi-Tier Budgeting**: Costs are dynamically calculated across Budget, Mid-range, and Comfort profiles to give the user a realistic financial overview.

## Project Structure

```text
travel-chatbot/
├── TravelCrewApp.py        # Streamlit-native UI and Orchestration Layer
├── TravelAgents.py         # Agent role definitions and LLM configurations
├── TravelTasks.py          # Structured prompt engineering for workflows
├── tools/                  # Custom tools for search integration
├── docs/                   # Full technical documentation and agent logic
└── .streamlit/             # UI themes and secure secret management
```

## Quick Start

### 1. Environment Setup
The project requires Python 3.11.

```bash
py -3.11 -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. API Configuration
1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
2. Populate the file with your `GROQ_API` and `SERPER_API_KEY`.

### 3. Launch
```bash
streamlit run TravelCrewApp.py
```

## Technical Stack

*   **Framework**: [CrewAI](https://crewai.com) for agentic orchestration.
*   **Model**: Groq Llama 3.3 70B for low-latency, high-reasoning inference.
*   **UI**: Streamlit for a responsive, Python-native frontend.
*   **Search**: Serper.dev for real-time web data retrieval.

---
Sai Buvanesh