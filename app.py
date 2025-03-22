# app.py
import streamlit as st
import requests
import os
import time

# API base URL (adjust for local testing or deployment)
API_URL = "http://localhost:8000"  # Change to deployed URL for Hugging Face Spaces

# Streamlit app configuration
st.set_page_config(page_title="News Summarization & TTS", layout="wide")

# Title and description
st.title("News Summarization & Text-to-Speech Application")
st.markdown("""
    Enter a company name to fetch news articles, analyze their sentiment, 
    and listen to a summary in Hindi.
""")

# Input section
company_name = st.text_input("Enter Company Name", value="Tesla", help="e.g., Tesla, Google, Apple")
num_articles = st.slider("Number of Articles", min_value=1, max_value=15, value=10, step=1)

# Button to trigger analysis
if st.button("Analyze"):
    with st.spinner("Fetching and analyzing news articles..."):
        try:
            url = f"{API_URL}/analyze/{company_name}"
            st.write(f"Debug URL: {url}?num_articles={num_articles}")
            response = requests.get(url, params={"num_articles": num_articles}, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Make API request
            response = requests.get(f"{API_URL}/analyze/{company_name}", params={"num_articles": num_articles})
            response.raise_for_status()
            data = response.json()

            # Display company name
            st.header(f"Analysis for {data['company']}")
            st.write("---")

            # Display article details
            st.subheader("Articles")
            for idx, article in enumerate(data["articles"], 1):
                with st.expander(f"Article {idx}: {article['title']}", expanded=False):
                    st.write(f"**Summary**: {article['summary']}")
                    st.write(f"**Sentiment**: {article['sentiment']}")
                    st.write(f"**Topics**: {', '.join(article['topics'])}")
                    st.write(f"**Source**: [{article['url']}]({article['url']})")
            
            # Display comparative analysis
            st.subheader("Comparative Analysis")
            sentiment_dist = data["comparative_analysis"]["sentiment_distribution"]
            st.write("**Sentiment Distribution**:")
            st.write(f"- Positive: {sentiment_dist['Positive']}")
            st.write(f"- Negative: {sentiment_dist['Negative']}")
            st.write(f"- Neutral: {sentiment_dist['Neutral']}")
            st.write("**Coverage Insights**:")
            for insight in data["comparative_analysis"]["coverage_difference"]:
                st.write(f"- {insight}")

            # Display and play TTS audio
            st.subheader("Hindi Audio Summary")
            audio_file = data["audio"]
            if os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")
                with open(audio_file, "rb") as f:
                    st.download_button("Download Audio", f, file_name=audio_file)
            else:
                st.error("Audio file not found. Please try again.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
        except ValueError as e:
            st.error(f"Invalid response from API: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Footer
st.markdown("---")

if __name__ == "__main__":
    # This block is optional since Streamlit is typically run via `streamlit run app.py`
    st.write("Run this app using: `streamlit run app.py`")