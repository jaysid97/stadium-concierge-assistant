import streamlit as st
import time
from dotenv import load_dotenv
import os
from logic import process_user_intent

# Load environment logic
load_dotenv()

st.set_page_config(page_title="Freelance Assistant Demo", page_icon="🤖", layout="centered")

@st.cache_data(ttl=3600)
def cached_process_user_intent(user_input_str):
    """Efficiency: Cache repeated prompts to save API overhead."""
    return process_user_intent(user_input_str)

st.markdown("<h1 aria-label='Freelance Project Management Assistant'>🤖 Freelance Project Management Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p aria-label='Simulated Live Demo for Hackathon Submission'><em>(Simulated Live Demo for Hackathon Submission)</em></p>", unsafe_allow_html=True)
st.write("This interactive demo uses **Gemini 2.5 Flash** to extract context. Unlike the local CLI tool, it safely skips hitting actual Google APIs to keep your personal data secure.")

st.divider()

user_input = st.text_area("What's on your mind? (e.g. 'I just got an email from Client X about a meeting on Friday at 2PM')", height=100)

if st.button("Submit to Context-Engine", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Gemini is analyzing your intent..."):
            intent_data = cached_process_user_intent(user_input)
            
        if not intent_data:
            st.error("Failed to process the input. Make sure GEMINI_API_KEY is present in the environment (.env file).")
        else:
            intent = intent_data.get('intent', 'unknown')
            st.success(f"**Intent Recognized:** `{intent.upper()}`")
            
            with st.expander("View Raw JSON Dump from Gemini"):
                st.json(intent_data)
                
            st.markdown("<h3 aria-label='Simulated Automation Workflow'>Simulated Automation Workflow ⚡</h3>", unsafe_allow_html=True)
            
            if intent == 'meeting_scheduling':
                start_time = intent_data.get('start_time')
                end_time = intent_data.get('end_time')
                client_name = intent_data.get('client_name') or "Client"
                
                # 1. Calendar Simulation
                st.write(f"📅 **Calendar Check:** Verified availability around `{start_time}`. Time-slot is clear!")
                time.sleep(0.5)
                
                # 2. Gmail Draft Simulation
                st.write(f"✉️ **Gmail Drafting:** Composing contextual response to `{client_name}`...")
                time.sleep(1)
                st.info(f"""
                **Drafted Subject**: Meeting Confirmation - {client_name}
                
                **Drafted Body**:
                > Hi {client_name},
                > I am available to meet. Let's schedule for {start_time[:10]} if that works for you.
                > Best regards,  
                > Your Freelancer
                """)
                
                # 3. Tasks Simulation
                task_desc = intent_data.get('task_description')
                if task_desc:
                    time.sleep(0.5)
                    st.write(f"✅ **Google Tasks:** Actionable prep item created: **'Prep: {task_desc}'**")
                    
            elif intent == 'task_creation':
                task_desc = intent_data.get('task_description')
                if task_desc:
                    st.write(f"✅ **Google Tasks:** Task created: **'{task_desc}'**")
                else:
                    st.warning("Could not extract task details from your message.")
            else:
                st.info("I've logged this, but no specific Google integrations were triggered based on your intent.")
