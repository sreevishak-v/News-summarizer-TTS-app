# utils.py
import nltk
nltk.data.path.append('/app/nltk_data')
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from gtts import gTTS
import os
import requests
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

STOP_WORDS = set(stopwords.words('english'))
sid = SentimentIntensityAnalyzer()

def fetch_articles(company_name, num_articles=10):
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        logger.error("NEWSAPI_KEY not set")
        return []
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&language=en&sortBy=publishedAt"
    try:
        logger.info(f"Fetching articles for {company_name} with URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            logger.error(f"NewsAPI error: {data.get('message')}")
            return []
        articles = []
        for item in data.get("articles", [])[:num_articles]:
            content = item["description"] or item["content"] or "No content available"
            if content:
                articles.append({
                    "title": item["title"],
                    "content": content,
                    "url": item["url"]
                })
        logger.info(f"Fetched {len(articles)} articles for {company_name}")
        return articles
    except requests.RequestException as e:
        logger.error(f"Error fetching articles from NewsAPI: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in fetch_articles: {str(e)}")
        return []

def scrape_article(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title Available"
        paragraphs = soup.select('p')
        content = " ".join([p.get_text(strip=True) for p in paragraphs][:5])
        if not content:
            return None
        return {"title": title, "content": content, "url": url}
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def summarize_text(text, num_sentences=2):
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text
        return " ".join(sentences[:num_sentences])
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text

def analyze_sentiment(text):
    try:
        scores = sid.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Neutral"

def extract_topics(text):
    try:
        words = [w.lower() for w in word_tokenize(text) if w.isalnum() and w.lower() not in STOP_WORDS]
        if not words:
            return ["No Topics Identified"]
        word_freq = Counter(words).most_common(3)
        return [word for word, _ in word_freq]
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return ["Error in Topic Extraction"]

def generate_tts(text, output_file="/tmp/output.mp3"):
    try:
        if not text.strip():
            text = "कोई डेटा उपलब्ध नहीं है।"
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error generating TTS: {e}")
        tts = gTTS(text="त्रुटि: ऑडियो उत्पन्न नहीं हो सका।", lang='hi', slow=False)
        tts.save(output_file)
        return output_file

def comparative_analysis(articles):
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_dist[article['sentiment']] += 1
    coverage_diff = []
    if sentiment_dist["Positive"] > sentiment_dist["Negative"]:
        coverage_diff.append("Coverage is mostly positive, indicating strong public or market support.")
    elif sentiment_dist["Negative"] > sentiment_dist["Positive"]:
        coverage_diff.append("Coverage is mostly negative, suggesting challenges or controversies.")
    else:
        coverage_diff.append("Coverage is balanced between positive and negative sentiments.")
    return {
        "sentiment_distribution": sentiment_dist,
        "coverage_difference": coverage_diff
    }
