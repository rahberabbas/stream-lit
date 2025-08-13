import streamlit as st
import requests

API_URL = "http://103.189.173.28:8001/california/analyze"

st.title("Review Tag Analyzer 🏷️")
st.write("Enter a review to generate tags, sentiment, and confidence score.")

if "last_review" not in st.session_state:
    st.session_state.last_review = ""

user_review = st.text_input("Enter your review:", key="review_input")
service_type = st.selectbox("Select service type:", ["dining", "delivery"])

if user_review.strip() != "" and user_review != st.session_state.last_review:
    st.session_state.last_review = user_review
    with st.spinner("Analyzing review..."):
        try:
            response = requests.post(API_URL, json={
                "review_text": user_review,
                "service_type": service_type
            })
            response.raise_for_status()
            result = response.json()

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

            with st.expander("Show raw API response"):
                st.json(result)

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")
