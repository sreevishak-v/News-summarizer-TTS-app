# utils.py
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from gtts import gTTS
import os

# Initialize NLTK Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

# Stopwords for topic extraction
STOP_WORDS = set(stopwords.words('english'))


def fetch_articles(company_name, num_articles=10):
    api_key = "cc51154dfad849508c2076a186cca6ec"  # Get from newsapi.org
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&language=en&sortBy=publishedAt"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for item in data.get("articles", [])[:num_articles]:
            articles.append({
                "title": item["title"],
                "content": item["description"] or item["content"] or "No content available",
                "url": item["url"]
            })
        return articles
    except Exception as e:
        print(f"Error fetching articles from NewsAPI: {e}")
        return []

def scrape_article(url):
    """
    Scrape title and content from a news article URL.
    
    Args:
        url (str): URL of the article to scrape.
    
    Returns:
        dict: Dictionary with title, content, and url, or None if scraping fails.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No Title Available"
        
        # Extract content (limited to first 5 paragraphs for brevity)
        paragraphs = soup.select('p')
        content = " ".join([p.get_text(strip=True) for p in paragraphs][:5])
        
        if not content:
            return None
        
        return {
            "title": title,
            "content": content,
            "url": url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def summarize_text(text, num_sentences=2):
    """
    Generate a summary of the text using extractive summarization.
    
    Args:
        text (str): Text to summarize.
        num_sentences (int): Number of sentences in the summary (default: 2).
    
    Returns:
        str: Summarized text.
    """
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text
        return " ".join(sentences[:num_sentences])
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text  # Return original text if summarization fails


def analyze_sentiment(text):
    """
    Perform sentiment analysis on the text.
    
    Args:
        text (str): Text to analyze.
    
    Returns:
        str: Sentiment label (Positive, Negative, Neutral).
    """
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
        return "Neutral"  # Default to Neutral on error


def extract_topics(text):
    """
    Extract key topics from the text based on word frequency.
    
    Args:
        text (str): Text to analyze.
    
    Returns:
        list: List of top 3 topics (keywords).
    """
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
    """
    Convert text to Hindi speech and save as an audio file.
    
    Args:
        text (str): Text to convert to speech.
        output_file (str): Path to save the audio file (default: 'output.mp3').
    
    Returns:
        str: Path to the generated audio file.
    """
    try:
        # Ensure text is not empty
        if not text.strip():
            text = "कोई डेटा उपलब्ध नहीं है।"
        
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error generating TTS: {e}")
        # Generate a fallback audio
        tts = gTTS(text="त्रुटि: ऑडियो उत्पन्न नहीं हो सका।", lang='hi', slow=False)
        tts.save(output_file)
        return output_file


def comparative_analysis(articles):
    """
    Perform comparative sentiment analysis across articles.
    
    Args:
        articles (list): List of article dictionaries with sentiment.
    
    Returns:
        dict: Sentiment distribution and coverage insights.
    """
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_dist[article['sentiment']] += 1
    
    # Simple coverage difference insight
    coverage_diff = []
    if sentiment_dist["Positive"] > sentiment_dist["Negative"]:
        coverage_diff.append("Coverage is mostly positive, indicating strong public or market support.")
    elif sentiment_dist["Negative"] > sentiment_dist["Positive"]:
        coverage_diff.append("Coverage leans negative, suggesting challenges or controversies.")
    else:
        coverage_diff.append("Coverage is balanced between positive and negative sentiments.")
    
    return {
        "sentiment_distribution": sentiment_dist,
        "coverage_difference": coverage_diff
    }


if __name__ == "__main__":
    # Test the functions
    articles = fetch_articles("Tesla", num_articles=2)
    for article in articles:
        summary = summarize_text(article['content'])
        sentiment = analyze_sentiment(summary)
        topics = extract_topics(summary)
        print(f"Title: {article['title']}")
        print(f"Summary: {summary}")
        print(f"Sentiment: {sentiment}")
        print(f"Topics: {topics}")
        print("---")
    
    # Test TTS
    tts_text = "टेस्ला की खबरें सकारात्मक हैं।"
    audio_file = generate_tts(tts_text, "test_output.mp3")
    print(f"Audio saved to: {audio_file}")