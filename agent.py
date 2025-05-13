import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools.serp_search import search_competitors
from tools.semantic_retriever import find_related_context
from tools.Doc_embadder import search_uploaded_doc, process_document
from functools import lru_cache
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

session_log_file = "JSON\\session_log.json"

def log_session(memory: dict):
    try:
        if os.path.exists(session_log_file):
            with open(session_log_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(memory)
        
        with open(session_log_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error logging session: {e}")       


@lru_cache(maxsize=100)
def clarify_idea(idea: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You clarify vague startup ideas."},
            {"role": "user", "content": f"Clarify and rephrase this startup idea in one sentence: {idea}"}
        ]
    )
    return response.choices[0].message.content.strip()



@lru_cache(maxsize=100)
def cached_market_analysis(idea: str) -> str:
    prompt = f"""
    You are a startup analyst. Analyze the following idea:
    "{idea}"
    
    Provide:
    1. Market overview
    2. Target customer segments
    3. Main pain point solved
    4. Likely revenue model
    
    Respond clearly using bullet points.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a structured and insightful startup analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


@lru_cache(maxsize=100)
def cached_suggestions(idea: str, analysis_text: str, competitors_text: str, past_context: str = "", doc_context: str = "") -> str:
    prompt = f"""
    You previously analyzed similar startup ideas:
    {past_context}
    
    And here is relevant content from the uploaded document:
    {doc_context}
    
    Given the startup idea:
    "{idea}"
    
    Here is the market analysis:
    {analysis_text}
    
    And here are the competitors:
    {competitors_text}
    
    Now suggest at least 2 specific improvements or pivot the idea to stand out in the market. Focus on strategy, differentiation, or underserved niches.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a strategic and innovative startup advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@lru_cache(maxsize=100)
def analyze_competitors(idea: str, city: str, country_code: str) -> dict:
    """
    Evaluates a startup idea by generating market analysis, fetching competitors from SerpAPI,
    and using OpenAI to suggest improvements or pivots.
    """
    #1. Clarify the idea
    idea = idea.strip().lower()
    clarified = clarify_idea(idea)
    print(f"🔍 Clarified Idea: {clarified}")
    #2. Market Analysis
    analysis_text = cached_market_analysis(clarified)
    #3. Competitors
    competitors_text = search_competitors(clarified, city=city, country_code=country_code)
    past_context = find_related_context(clarified)
    doc_context = search_uploaded_doc(clarified)
    #4. Suggestions
    suggestion_text = cached_suggestions(clarified, analysis_text, competitors_text, past_context, doc_context)
    #5. Return the results
    
    summary = f"""
    🧠 **Clarified Idea**:
{clarified}

📊 **Market Analysis**:
{analysis_text}

🏢 **Top Competitors**:
{competitors_text}

💡 **Strategic Suggestions**:
{suggestion_text}
    """
    
    memory = {
        "Idea": clarified,
        "Market Analysis": analysis_text,
        "Competitors": competitors_text,
        "Suggestions": suggestion_text,
        "timestamp": datetime.now().isoformat(),
        "Text summary": summary.strip()
    }

    log_session(memory)
    return memory

# Example usage
# if __name__ == "__main__":
#     idea = "Designing new digital business models with AI support"
#     result = analyze_competitors(idea)

#     print("\n📄 Structured Summary:\n")
#     print(result["Text summary"])
    