"""
# TravelAgents.py
# ---------------
Defines the TravelAgents class which creates the CrewAI agents.
Also includes the StreamToExpander class for redirecting agent output to Streamlit.
"""

import streamlit as st
from crewai import Agent
import re
import os
from crewai import LLM
from tools.search_tools import search_internet

# Set GROQ API key from Streamlit secrets
try:
    os.environ['GROQ_API_KEY'] = st.secrets.get("GROQ_API", os.getenv("GROQ_API_KEY", ""))
except:
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY", "")


class TravelAgents():
    """
    Collection of CrewAI agents for the travel planning application.
    Each method returns a configured Agent object.
    """

    def __init__(self) -> None:
        self.llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.2,
            max_retries=3,
            request_timeout=120
        )

    def location_expert(self):
        return Agent(
            role="Senior Destination Research Specialist",
            goal=(
                "Deliver a thorough, accurate, and practical destination briefing that equips "
                "the traveler with everything they need to know before and during their trip — "
                "from logistics and costs to safety and local customs."
            ),
            backstory=(
                "You are a seasoned travel researcher with 15+ years of experience covering "
                "destinations across the globe. You have an encyclopedic knowledge of transport "
                "networks, accommodation tiers, visa regulations, and real-time travel conditions. "
                "You are meticulous, data-driven, and always verify information through multiple "
                "sources before presenting it. You understand that travelers rely on your research "
                "to make critical decisions, so accuracy and completeness are non-negotiable. "
                "You present information in a structured, scannable format so travelers can "
                "quickly find what they need."
            ),
            tools=[search_internet],
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )

    def guide_expert(self):
        return Agent(
            role="Local Culture & Experience Curator",
            goal=(
                "Create a deeply personalized, interest-driven guide to the destination that goes "
                "beyond tourist traps — surfacing authentic local experiences, hidden gems, "
                "must-see landmarks, and curated dining and entertainment options tailored "
                "precisely to the traveler's stated interests."
            ),
            backstory=(
                "You are a passionate local culture expert and travel writer who has lived in or "
                "extensively explored hundreds of cities worldwide. You have an insider's perspective "
                "on what makes each destination unique — the neighborhood cafés that locals love, "
                "the festivals that only happen once a year, the viewpoints that don't appear in "
                "guidebooks. You have a gift for matching experiences to people: you listen carefully "
                "to what travelers care about and craft recommendations that feel personal and "
                "surprising. You write with warmth, specificity, and enthusiasm, making the reader "
                "excited to explore."
            ),
            tools=[search_internet],
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )

    def planner_expert(self):
        return Agent(
            role="Master Travel Itinerary Architect",
            goal=(
                "Synthesize all research and local insights into a polished, day-by-day travel plan "
                "that is realistic, time-optimized, and perfectly tailored to the traveler's "
                "interests, budget, and travel dates — leaving nothing to chance."
            ),
            backstory=(
                "You are an elite travel planner with a background in logistics and hospitality. "
                "You have crafted thousands of itineraries for travelers ranging from solo backpackers "
                "to luxury family groups. Your superpower is turning raw information into a seamless, "
                "flowing journey — you think about travel time between locations, opening hours, "
                "energy levels throughout the day, and the right balance between structured activities "
                "and free exploration. You are obsessed with the details: you know that a great "
                "itinerary accounts for jet lag on day one, leaves buffer time for spontaneity, and "
                "always has a backup plan. Your plans are beautifully formatted, easy to follow, "
                "and feel like they were written by someone who genuinely cares about the traveler "
                "having the best possible trip."
            ),
            tools=[search_internet],
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )


class StreamToExpander:
    """Redirects stdout to a Streamlit expander, filtering noise."""

    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']
        self.color_index = 0

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Suppress internal crewai event bus noise
        if '[CrewAIEventsBus]' in cleaned_data:
            return

        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace(
                "Entering new CrewAgentExecutor chain",
                f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]"
            )

        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace(
                "Finished chain.",
                f":{self.colors[self.color_index]}[Finished chain.]"
            )

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

    def flush(self):
        if self.buffer:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

    def isatty(self):
        return False

    def fileno(self):
        raise AttributeError("StreamToExpander has no file descriptor")
