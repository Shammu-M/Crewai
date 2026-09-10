# CrewAI Banking Assistant

A proof-of-concept conversational banking assistant using Streamlit, CrewAI, Groq's ChatGroq integration, and SQLite-backed mock MCP tools.

## Run

1. Create a Python 3.10+ environment and install dependencies. Python 3.13 is recommended for the current CrewAI release range:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Set the Groq provider key. The model name is fixed to the free-tier `openai/gpt-oss-120b` model.

   ```powershell
   $env:GROQ_API_KEY = "your-groq-api-key"
   ```

3. Launch Streamlit:

   ```powershell
   streamlit run app.py
   ```

The database is regenerated at app startup. There is deliberately no authentication or authorization; every request uses `DEMO-USER-001`. The MCP server integrations are simulated by CrewAI tools querying SQLite. `MAX_RPM` is set to 900 for headroom below the provider's 1000 RPM limit, and provider 429 responses are retried with exponential backoff.

## MVC layout

- `models/`: SQLite data model and mocked MCP endpoints.
- `services/`: CrewAI orchestration and ChatGroq configuration.
- `controllers/`: request handling and error translation.
- `views/`: Streamlit presentation and session history.
- `app.py`: thin application entry point.
