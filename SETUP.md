# Development Setup Guide

Follow these steps to set up the Travel Planner AI on your local machine.

## Prerequisites
- **Python 3.11**: Strict requirement for library compatibility.
- **Git**: For version control and cloning.
- **API Keys**: Groq (LLM Inference) and Serper.dev (Web Search).

---

## 1. Branch Deployment
Clone the repository and enter the project directory:
```bash
git clone <repository-url>
cd travel-chatbot
```

## 2. Environment Synchronization
We recommend using a virtual environment to manage dependencies locally.

### Windows
```powershell
py -3.11 -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Secret Management
The application uses Streamlit's native secrets management for API authentication.

1. Navigate to the `.streamlit` directory.
2. Duplicate the template file:
    ```bash
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    ```
3. Open `.streamlit/secrets.toml` and populate your keys:
    ```toml
    GROQ_API = "gsk_your_key_here"
    SERPER_API_KEY = "your_serper_key_here"
    ```

> [!NOTE]
> Ensure you maintain the exact variable names from the example file to ensure compatibility with the orchestration layer.

---

## 4. Execution
Launch the orchestration engine and frontend:
```bash
streamlit run TravelCrewApp.py
```

## Troubleshooting

| System Response | Potential Fix |
| :--- | :--- |
| `ModuleNotFoundError` | Verify the virtual environment is active and `pip install` was successful. |
| `Model not found` | Check your `GROQ_API` key permissions and model availability. |
| `Rate limit reached` | The Groq free tier has limits. The system uses `max_rpm=3` to mitigate this. |
