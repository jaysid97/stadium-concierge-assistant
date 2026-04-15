import os
import json
import logging
from google import genai
from google.genai import types
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def process_user_intent(user_input: str) -> Optional[Dict[str, Any]]:
    """
    Uses the Context-Engine (powered by Gemini) to analyze user intent and extract actionable data.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please update your .env file.")
            
        client = genai.Client(api_key=api_key)
        
        system_prompt = f"""
        You are a Context-Engine for a Freelance Project Management Assistant.
        Your goal is to parse user inputs and determine what automations need to fire.
        
        The current date and time is {datetime.now().isoformat()}.
        
        You must respond exclusively with a valid JSON object matching this exact structure:
        {{
            "intent": "meeting_scheduling" | "task_creation" | "other",
            "client_name": "Extracted name of the client if present, else null",
            "client_email": "Extracted email if present, else null",
            "start_time": "ISO 8601 format for proposed start (guess year based on current time), else null",
            "end_time": "ISO 8601 format for proposed end (default 1 hour after start if not specified), else null",
            "task_description": "A summarized task description for preparation/action item, else null"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"{system_prompt}\n\nUser Input: {user_input}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        parsed_data = json.loads(response.text)
        return parsed_data
    except Exception as e:
        logger.error(f"Failed to process intent with Gemini: {e}")
        return None
