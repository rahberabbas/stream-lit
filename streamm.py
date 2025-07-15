import streamlit as st
import requests

# API endpoint for tag analysis
API_URL = "https://together-cleanly-sponge.ngrok-free.app/analyze"

st.title("Review Tag Analyzer 🏷️")
st.write("Enter a review to generate tags with sentiment and color coding.")

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
            tags = response.json()

            if tags:
                st.success("Tags generated:")
                for tag in tags:
                    st.markdown(
                        f"<div style='background-color:{tag['color_hex']};"
                        f"padding: 8px; border-radius: 5px; margin-bottom: 5px;'>"
                        f"<strong>{tag['tag']}</strong> - {tag['sentiment'].capitalize()}</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No relevant tags were generated for this review.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")
