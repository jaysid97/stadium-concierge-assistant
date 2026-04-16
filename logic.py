import os
import json
import logging
from google import genai
from google.genai import types
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    """Security Function: Sanitize input to prevent prompt injection and limit payload size."""
    if not text:
        return ""
    clean_text = text.strip()[:1000]
    return clean_text.replace("System:", "").replace("Instruction:", "")

def process_user_intent(user_input: str) -> Optional[Dict[str, Any]]:
    """
    Uses the Context-Engine (powered by Gemini) to analyze user intent and extract actionable data.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please update your .env file.")
            
        client = genai.Client(api_key=api_key)
        
        clean_input = sanitize_input(user_input)
        if not clean_input:
            logger.warning("Security: Empty or invalid input provided.")
            return None
            
        system_prompt = f"""
        You are a Context-Engine for a Stadium Concierge Assistant at a large-scale sporting venue.
        Your goal is to parse user inputs regarding crowd movement, waiting times, or real-time coordination and determine what automations need to fire.
        
        The current date and time is {datetime.now().isoformat()}.
        
        You must respond exclusively with a valid JSON object matching this exact structure:
        {{
            "intent": "event_coordination" | "stadium_support" | "attendance_reminder" | "other",
            "target_location": "Extracted location or section in the stadium if present, else null",
            "support_issue": "Extracted problem or coordination issue if present, else null",
            "start_time": "ISO 8601 format for proposed time (guess year based on current time), else null",
            "end_time": "ISO 8601 format for proposed end (default 1 hour after start if not specified), else null",
            "task_description": "A summarized task description for a reminder or action item, else null"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\nUser Input: {clean_input}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        parsed_data = json.loads(response.text)
        return parsed_data
    except Exception as e:
        logger.error(f"Failed to process intent with Gemini: {e}")
        return {"error": f"Failed to process intent with Gemini: {e}"}
