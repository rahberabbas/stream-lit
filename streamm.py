import streamlit as st
import requests

# API_URL = "http://localhost:8001/query"

API_URL = "https://together-cleanly-sponge.ngrok-free.app/query"

st.title("Natural's Q&A Bot 🧠💬")
st.write("Ask a question and get an intelligent response!")

# Session state to prevent re-running multiple times
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# Text input (auto submits on Enter)
user_question = st.text_input("Enter your question:", key="question_input")

# Trigger when Enter is pressed (text input changes)
if user_question.strip() != "" and user_question != st.session_state.last_question:
    st.session_state.last_question = user_question  # Save to session to avoid re-submission
    with st.spinner("Thinking... 🤔"):
        try:
            response = requests.post(API_URL, json={"question": user_question})
            response.raise_for_status()

            data = response.json()
            st.success("Answer Received!")
            st.markdown(f"**Answer:** {data.get('answer')}")
            # st.markdown(f"**Category:** {data.get('category')}")  # Optional
            # st.markdown(f"**Matched Question:** {data.get('matched_question')}")  # Optional
            # st.markdown(f"**Confidence:** {round(data.get('confidence', 0) * 100, 2)}%")  # Optional

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")
