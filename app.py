import streamlit as st
from groq import ollama  # Replaced google.generativeai with ollama
import os

# 1. Humor Persona Configuration
# This stays the same to keep your witty character intact
SYSTEM_INSTRUCTION = """
You are 'JesterBot', a project created for an academic study on forced-persona chatbots.
Your ONLY mission is to be humorous. You never break character.
- If the user is SAD: Give an encouraging, funny pick-me-up.
- If the user is HAPPY: Be a witty hype-man.
- If the user wants JOKES: Give a classic Dad Joke.
- If the user wants ROASTS: Give a friendly, witty roast.
- If the user is SUGGESTIVE: Be bold and flirtatiously witty (PG-13).
"""

# 2. Building the Interface (The "Face")
st.set_page_config(page_title="JesterBot Academic Project", page_icon="🤡")

# Display the Jesterbot Avatar
# Ensure 'jester.png' is in the same folder as this script
st.image("jester.png", width=150)
st.title("JesterBot")
st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handling Interaction with Ollama Phi3
if prompt := st.chat_input("Talk to me..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using local Ollama Phi3
    with st.chat_message("assistant"):
        try:
            # We pass the system instruction and user prompt to Phi3
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt}
            ],
            )

            response_text = response.choices[0].message.content
            st.markdown(response_text)
            
            # Save the response to history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ollama Error: {e}")
            st.info("Make sure Ollama is running in the background and 'phi3' is pulled.")