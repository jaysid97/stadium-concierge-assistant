import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import Optional, Any, Dict

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/tasks'
]

logger = logging.getLogger(__name__)

def get_credentials() -> Optional[Credentials]:
    """Handles Google OAuth2 authentication."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def check_calendar_availability(start_time: str, end_time: str) -> bool:
    """Checks if the given time slot is free on Google Calendar."""
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)
        
        events_result = service.events().list(
            calendarId='primary', timeMin=start_time, timeMax=end_time,
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        # If events list is empty, the calendar is free
        return len(events) == 0
    except Exception as e:
        logger.error(f"Error checking calendar: {e}")
        return False

def draft_gmail_reply(to_email: str, subject: str, body: str) -> Optional[Dict[str, Any]]:
    """Drafts a reply in Gmail."""
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        
        from email.message import EmailMessage
        import base64
        
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_email
        message['Subject'] = subject
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        logger.info(f"Draft created successfully. Draft ID: {draft['id']}")
        return draft
    except Exception as e:
        logger.error(f"Error drafting email: {e}")
        return None

def create_task(title: str, due_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Creates an actionable item in Google Tasks."""
    try:
        creds = get_credentials()
        service = build('tasks', 'v1', credentials=creds)
        
        task = {
            'title': title
        }
        if due_date:
            task['due'] = due_date
            
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        logger.info(f"Task created successfully. Task ID: {result['id']}")
        return result
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return None
