"""
TravelCrewApp.py
----------------
Main Streamlit application entry point.
Handles the UI, user input, and orchestration of the CrewAI agents.
"""

import sys
import os

# 1. DOTENV FIXES
# Fix dotenv encoding issue before importing crewai
try:
    import dotenv.parser
    import io
    original_reader_init = dotenv.parser.Reader.__init__
    def safe_reader_init(self, stream):
        try:
            if hasattr(stream, 'read'):
                try:
                    content = stream.read()
                    if isinstance(content, bytes):
                        try:
                            content = content.decode('utf-8')
                        except UnicodeDecodeError:
                            content = ""
                    safe_stream = io.StringIO(content)
                    original_reader_init(self, safe_stream)
                except Exception:
                    self.string = ""
                    self.position = dotenv.parser.Position.start()
                    self.mark = dotenv.parser.Position.start()
            else:
                original_reader_init(self, stream)
        except Exception:
            self.string = ""
            self.position = dotenv.parser.Position.start()
            self.mark = dotenv.parser.Position.start()
    dotenv.parser.Reader.__init__ = safe_reader_init
except Exception:
    pass

try:
    import dotenv.main
    original_load = dotenv.main.load_dotenv
    def safe_load_dotenv(*args, **kwargs):
        try:
            return original_load(*args, **kwargs)
        except Exception:
            return False
    dotenv.main.load_dotenv = safe_load_dotenv
except Exception:
    pass

# 2. IMPORTS & CONFIG
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore", message=".*signal.*")

try:
    from crewai import Crew, Process
except UnicodeDecodeError:
    from crewai import Crew, Process

from TravelAgents import TravelAgents, StreamToExpander
from TravelTasks import TravelTasks

# Page config
st.set_page_config(
    page_icon="🗺️",
    page_title="Travel Planner AI",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hero header */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1.05rem;
    color: #8B8FA8;
    margin-top: 0.4rem;
}
.accent { color: #FF6B35; }

/* Input card */
.input-card {
    background: #1A1D27;
    border: 1px solid #2A2D3E;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
}

/* Section label */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8B8FA8;
    margin-bottom: 0.5rem;
}

/* Trip summary pill */
.trip-summary {
    background: linear-gradient(135deg, #1e2030, #252840);
    border: 1px solid #FF6B3530;
    border-left: 3px solid #FF6B35;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.92rem;
    color: #C8CADB;
    margin: 0.8rem 0 1.2rem;
    line-height: 1.6;
}

/* Result card */
.result-card {
    background: #1A1D27;
    border: 1px solid #2A2D3E;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1000px; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Inputs */
.stTextInput input, .stDateInput input {
    background: #0F1117 !important;
    border: 1px solid #2A2D3E !important;
    border-radius: 8px !important;
    color: #E8EAF0 !important;
}
.stTextInput input:focus, .stDateInput input:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 2px #FF6B3520 !important;
}

/* Divider */
hr { border-color: #2A2D3E !important; }
</style>
""", unsafe_allow_html=True)


# TravelCrew class
class TravelCrew:

    def __init__(self, from_city, destination_city, interests, date_from, date_to):
        self.destination_city = destination_city
        self.from_city = from_city
        self.interests = interests
        self.date_from = date_from
        self.date_to = date_to
        self.output_placeholder = st.empty()

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        location_expert = agents.location_expert()
        guide_expert = agents.guide_expert()
        planner_expert = agents.planner_expert()

        location_task = tasks.location_task(
            location_expert, self.from_city, self.destination_city,
            self.date_from, self.date_to
        )
        guide_task = tasks.guide_task(
            guide_expert, self.destination_city, self.interests,
            self.date_from, self.date_to
        )
        planner_task = tasks.planner_task(
            [location_task, guide_task], planner_expert,
            self.destination_city, self.interests,
            self.date_from, self.date_to,
        )

        crew = Crew(
            agents=[location_expert, guide_expert, planner_expert],
            tasks=[location_task, guide_task, planner_task],
            process=Process.sequential,
            share_crew=False,
            verbose=True,
            max_rpm=3,
        )

        result = crew.kickoff()
        result_str = str(result) if not isinstance(result, str) else result
        self.output_placeholder.markdown(result_str)
        return result_str


# Hero Section
st.markdown("""
<div class="hero">
    <h1>Travel Planner <span class="accent">AI</span></h1>
    <p>3 specialized AI agents craft your perfect itinerary</p>
</div>
""", unsafe_allow_html=True)

# Input Fields
today = datetime.now()
seven_days = today + timedelta(days=7)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        from_city = st.text_input("📍 From", placeholder="e.g. Chennai, Tamil Nadu")
    with col2:
        destination_city = st.text_input("🏝️ Destination", placeholder="e.g. Madurai, Tamil Nadu")

    INTEREST_OPTIONS = [
        "🏛️ Culture & History",
        "🍜 Food & Cuisine",
        "🛍️ Shopping",
        "🏔️ Nature & Hiking",
        "🎭 Nightlife & Entertainment",
        "🏖️ Beach & Relaxation",
        "📸 Photography & Sightseeing",
        "🧘 Wellness & Spa",
        "⚽ Sports & Adventure",
        "Other",
    ]
    selected = st.multiselect(
        "🎯 Interests",
        INTEREST_OPTIONS,
        placeholder="Pick your travel interests…",
    )
    custom_interest = ""
    if "Other" in selected:
        custom_interest = st.text_input(
            "Custom interest",
            placeholder="e.g. Anime spots, Jazz clubs, Architecture…",
            label_visibility="collapsed",
        )
    # Build final interests string (strip emoji prefixes for the agents)
    clean = [s.split(" ", 1)[-1] if s != "Other" else custom_interest for s in selected]
    interests = ", ".join([c for c in clean if c])

    col3, col4 = st.columns(2)
    with col3:
        date_from = st.date_input("🗓️ Departure", today, format="DD/MM/YYYY")
    with col4:
        date_to = st.date_input("🗓️ Return", seven_days, format="DD/MM/YYYY")

# Trip summary and Generate logic
all_filled = from_city and destination_city and interests and date_from and date_to

if all_filled:
    travel_period = (date_to - date_from).days
    st.markdown(f"""
    <div class="trip-summary">
        <strong>{from_city}</strong> → <strong style="color:#FF6B35">{destination_city}</strong>
        &nbsp;·&nbsp; {travel_period} days
        &nbsp;·&nbsp; {date_from.strftime("%d %b")} – {date_to.strftime("%d %b %Y")}
        &nbsp;·&nbsp; {interests}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate My Travel Plan ✨"):
        try:
            with st.status("🤖 Agents at work…", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    sys.stdout = StreamToExpander(st)
                    travel_crew = TravelCrew(
                        from_city, destination_city, interests, date_from, date_to
                    )
                    result = travel_crew.run()
                status.update(label="✅ Your plan is ready!", state="complete", expanded=False)

            st.markdown("---")
            st.markdown("### 🗺️ Your Itinerary")
            st.markdown(result)

        except Exception as e:
            sys.stdout = sys.__stdout__
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "ratelimit" in error_msg.lower():
                st.warning(
                    "⏳ **Rate limit hit** (after auto-retries).\n\n"
                    "Groq's free tier allows 6,000 tokens/min. "
                    "Wait a minute and try again, or [upgrade here](https://console.groq.com/settings/billing)."
                )
            else:
                st.error(f"❌ Something went wrong: {error_msg}")
