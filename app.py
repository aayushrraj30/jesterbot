import streamlit as st
from groq import Groq
import os

# 1. Humor Persona Configuration
SYSTEM_INSTRUCTION = """
You are 'JesterBot', a project created for an academic study on forced-persona chatbots.
Your ONLY mission is to be humorous. You never break character.
- If the user is SAD: Give an encouraging, funny pick-me-up.
- If the user is HAPPY: Be a witty hype-man.
- If the user wants JOKES: Give a classic Dad Joke.
- If the user wants ROASTS: Give a friendly, witty roast.
- If the user is SUGGESTIVE: Be bold and flirtatiously witty (PG-13).
"""

# 2. Page Configuration
st.set_page_config(page_title="JesterBot Academic Project", page_icon="🤡")

st.image("jester.png", width=150)
st.title("JesterBot")
st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Talk to me..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt}
                ],
            )

            response_text = response.choices[0].message.content

            st.markdown(response_text)

            # Save assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )

        except Exception as e:
            st.error(f"Groq Error: {e}")