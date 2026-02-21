"""
TravelTasks.py
--------------
Defines the TravelTasks class which creates the CrewAI tasks.
Each method returns a configured Task object with detailed prompts.
"""

from crewai import Task


class TravelTasks():
    """
    Collection of CrewAI tasks for the travel planning application.
    Each method returns a configured Task object.
    """

    # Task 1: Destination Research
    def location_task(self, agent, from_city, destination_city, date_from, date_to):
        return Task(
            description=f"""
You are researching {destination_city} for a traveler departing from {from_city}.
Travel window: {date_from} to {date_to}.

Search for and compile the following information:

1. **Getting There**
   - Best transport options from {from_city} to {destination_city} (flight, train, bus, car)
   - Estimated travel time and approximate cost for each option
   - Recommended booking platforms or tips

2. **Accommodation**
   - 2–3 budget options (with approximate price per night in INR or local currency)
   - 2–3 mid-range options
   - 1–2 premium/boutique options
   - Key neighborhoods to stay in and why

3. **Cost of Living & Daily Budget**
   - Average daily spend for budget / mid-range / comfort traveler
   - Typical meal costs (street food, local restaurant, upscale)
   - Local transport costs (auto, taxi, metro if available)

4. **Weather During Travel Dates**
   - Expected temperature range for {date_from} to {date_to}
   - Any weather advisories or seasonal considerations
   - What to pack

5. **Practical Info**
   - Local currency and payment norms (cash vs card)
   - Language spoken and useful local phrases
   - Safety tips and areas to avoid
   - Emergency contacts (police, hospital, tourist helpline)

6. **Events & Festivals**
   - Any festivals, cultural events, or local happenings during {date_from} to {date_to}

> **IMPORTANT**: For every specific place, hotel, restaurant, or landmark you mention,
> append a Google Maps link in this exact format:
> `[📍 View on Maps](https://www.google.com/maps/search/?api=1&query=PLACE+NAME+{destination_city})`
> Replace spaces with `+` in the URL.
""",
            expected_output="""
A well-structured markdown report with clear headings for each section above.
Use tables where appropriate (e.g., accommodation options, transport comparison).
Be specific — include real names, real price ranges, and actionable advice.
Avoid generic filler. Every sentence should add value to the traveler.
""",
            agent=agent,
            output_file='city_report.md',
        )

    # Task 2: Local Guide
    def guide_task(self, agent, destination_city, interests, date_from, date_to):
        return Task(
            description=f"""
You are creating a personalized local guide for {destination_city}, tailored to a traveler
whose interests are: **{interests}**.
Travel dates: {date_from} to {date_to}.

Research and curate the following:

1. **Top Attractions Aligned with Interests**
   - For each interest in "{interests}", find 3–5 specific places, experiences, or activities
   - Include name, why it's relevant to the interest, location, opening hours, entry fees
   - Mix iconic landmarks with lesser-known local favorites

2. **Food & Dining**
   - 3–5 must-try local dishes or food experiences in {destination_city}
   - Specific restaurant or street food stall recommendations (name, area, price range)
   - Any food markets, food streets, or culinary experiences worth visiting

3. **Hidden Gems & Local Tips**
   - 2–3 places or experiences that most tourists miss but locals love
   - Best time of day to visit key attractions (to avoid crowds or catch best light)
   - Any insider tips specific to {destination_city}

4. **Shopping & Souvenirs**
   - What {destination_city} is famous for buying
   - Best markets or shopping areas
   - Price negotiation tips if applicable

5. **Day Trips (if applicable)**
   - 1–2 nearby destinations worth a half-day or full-day trip from {destination_city}

> **IMPORTANT**: For every specific place, attraction, restaurant, or market you mention,
> append a Google Maps link in this exact format:
> `[📍 View on Maps](https://www.google.com/maps/search/?api=1&query=PLACE+NAME+{destination_city})`
> Replace spaces with `+` in the URL.
""",
            expected_output="""
A rich, engaging markdown guide with emojis on section headers.
Write in a warm, enthusiastic tone — make the traveler excited to explore.
Be specific: real place names, real addresses or areas, real prices where possible.
Organize clearly so the traveler can use this as a reference during their trip.
""",
            agent=agent,
            output_file='guide_report.md',
        )

    # Task 3: Day-by-Day Itinerary
    def planner_task(self, context, agent, destination_city, interests, date_from, date_to):
        return Task(
            description=f"""
Using the destination research and local guide provided by your colleagues, create a complete,
day-by-day travel itinerary for {destination_city}.

Traveler profile:
- Interests: {interests}
- Arrival: {date_from}
- Departure: {date_to}

Build the itinerary with these principles:

1. **Day-by-Day Structure**
   - Create a separate plan for each day from {date_from} to {date_to}
   - Each day should have a Morning / Afternoon / Evening breakdown with specific times
   - Include travel time between locations
   - Balance activity-heavy periods with rest or leisure time

2. **Smart Scheduling**
   - Day 1: Keep it light — account for arrival fatigue. Focus on nearby, easy experiences
   - Middle days: Pack in the highlights and interest-specific activities
   - Last day: Wind down, shopping, and departure prep
   - Respect opening hours — don't schedule visits to closed attractions

3. **No Repetition Rule** *(strictly enforced)*
   - Each specific location, attraction, restaurant, or place must appear **at most once** across the entire itinerary
   - Do NOT revisit or re-suggest the same place on different days under any circumstances
   - Every day must feature completely different locations from every other day
   - If you run out of major attractions, suggest nearby neighborhoods, local markets, parks, or day-trip spots — but never repeat

3. **Practical Details for Each Activity**
   - Name of place + brief description (1–2 sentences)
   - Estimated time to spend there
   - How to get there from previous location
   - Estimated cost

4. **Meals**
   - Suggest specific breakfast, lunch, and dinner spots for each day
   - Vary the dining experiences across the trip

5. **Budget Summary**
   - End with a rough total trip cost breakdown (transport, accommodation, food, activities)
   - Provide budget / mid-range / comfort estimates

> **IMPORTANT**: For every specific place, restaurant, attraction, or landmark in the itinerary,
> append a Google Maps link in this exact format:
> `[📍 Maps](https://www.google.com/maps/search/?api=1&query=PLACE+NAME+{destination_city})`
> Replace spaces with `+` in the URL. Include this for every single location mentioned.
""",
            expected_output=f"""
A beautifully formatted markdown travel plan with the following structure:

# 🌏 Welcome to {destination_city}
[3–4 paragraph introduction to the city — its character, vibe, what makes it special]

---

# 🗓️ Your {destination_city} Itinerary

## Day 1 — [Date] · Arrival & First Impressions
### 🌅 Morning (9:00 AM – 12:00 PM)
...
### ☀️ Afternoon (12:00 PM – 5:00 PM)
...
### 🌙 Evening (5:00 PM – 9:00 PM)
...

[Repeat for each day]

---

# 💰 Budget Overview
| Category | Budget | Mid-Range | Comfort |
|----------|--------|-----------|---------|
| ...      | ...    | ...       | ...     |

Use emojis on every section header. Write in a friendly, confident tone.
Every activity should feel purposeful and connected to the traveler's interests.
""",
            context=context,
            agent=agent,
            output_file='travel_plan.md',
        )
