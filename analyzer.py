import google.generativeai as genai
import os
import json
import warnings
from dotenv import load_dotenv

# Supprime les avertissements de dépréciation de Google qui polluent les logs
warnings.filterwarnings("ignore")

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Utilisation du modèle Flash (plus rapide et économe)
MODEL_NAME = 'gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

def analyze_article_with_ai(article_data):
    """Analyse une news pour extraction JSON"""
    title = article_data.get("title")
    content = (article_data.get("content") or "")[:3000]
    provider_hint = article_data.get("raw_provider", "Unknown")

    prompt = f"""
    Role: Expert Data Engineering.
    Tâche: Extrais les infos de cette news Cloud en JSON.
    
    Source: {provider_hint}
    Titre: {title}
    Contenu: {content}

    Règles:
    1. Resumé en français (2 phrases max).
    2. Catégorie PARMI: [Stockage, Compute, ML, Gouvernance, Sécurité, ETL, Base de Données].
    3. Impact: 1 (Faible), 2 (Moyen), 3 (Critique/Stratégique).
    4. Analyse Impact: 1 phrase pour un CTO.

    JSON attendu:
    {{
        "title": "Titre FR",
        "summary": "Résumé FR",
        "provider": "AWS/Azure/GCP",
        "service": "Nom service",
        "category": "Catégorie",
        "impact_level": 1,
        "impact_analysis": "Analyse..."
    }}
    """
    try:
        res = model.generate_content(prompt)
        # Nettoyage Markdown
        text = res.text.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(text)
        analysis["link"] = article_data.get("link")
        analysis["raw_source"] = provider_hint
        return analysis
    except Exception as e:
        # On log l'erreur mais on ne crash pas l'app
        print(f"⚠️ Erreur IA sur '{title[:15]}...': {e}")
        return None

def ask_gemini_strategy(question, context):
    try:
        prompt = f"""
        Tu es un Consultant Stratégique en Cloud.
        Contexte Actu : {context}
        Question : "{question}"
        Réponds en Markdown.
        """
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Indisponible pour le moment ({e})"