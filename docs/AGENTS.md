# Agentic Workforce and Task Definitions

This document details the configuration, psychological profiles, and operational parameters of the AI agents powering the Travel Planner system.

## The Agents

### 1. Destination Analyst
The Destination Analyst is responsible for the initial data infusion layer. It conducts high-fidelity research into logistics, safety, and real-time conditions.
- **Role**: `Senior Destination Research Specialist`
- **Objective**: Deliver a thorough destination briefing covering transportation, accommodation, and safety.
- **Experience**: Expert in transport networks, accommodation tiers, and cost-of-living indices.
- **Tool**: `SerperDevTool` for real-time web retrieval.

### 2. Cultural Concierge
The Concierge synthesizes raw research to identify authentic experiences. It acts as a filter to ensure the final itinerary includes high-value, culturally significant locations rather than just tourist traps.
- **Role**: `Local Culture & Experience Curator`
- **Objective**: Identify interest-driven venues and "hidden gems" based on traveler personas.
- **Experience**: Specialized in local culture, dining trends, and seasonal events.
- **Tool**: `SerperDevTool`.

### 3. Itinerary Architect
The Architect is the final decision layer. It weaves the research logs and curated lists into a cohesive, geolocated, and budget-optimized execution plan.
- **Role**: `Master Travel Itinerary Architect`
- **Objective**: Assemble all data into a polished, time-slotted day-by-day plan.
- **Experience**: Logistics scheduling and geographic grouping.
- **Logic**: Enforces spatiotemporal proximity to minimize travel overhead.

---

## Task Specifications

### I. Destination Intelligence Report
- **Orchestration**: Agent 1 outputs to `city_report.md`.
- **Scope**: Comprehensive briefing on transport hubs, accommodation markets, and practical info (currency, language, safety).

### II. Cultural and Experience Synthesis
- **Orchestration**: Agent 2 outputs to `guide_report.md`.
- **Scope**: Curated venue selection, dining recommendations, and insider tips optimized for cultural immersion.

### III. Strategic Itinerary Execution
- **Orchestration**: Agent 3 outputs to `travel_plan.md`.
- **Scope**: A multi-day blueprint featuring active Google Maps deep-links and a comparative budget matrix.

---

## Orchestration Parameters

| Parameter | Value |
| :--- | :--- |
| **Model Backbone** | `llama-3.3-70b-versatile` (Groq) |
| **Execution Strategy** | `SequentialProcess` (CrewAI) |
| **Determinism** | `temperature=0.2` |
| **Stability Guard** | `max_rpm=3` to adhere to API limits. |
| **Interactive Logic** | URL generation for direct map navigation. |
