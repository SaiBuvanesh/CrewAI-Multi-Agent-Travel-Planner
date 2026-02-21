# 🤝 Contribution Protocols

Thank you for contributing to the Travel Planner AI. We maintain a high standard for agentic orchestration and code quality.

## 🛠️ Development Workflow

1.  **Fork & Clone**:
    ```bash
    git clone https://github.com/your-username/travel-chatbot.git
    cd travel-chatbot
    ```
2.  **Environment Isolation**: Use Python 3.11.
    ```bash
    py -3.11 -m venv venv
    source venv/bin/activate
    ```
3.  **Dependency Initialization**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Local Secrets**:
    ```bash
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    ```

## 🏗️ Architectural Guidelines
When contributing new agents or tasks:
- **Atomicity**: Ensure each agent has a single, well-defined role.
- **Context Awareness**: Use `context` in `TravelTasks.py` to bridge information between agents.
- **Determinism**: Keep LLM temperatures low (0.2 - 0.3) for factual grounding.
- **Scalability**: All new tools should be added to the `tools/` directory with proper abstraction.

## 🧪 Quality Assurance
Before submitting a Pull Request:
- [x] Verify the Streamlit UI initializes without state conflicts.
- [x] Ensure all agentic loops complete within 3–5 minutes.
- [x] Confirm no API secrets are committed to the repository.
- [x] Update `docs/ARCHITECTURE.md` if the orchestration flow changes.

## 📥 Submission
1.  Push to a feature branch (`feature/your-enhancement`).
2.  Open a Pull Request with a clear description of the logic changes.
3.  Link any relevant issues.

---
*Elevating travel intelligence through collaborative code.*
