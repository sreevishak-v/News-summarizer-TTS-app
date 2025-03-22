# api.py
from fastapi import FastAPI, HTTPException
from utils import (
    fetch_articles,
    summarize_text,
    analyze_sentiment,
    extract_topics,
    generate_tts,
    comparative_analysis
)
import os

# Initialize FastAPI app
app = FastAPI(
    title="News Summarization API",
    description="API for news summarization, sentiment analysis, and Hindi TTS.",
    version="1.0.0"
)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from deep_translator import GoogleTranslator

@app.get("/analyze/{company_name}", response_model=dict)
async def analyze_company(company_name: str, num_articles: int = 10):
    articles = fetch_articles(company_name, num_articles=num_articles)
    if not articles:
        raise HTTPException(status_code=404, detail=f"No articles found for {company_name}")

    processed_articles = []
    for article in articles:
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(summary)
        topics = extract_topics(summary)
        processed_articles.append({
            "title": article["title"],
            "summary": summary,
            "sentiment": sentiment,
            "topics": topics,
            "url": article["url"]
        })

    comp_analysis = comparative_analysis(processed_articles)
    sentiment_dist = comp_analysis["sentiment_distribution"]
    
    # Translate coverage insights to Hindi
    translator = GoogleTranslator(source='en', target='hi')
    coverage_insight_hindi = translator.translate(comp_analysis['coverage_difference'][0])

    tts_text = (
        f"{company_name} की खबरों का विश्लेषण: "
        f"सकारात्मक {sentiment_dist['Positive']}, "
        f"नकारात्मक {sentiment_dist['Negative']}, "
        f"तटस्थ {sentiment_dist['Neutral']}। "
        f"कवरेज में मुख्य अंतर: {coverage_insight_hindi}"
    )
    audio_file = f"audio_{company_name.replace(' ', '_')}.mp3"
    audio_path = generate_tts(tts_text, audio_file)

    return {
        "company": company_name,
        "articles": processed_articles,
        "comparative_analysis": comp_analysis,
        "audio": audio_path
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status message.
    """
    return {"status": "API is running"}


if __name__ == "__main__":
    import uvicorn
    # Run the API locally for testing
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)