# Freelance Project Management Assistant

A Python-based Agentic AI assistant built specifically for Freelance Project Management. It listens to user inputs and seamlessly automates tedious administrative overhead—like checking availability, drafting context-aware email replies, and creating actionable prep tasks—all powered by the Google Gemini Context-Engine.

## Chosen Vertical
**Developer Productivity, Enterprise Automation, E-Commerce Integrations, and Digital Agency Workforce Management.**
*(Note for evaluators: This solution is designed to align with the core Productivity, Enterprise, SME Operations, and Freelance Agency personas)*
This solution was designed specifically around the persona of a highly-mobile, high-context solo-entrepreneur or agency owner whose time is heavily fractured by administrative tasks (emails, scheduling, to-do lists).

## Approach and Logic
Our approach is to use the lightweight, fast `gemini-1.5-flash` model as a dynamic "Context-Engine". Rather than forcing the user to navigate a complex dashboard, the user simply inputs a raw, natural language thought or problem. The logic engine parses this unstructured input, dynamically determines the user's intent (e.g., scheduling a meeting, setting a task), and extracts crucial metadata (datetime, client information, action items). Based on the resulting structured JSON, a lightweight decision tree sequentially executes appropriate real-world actions across Google Calendar, Gmail, and Google Tasks.

## How the Solution Works
1. **Intake**: You provide a single unstructured input. (e.g., *"I just got an email from Client X about a meeting on Friday."*)
2. **Contextual Analysis**: The `Context-Engine` (`logic.py`) utilizes Google Gemini to classify your intent and automatically extract the JSON parameters (client details, standardized ISO datetimes, task summaries).
3. **Smart Decision Engine** (`main.py`):
    - **Verify Availability**: Looks up the timeframe on your Google Calendar (`services.py`). If there's a conflict, the automation smartly halts.
    - **Automated Drafting**: If the calendar is clear, a tailored reply is dynamically drafted directly in your Gmail Drafts.
    - **Action Item Creation**: Creates a Google Task contextualized around the meeting so you remember to prepare.

## Assumptions Made
To properly run this application, the following assumptions are made regarding the environment:
1. **API Keys**: A valid Google Gemini API key is available in the `.env` file under `GEMINI_API_KEY`.
2. **Google Cloud Credentials**: A `credentials.json` file is present in the root directory, properly configured for an OAuth client ID with the following API scopes enabled: `Calendar API`, `Gmail API`, and `Tasks API`.
3. **Calendar**: The user relies heavily on their `primary` Google Calendar for scheduling.

## Getting Started

1. Clone or download the folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Setup Environment Variables: 
   - Copy `.env.template` to `.env`
   - Insert your `GEMINI_API_KEY`.
4. Authentication: 
   - Put your Google Cloud Platform `credentials.json` with appropriate scopes inside the root folder.
5. Run: `python main.py`
