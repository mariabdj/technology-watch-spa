from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
import asyncio

import scraper
import analyzer
import database

# --- ÉTAT GLOBAL ---
SCAN_STATE = {
    "is_scanning": False,
    "progress": 0,
    "message": "Prêt",
    "total_found": 0,
    "new_added": 0,
    "last_execution": None
}

scheduler = BackgroundScheduler()

def scheduled_scan():
    print("⏰ Scan automatique déclenché...")
    run_scan_process_sync()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Scan toutes les 6 heures
    scheduler.add_job(scheduled_scan, 'interval', hours=6)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="Cloud Watcher Pro", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    context_limit: int = 20

# --- LOGIQUE SCAN ---
def run_scan_process_sync():
    global SCAN_STATE
    SCAN_STATE["is_scanning"] = True
    SCAN_STATE["progress"] = 5
    SCAN_STATE["message"] = "Connexion aux flux..."
    SCAN_STATE["new_added"] = 0
    
    try:
        raw_articles = scraper.fetch_rss_data()
        total = len(raw_articles)
        SCAN_STATE["total_found"] = total
        SCAN_STATE["progress"] = 10
        
        if total == 0:
            SCAN_STATE["is_scanning"] = False
            SCAN_STATE["last_execution"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return

        step_value = 80 / total if total > 0 else 0
        
        for i, article in enumerate(raw_articles):
            SCAN_STATE["message"] = f"Traitement ({i+1}/{total}): {article.get('title')[:15]}..."
            
            # Vérification si l'article existe déjà
            if not database.check_link_exists(article.get("link")):
                
                # --- PAUSE ANTI-QUOTA (CRITIQUE) ---
                # On attend 10 secondes entre chaque appel IA pour respecter le plan gratuit
                time.sleep(10) 
                
                analyzed = analyzer.analyze_article_with_ai(article)
                if analyzed:
                    database.insert_news(analyzed)
                    SCAN_STATE["new_added"] += 1
            else:
                print(f"   -> Déjà en base : {article.get('title')[:20]}...")
            
            SCAN_STATE["progress"] = 10 + int((i + 1) * step_value)
            
        SCAN_STATE["progress"] = 100
        SCAN_STATE["message"] = "Terminé !"
        # Enregistrement de l'heure en UTC (le frontend convertira en heure d'Algérie)
        SCAN_STATE["last_execution"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
    except Exception as e:
        print(f"Erreur Scan: {e}")
        SCAN_STATE["message"] = "Erreur technique"
    finally:
        time.sleep(1) 
        SCAN_STATE["is_scanning"] = False

def run_scan_wrapper():
    # Exécution synchrone dans un thread séparé géré par FastAPI
    run_scan_process_sync()

# --- ROUTES ---
@app.get("/news")
def get_news():
    return database.get_all_news(limit=100)

@app.get("/stats")
def get_stats_route():
    return database.get_stats()

@app.get("/scan-status")
def get_scan_status():
    return SCAN_STATE

@app.post("/trigger-scan")
async def trigger_scan(background_tasks: BackgroundTasks):
    if SCAN_STATE["is_scanning"]:
        return {"status": "busy", "message": "Déjà en cours"}
    
    # Lancement en arrière-plan
    background_tasks.add_task(run_scan_wrapper)
    return {"status": "started", "message": "Démarré"}

@app.post("/chat")
def chat_with_advisor(req: ChatRequest):
    recent_news = database.get_all_news(limit=req.context_limit)
    context_text = "Actu Cloud :\n"
    for n in recent_news:
        context_text += f"- {n['title']} (Impact: {n['impact_level']})\n"
    response = analyzer.ask_gemini_strategy(req.question, context_text)
    return {"response": response}

@app.post("/news/{item_id}/toggle-save")
def toggle_save_route(item_id: str):
    return {"status": "success", "is_saved": database.toggle_save(item_id)}

if __name__ == "__main__":
    import uvicorn
    # Le reload=True est utile en dev, mais attention aux doubles scans au redémarrage
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)