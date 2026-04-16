import streamlit as st
import time
from dotenv import load_dotenv
import os
from logic import process_user_intent

# Load environment logic
load_dotenv()

st.set_page_config(page_title="Stadium Concierge Demo", page_icon="🏟️", layout="centered")

@st.cache_data(ttl=3600)
def cached_process_user_intent(user_input_str):
    """Efficiency: Cache repeated prompts to save API overhead."""
    return process_user_intent(user_input_str)

st.markdown("<h1 aria-label='Stadium Concierge Assistant'>🏟️ Stadium Concierge Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p aria-label='Simulated Live Demo for Hackathon Submission'><em>(Simulated Live Demo for Hackathon Submission - Sporting Venues)</em></p>", unsafe_allow_html=True)
st.write("This interactive demo uses **Gemini 2.5 Flash** to extract context. Unlike the local CLI tool, it safely skips hitting actual Google APIs to keep your personal data secure.")

st.divider()

user_input = st.text_area("How can I help you today? (e.g. 'I need support at section 104 because it is overcrowded' or 'Remind me to get food during halftime at 2 PM')", height=100)

if st.button("Submit to Context-Engine", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Gemini is analyzing your intent..."):
            intent_data = cached_process_user_intent(user_input)
            
        if not intent_data:
            st.error("Failed to process the input. Make sure GEMINI_API_KEY is present in the environment (.env file).")
        elif intent_data.get('error'):
            st.error(intent_data.get('error'))
        else:
            intent = intent_data.get('intent', 'unknown')
            st.success(f"**Intent Recognized:** `{intent.upper()}`")
            
            with st.expander("View Raw JSON Dump from Gemini"):
                st.json(intent_data)
                
            st.markdown("<h3 aria-label='Simulated Automation Workflow'>Simulated Automation Workflow ⚡</h3>", unsafe_allow_html=True)
            
            if intent == 'event_coordination' or intent == 'event_scheduling':
                start_time = intent_data.get('start_time')
                
                # 1. Calendar Simulation
                st.write(f"📅 **Calendar Check:** Verified venue schedule availability around `{start_time}`. Time-slot is clear!")
                time.sleep(0.5)
                
                # 3. Tasks Simulation
                task_desc = intent_data.get('task_description') or "Coordinate venue event"
                if task_desc:
                    time.sleep(0.5)
                    st.write(f"✅ **Google Tasks:** Coordination prep item created: **'Coordinate: {task_desc}'**")
                    
            elif intent == 'stadium_support':
                target_location = intent_data.get('target_location') or "Unknown Location"
                support_issue = intent_data.get('support_issue') or "General Assistance needed"
                
                # 2. Gmail Draft Simulation
                st.write(f"✉️ **Gmail Drafting:** Composing support ticket for Stadium Operations concerning `{target_location}`...")
                time.sleep(1)
                st.info(f"""
                **Drafted Subject**: Stadium Support Needed - {target_location}
                
                **Drafted Body**:
                > Attention Stadium Operations,
                > An attendee has reported the following issue at {target_location}:
                > {support_issue}
                > Automated via Stadium Concierge
                """)

            elif intent == 'attendance_reminder' or intent == 'task_creation':
                task_desc = intent_data.get('task_description')
                if task_desc:
                    st.write(f"✅ **Google Tasks:** Crowd notification or reminder created: **'{task_desc}'**")
                else:
                    st.warning("Could not extract task details from your message.")
            else:
                st.info("I've logged this stadium update, but no specific Google integrations were triggered based on your intent.")
