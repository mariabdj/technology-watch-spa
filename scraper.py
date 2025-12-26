import requests
import xml.etree.ElementTree as ET
import time

# Headers pour simuler un navigateur et éviter les rejets
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

RSS_FEEDS = [
    {"url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/", "provider": "AWS"},
    {"url": "https://aws.amazon.com/blogs/big-data/feed/", "provider": "AWS"},
    {"url": "https://azure.microsoft.com/en-us/blog/feed/", "provider": "Azure"},
    # Flux GCP plus fiable
    {"url": "https://feeds.feedburner.com/GoogleCloudPlatform", "provider": "GCP"}
]

def parse_xml_feed(content, provider):
    """Parseur robuste compatible RSS et Atom"""
    articles = []
    try:
        root = ET.fromstring(content)
        
        # 1. Format RSS Standard (<item>)
        items = root.findall(".//item")
        if not items:
            # 2. Format Atom (<entry>) - Gère les namespaces
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
        if not items:
            # 3. Fallback sans namespace
             items = root.findall(".//entry")

        for item in items:
            # Titre
            title = item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title")
            
            # Lien
            link = item.findtext("link")
            if not link:
                link_elem = item.find("{http://www.w3.org/2005/Atom}link")
                if link_elem is not None:
                    link = link_elem.get("href")
            
            # Contenu
            description = item.findtext("description") or \
                          item.findtext("{http://www.w3.org/2005/Atom}content") or \
                          item.findtext("{http://www.w3.org/2005/Atom}summary") or \
                          "Contenu non disponible"

            if title and link:
                articles.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    # On tronque à 5000 char pour économiser des tokens IA
                    "content": description[:5000],
                    "raw_provider": provider
                })
                
    except Exception as e:
        print(f"⚠️ Erreur de parsing XML pour {provider}: {e}")
        
    return articles

def fetch_rss_data():
    all_articles = []
    print("📡 Démarrage du scraping RSS (Mode Direct)...")

    for source in RSS_FEEDS:
        feed_url = source["url"]
        provider = source["provider"]
        
        try:
            # Timeout augmenté à 30s pour les connexions lentes (Azure)
            response = requests.get(feed_url, headers=HEADERS, timeout=30)
            
            if response.status_code == 200:
                items = parse_xml_feed(response.content, provider)
                # On ne garde que les 3 derniers par flux pour limiter la charge IA
                items = items[:3]
                print(f"   -> {provider}: {len(items)} articles extraits.")
                all_articles.extend(items)
            else:
                print(f"❌ Erreur HTTP {response.status_code} sur {feed_url}")
                
        except Exception as e:
            print(f"❌ Erreur réseau sur {feed_url}: {e}")

    return all_articles