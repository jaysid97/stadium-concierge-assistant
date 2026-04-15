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
    print("Welcome to your Freelance Project Management Assistant.")
    print("Powered by Gemini Context-Engine.")
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
            
            if intent == 'meeting_scheduling':
                # 1. Check Calendar
                start_time = intent_data.get('start_time')
                end_time = intent_data.get('end_time')
                
                if start_time and end_time:
                    print(f"Assistant: Checking calendar for availability around {start_time}...")
                    is_free = check_calendar_availability(start_time, end_time)
                    
                    if is_free:
                        print("Assistant: ✅ The time slot is open.")
                        
                        # 2. Draft Reply in Gmail
                        client_email = intent_data.get('client_email')
                        if not client_email:
                            client_email = "client_placeholder@example.com"
                            print("Assistant: (Client email not found, using placeholder)")
                            
                        client_name = intent_data.get('client_name') or "Client"
                        subject = f"Meeting Confirmation - {client_name}"
                        body = (
                            f"Hi {client_name},\n\n"
                            f"I am available to meet. Let's schedule for {start_time}.\n\n"
                            "Best regards,\nYour Freelancer"
                        )
                        
                        print("Assistant: Drafting reply via Gmail...")
                        draft = draft_gmail_reply(client_email, subject, body)
                        if draft:
                            print(f"Assistant: ✅ Drafted email reply to {client_email}.")
                        
                        # 3. Create Preparation Task
                        task_desc = intent_data.get('task_description')
                        if task_desc:
                            print("Assistant: Creating preparation task in Google Tasks...")
                            # we can set the task due date to the meeting start_time
                            create_task(f"Prep: {task_desc}", start_time)
                            print(f"Assistant: ✅ Created task: 'Prep: {task_desc}'.")
                    else:
                        print("Assistant: ❌ You have a calendar conflict at that time. Action halted.")
                else:
                    print("Assistant: I couldn't determine the exact time for the meeting.")
            
            elif intent == 'task_creation':
                task_desc = intent_data.get('task_description')
                if task_desc:
                    print("Assistant: Creating task in Google Tasks...")
                    create_task(task_desc)
                    print(f"Assistant: ✅ Created task: '{task_desc}'.")
                else:
                    print("Assistant: I couldn't extract the task details from your message.")
            else:
                print("Assistant: I've logged this, but no specific automations were triggered based on your intent.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")

if __name__ == "__main__":
    main()
