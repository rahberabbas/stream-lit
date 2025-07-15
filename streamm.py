import streamlit as st
import requests

# API endpoint for tag analysis
API_URL = "https://together-cleanly-sponge.ngrok-free.app/analyze"

st.title("Review Tag Analyzer 🏷️")
st.write("Enter a review to generate tags, sentiment, and confidence score.")

# Track last input to avoid duplicate requests
if "last_review" not in st.session_state:
    st.session_state.last_review = ""

# Input field for the review
user_review = st.text_input("Enter your review:", key="review_input")

# If review changes, call the API
if user_review.strip() != "" and user_review != st.session_state.last_review:
    st.session_state.last_review = user_review
    with st.spinner("Analyzing review..."):
        try:
            response = requests.post(API_URL, json={"review": user_review})
            response.raise_for_status()
            result = response.json()

            # Extracted values from response
            tags = result.get("tags", [])
            sentiment = result.get("sentiment", "unknown").capitalize()
            accuracy = result.get("accuracy", 0.0)

            st.markdown(f"**Sentiment:** `{sentiment}`")
            st.markdown(f"**Confidence:** `{accuracy:.2f}`")

            if tags and tags != ["no tag"]:
                st.success("Tags identified:")
                for tag in tags:
                    st.markdown(f"- ✅ **{tag}**")
            else:
                st.info("No specific tags found for this review.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")
