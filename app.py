# app.py
import streamlit as st
import requests
import time

# API base URL
API_URL = "https://sreevishak-news-summarizer-api.hf.space"  # Correct API endpoint

# Streamlit app configuration
st.set_page_config(page_title="News Summarization & TTS", layout="wide")

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
            # Make API request
            url = f"{API_URL}/analyze/{company_name}"
            response = requests.get(url, params={"num_articles": num_articles}, timeout=30)
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

            # Fetch and play TTS audio
            st.subheader("Hindi Audio Summary")
            audio_url = f"{API_URL}{data['audio']}"
            audio_response = requests.get(audio_url, timeout=10)
            if audio_response.status_code == 200:
                st.audio(audio_response.content, format="audio/mp3")
                st.download_button(
                    "Download Audio",
                    audio_response.content,
                    file_name=f"audio_{company_name}.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error(f"Failed to fetch audio: {audio_response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
        except ValueError as e:
            st.error(f"Invalid response from API: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Footer
st.markdown("---")

if __name__ == "__main__":
    st.write("Run this app using: `streamlit run app.py`")
