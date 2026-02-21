"""
search_tools.py
---------------
Configures the SerperDevTool for web search capabilities.
Relies on STREAMLIT_SECRETS or environment variables for the API key.
"""

import os
import streamlit as st
from crewai_tools import SerperDevTool

# Get SERPER_API_KEY from Streamlit secrets or environment variable
try:
    serper_api_key = st.secrets.get("SERPER_API_KEY", os.getenv("SERPER_API_KEY", ""))
    os.environ["SERPER_API_KEY"] = serper_api_key
except:
    serper_api_key = os.getenv("SERPER_API_KEY", "")
    os.environ["SERPER_API_KEY"] = serper_api_key

# Create the search tool using SerperDevTool from crewai_tools
search_internet = SerperDevTool()