# api.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from utils import (
    fetch_articles,
    summarize_text,
    analyze_sentiment,
    extract_topics,
    generate_tts,
    comparative_analysis
)
from deep_translator import GoogleTranslator
import os
import logging

app = FastAPI(
    title="News Summarization API",
    description="API for news summarization, sentiment analysis, and Hindi TTS.",
    version="1.0.0"
)

@app.get("/analyze/{company_name}", response_model=dict)
async def analyze_company(company_name: str, num_articles: int = 10):
    try:
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
        
        translator = GoogleTranslator(source='en', target='hi')
        coverage_insight_hindi = translator.translate(comp_analysis['coverage_difference'][0])

        tts_text = (
            f"{company_name} की खबरों का विश्लेषण: "
            f"सकारात्मक {sentiment_dist['Positive']}, "
            f"नकारात्मक {sentiment_dist['Negative']}, "
            f"तटस्थ {sentiment_dist['Neutral']}। "
            f"कवरेज में मुख्य अंतर: {coverage_insight_hindi}"
        )
        audio_file = f"/tmp/audio_{company_name.replace(' ', '_')}.mp3"
        audio_path = generate_tts(tts_text, audio_file)
        logging.info(f"TTS generated at {audio_path}")

        return {
            "company": company_name,
            "articles": processed_articles,
            "comparative_analysis": comp_analysis,
            "audio": f"/audio/{company_name}"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in analyze_company: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/audio/{company_name}")
async def get_audio(company_name: str):
    audio_file = f"/tmp/audio_{company_name.replace(' ', '_')}.mp3"
    if os.path.exists(audio_file):
        return FileResponse(audio_file, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/health")
async def health_check():
    return {"status": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=7860, reload=True)

