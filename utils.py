# utils.py
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from gtts import gTTS
import os

sid = SentimentIntensityAnalyzer()
STOP_WORDS = set(stopwords.words('english'))

def fetch_articles(company_name, num_articles=10):
    query = f"{company_name} news"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('div.SoaBEf a')  # Updated selector
        articles = []
        for link in links[:num_articles]:
            href = link.get('href', '')
            if href.startswith('/url?q='):
                href = href.split('/url?q=')[1].split('&')[0]
            if href.startswith('http') and 'javascript' not in href.lower():
                article = scrape_article(href)
                if article:
                    articles.append(article)
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
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

def generate_tts(text, output_file="output.mp3"):
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
        coverage_diff.append("कवरेज ज्यादातर सकारात्मक है, जो मजबूत सार्वजनिक या बाजार समर्थन को दर्शाता है।")
    elif sentiment_dist["Negative"] > sentiment_dist["Positive"]:
        coverage_diff.append("कवरेज मुख्य रूप से नकारात्मक है, जो चुनौतियों या विवादों का सुझाव देता है।")
    else:
        coverage_diff.append("कवरेज सकारात्मक और नकारात्मक भावनाओं के बीच संतुलित है।")
    
    return {
        "sentiment_distribution": sentiment_dist,
        "coverage_difference": coverage_diff
    }