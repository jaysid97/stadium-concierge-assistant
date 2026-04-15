import os
import logging
from dotenv import load_dotenv
from logic import process_user_intent
from services import check_calendar_availability, draft_gmail_reply, create_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main() -> None:
    # Load environment variables
    load_dotenv()
    
    print("=" * 60)
    print("Welcome to your Stadium Concierge Assistant.")
    print("Powered by Gemini Context-Engine for Event Coordination.")
    print("Type 'exit' or 'quit' to close the assistant.")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("System: Processing your input with Gemini Context-Engine...")
            intent_data = process_user_intent(user_input)
            
            if not intent_data:
                print("Assistant: Sorry, I couldn't understand that request or a service failed.")
                continue
                
            intent = intent_data.get('intent')
            print(f"Assistant: Understood intent -> {intent.upper()}")
            
            if intent == 'event_coordination' or intent == 'event_scheduling':
                # 1. Check Calendar
                start_time = intent_data.get('start_time')
                end_time = intent_data.get('end_time')
                
                if start_time and end_time:
                    print(f"Assistant: Checking venue availability schedule around {start_time}...")
                    is_free = check_calendar_availability(start_time, end_time)
                    
                    if is_free:
                        print("Assistant: ✅ The time slot is open and scheduled.")
                        
                        # 3. Create Preparation Task
                        task_desc = intent_data.get('task_description') or "Coordinate venue event"
                        print("Assistant: Creating real-time coordination task...")
                        create_task(f"Coordinate: {task_desc}", start_time)
                        print(f"Assistant: ✅ Created task: 'Coordinate: {task_desc}'.")
                    else:
                        print("Assistant: ❌ You have a timing conflict at that time. Action halted.")
                else:
                    print("Assistant: I couldn't determine the exact time for the coordination.")
                    
            elif intent == 'stadium_support':
                target_location = intent_data.get('target_location') or "Unknown Location"
                support_issue = intent_data.get('support_issue') or "General Assistance needed"
                
                print("Assistant: Drafting support ticket to Stadium Staff via Gmail...")
                subject = f"Stadium Support Needed - {target_location}"
                body = (
                    f"Attention Stadium Operations,\n\n"
                    f"An attendee has reported the following issue at {target_location}:\n"
                    f"{support_issue}\n\n"
                    "Automated via Stadium Concierge"
                )
                draft = draft_gmail_reply("stadium_ops_placeholder@example.com", subject, body)
                if draft:
                    print(f"Assistant: ✅ Drafted support email to stadium operations.")

            elif intent == 'attendance_reminder' or intent == 'task_creation':
                task_desc = intent_data.get('task_description')
                if task_desc:
                    print("Assistant: Creating crowd-movement reminder in Google Tasks...")
                    create_task(task_desc)
                    print(f"Assistant: ✅ Created task: '{task_desc}'.")
                else:
                    print("Assistant: I couldn't extract the reminder details from your message.")
            else:
                print("Assistant: I've logged this stadium update, but no specific automations were triggered.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")

if __name__ == "__main__":
    main()
