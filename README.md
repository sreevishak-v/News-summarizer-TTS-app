
# News Summarization & Text-to-Speech Application 📰 

## Overview
This project is a two-part application designed to fetch, summarize, and analyze news articles for a given company, then provide a Hindi audio summary using text-to-speech (TTS). It consists of:
- News-Summarizer-API: A FastAPI backend that handles news fetching, summarization, sentiment analysis, and TTS generation.
- News-Summarizer-Frontend: A Streamlit frontend offering a user-friendly interface to interact with the API.

Deployed on Hugging Face Spaces:
- API: https://sreevishak-news-summarizer-api.hf.space
- Frontend: https://sreevishak-news-summarizer-frontend.hf.space

## Features 
- Fetch recent news articles for any company using NewsAPI.
- Summarize articles into concise excerpts.
- Analyze sentiment (Positive, Negative, Neutral) using NLTK’s VADER.
- Extract key topics from summaries.
- Generate Hindi audio summaries with gTTS.
- Interactive web interface with audio playback and download.

## Project Setup
Prerequisites

- Python 3.9+
- Git
- Docker (optional for local containerized setup)
- A NewsAPI key (free tier available)
- Hugging Face account (for deployment)

### Backend (News-Summarizer-API)
Local Setup
#### 1.Clone the Repository:
 
 ```bash
  git clone https:// face.co/spaces/sreevishak/ News-Summarizer-API
  cd News-Summarizer-API
```
#### 2.Install Dependencies:
 ```bash
  python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
#### 3.Download NLTK Data:
 ```bash
  python -m nltk.downloader -d ./nltk_data punkt punkt_tab stopwords vader_lexicon
```
#### 4.Set Environment Variable:
 ```bash
  export NEWSAPI_KEY="your_newsapi_key_here"  # On Windows: set NEWSAPI_KEY=your_newsapi_key_here
```
#### 5.Run the API::
 ```bash
  uvicorn api:app --host 0.0.0.0 --port 7860 --reload
```
- Access at http://localhost:7860/health to verify.
#### Hugging Face Deployment

- Push the repository to your Hugging Face Space.
- Add NEWSAPI_KEY to Repository Secrets (Settings > Repository Secrets).
- The Dockerfile automatically builds and runs the app.

### Frontend (News-Summarizer-Frontend)
###### Local Setup

#### 1.Clone the Repository:
 ```bash
  git clone https://huggingface.co/spaces/sreevishak/News-Summarizer-Frontend
cd News-Summarizer-Frontend
```
#### 2.Install Dependencies:
 ```bash
  git clone https://huggingface.co/spaces/sreevishak/News-Summarizer-Frontend
cd News-Summarizer-Frontend
```
#### .3.Run the Frontend:
 ```bash
  streamlit run app.py
```
Access at http://localhost:8501.
Hugging Face Deployment
- Push the repository to your Hugging Face Space.
- Ensure API_URL in app.py is set to https://sreevishak-news-summarizer-api.hf.space.

### project structure
- Backend
```bash
News-Summarizer-API/
├── api.py                 # FastAPI app with endpoints
├── utils.py               # Functions for news fetching, summarization, etc.
├── requirements.txt       # Dependencies (fastapi, uvicorn, nltk, etc.)
├── Dockerfile             # Container configuration
└── nltk_data/             # NLTK resources 
```
- Frontend
```bash
News-Summarizer-API/
├── app.py                 # Streamlit app
├── requirements.txt       #  Dependencies (streamlit, requests) etc.
```


### Technologies Used

#### Backend
- FastAPI: API framework.
- NewsAPI: News article source.
- NLTK: Summarization (custom), sentiment analysis (VADER), topic extraction.
- gTTS: Hindi text-to-speech.
- deep_translator: English-to-Hindi translation.

#### Frontend
- Streamlit: Web interface.
- Requests: API communication.


###  Assumptions & Limitations

#### Assumptions
- NewsAPI provides sufficient articles for queried companies.
- Internet connectivity is available for all third-party services.
- Users understand Hindi for TTS output.
#### Limitations
- Summarization is extractive (first 2 sentences), potentially missing key - details.
- Topic extraction is keyword-based, lacking deeper context.
- Free NewsAPI tier limits requests to 100/day.
- Hindi-only TTS; no multi-language support.
- Dependent on third-party API availability (NewsAPI, Google services).




### Acknowledgments
- NewsAPI for news data.
- NLTK for NLP tools.
- gTTS for text-to-speech.
- Hugging Face Spaces for hosting.
