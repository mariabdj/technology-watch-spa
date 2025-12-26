import os
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime, timezone

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("⚠️ Clé Supabase manquante")

supabase: Client = create_client(url, key)

def check_link_exists(link: str) -> bool:
    try:
        res = supabase.table("news").select("id").eq("link", link).execute()
        return len(res.data) > 0
    except:
        return False

def insert_news(data: dict):
    try:
        if "created_at" not in data:
            # IMPORTANT: On enregistre en UTC. 
            # Le navigateur convertira en heure locale (Algérie) automatiquement.
            data["created_at"] = datetime.now(timezone.utc).isoformat()
        
        data["is_saved"] = False
        supabase.table("news").insert(data).execute()
    except Exception as e:
        print(f"Erreur insert: {e}")

def get_all_news(limit: int = 100):
    try:
        return supabase.table("news").select("*").order("created_at", desc=True).limit(limit).execute().data
    except:
        return []

def toggle_save(item_id: str):
    try:
        current = supabase.table("news").select("is_saved").eq("id", item_id).execute().data
        if not current: return False
        
        new_val = not current[0].get("is_saved", False)
        supabase.table("news").update({"is_saved": new_val}).eq("id", item_id).execute()
        return new_val
    except Exception as e:
        print(f"Erreur toggle save: {e}")
        return False

def get_stats():
    try:
        data = supabase.table("news").select("provider, impact_level, category, created_at").execute().data
        
        total = len(data)
        critical = len([d for d in data if d['impact_level'] == 3])
        providers = Counter([d['provider'] for d in data])
        active_provider = providers.most_common(1)[0][0] if providers else "N/A"
        categories = Counter([d.get('category', 'Autre') for d in data])
        dates = [d['created_at'].split('T')[0] for d in data if d.get('created_at')]
        timeline = Counter(dates)

        return {
            "total_news": total,
            "critical_news": critical,
            "active_provider": active_provider,
            "providers_stats": dict(providers),
            "categories_stats": dict(categories),
            "timeline_stats": dict(timeline)
        }
    except Exception as e:
        return {
            "total_news": 0, "critical_news": 0, "active_provider": "-", 
            "providers_stats": {}, "categories_stats": {}, "timeline_stats": {}
        }