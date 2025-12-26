import os
import uuid
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("⚠️ ERREUR: Les clés SUPABASE_URL ou SUPABASE_KEY sont manquantes.")

supabase: Client = create_client(url, key)

print("🌱 Démarrage du remplissage de la base de données (Historique Réaliste 5 mois)...")

# --- DONNÉES HISTORIQUES RÉALISTES (Derniers 5 mois) ---
# Basé sur les tendances réelles : Zero-ETL, IA Générative, Gouvernance, Vector Search.
historical_news = [
    # ==============================
    # AWS (Amazon Web Services)
    # ==============================
    {
        "title": "AWS annonce Amazon Q pour l'intégration de données (Zero-ETL)",
        "summary": "Amazon Q permet désormais de générer automatiquement des pipelines Zero-ETL entre Aurora et Redshift en langage naturel, simplifiant l'intégration de données sans code.",
        "provider": "AWS",
        "service": "AWS Glue / Redshift",
        "category": "ETL",
        "impact_level": 3,
        "impact_analysis": "Révolutionne la productivité des Data Engineers en automatisant la création de pipelines complexes.",
        "link": "https://aws.amazon.com/blogs/big-data/amazon-q-zero-etl-integration",
        "days_ago": 15
    },
    {
        "title": "Amazon Redshift ajoute le support du Vector Search pour le RAG",
        "summary": "Redshift supporte maintenant nativement la recherche vectorielle, permettant d'interroger des bases de connaissances pour les applications d'IA générative directement en SQL.",
        "provider": "AWS",
        "service": "Redshift",
        "category": "ML",
        "impact_level": 3,
        "impact_analysis": "Permet de construire des applications RAG performantes directement sur le Data Warehouse sans base vectorielle dédiée.",
        "link": "https://aws.amazon.com/about-aws/whats-new/2024/12/redshift-vector-search-preview",
        "days_ago": 45
    },
    {
        "title": "AWS Glue Data Quality ajoute la détection d'anomalies par IA",
        "summary": "Nouvelle fonctionnalité utilisant le ML pour détecter automatiquement les dérives de qualité (data drift) dans les Data Lakes S3 sans règles manuelles.",
        "provider": "AWS",
        "service": "AWS Glue",
        "category": "Gouvernance",
        "impact_level": 2,
        "impact_analysis": "Améliore la fiabilité des données pour les modèles ML sensibles.",
        "link": "https://aws.amazon.com/blogs/big-data/glue-data-quality-anomaly-detection",
        "days_ago": 60
    },
    {
        "title": "Amazon S3 Express One Zone : Latence ultra-faible pour Spark",
        "summary": "Lancement d'une nouvelle classe de stockage S3 offrant des performances 10x supérieures pour les charges de travail analytiques intensives comme Spark et EMR.",
        "provider": "AWS",
        "service": "S3",
        "category": "Stockage",
        "impact_level": 3,
        "impact_analysis": "Game changer pour les coûts et la performance des traitements Big Data temps réel.",
        "link": "https://aws.amazon.com/s3/express-one-zone/",
        "days_ago": 110
    },
    {
        "title": "EMR Serverless supporte désormais les images Docker personnalisées",
        "summary": "Les développeurs peuvent maintenant utiliser leurs propres images Docker pour exécuter des jobs Spark et Hive sur EMR Serverless, offrant plus de flexibilité.",
        "provider": "AWS",
        "service": "EMR",
        "category": "Compute",
        "impact_level": 2,
        "impact_analysis": "Facilite la migration des workloads legacy vers le Serverless.",
        "link": "https://aws.amazon.com/about-aws/whats-new/2024/10/emr-serverless-custom-images",
        "days_ago": 90
    },
    {
        "title": "Amazon Athena supporte désormais les UDFs en Java et Python",
        "summary": "Athena permet l'exécution de fonctions définies par l'utilisateur (UDF) complexes directement dans les requêtes SQL serverless.",
        "provider": "AWS",
        "service": "Athena",
        "category": "Compute",
        "impact_level": 1,
        "impact_analysis": "Étend les capacités SQL standard pour des transformations complexes à la volée.",
        "link": "https://aws.amazon.com/blogs/big-data/athena-udf-support",
        "days_ago": 130
    },
    {
        "title": "AWS DataZone : Gouvernance automatisée pour les Data Mesh",
        "summary": "DataZone simplifie le partage de données entre comptes AWS avec une gestion fine des accès et un catalogue métier unifié.",
        "provider": "AWS",
        "service": "DataZone",
        "category": "Gouvernance",
        "impact_level": 2,
        "impact_analysis": "Simplifie massivement l'implémentation d'une architecture Data Mesh.",
        "link": "https://aws.amazon.com/datazone/",
        "days_ago": 20
    },
     {
        "title": "Amazon OpenSearch Serverless supporte les collections de vecteurs",
        "summary": "Mise à l'échelle automatique pour les collections vectorielles, facilitant le déploiement d'applications de recherche sémantique.",
        "provider": "AWS",
        "service": "OpenSearch",
        "category": "ML",
        "impact_level": 2,
        "impact_analysis": "Réduit la complexité opérationnelle des moteurs de recherche vectoriels.",
        "link": "https://aws.amazon.com/opensearch-service/serverless-vector-engine/",
        "days_ago": 50
    },

    # ==============================
    # AZURE (Microsoft)
    # ==============================
    {
        "title": "Microsoft Fabric : Disponibilité Générale (GA) annoncée",
        "summary": "La plateforme unifiée de données Microsoft Fabric est désormais en disponibilité générale, intégrant Data Factory, Synapse et Power BI en une seule interface SaaS.",
        "provider": "Azure",
        "service": "Microsoft Fabric",
        "category": "Gouvernance",
        "impact_level": 3,
        "impact_analysis": "L'annonce la plus importante de l'année pour l'écosystème Microsoft Data.",
        "link": "https://blog.fabric.microsoft.com/en-us/blog/fabric-ga-announcement",
        "days_ago": 30
    },
    {
        "title": "Azure AI Search : Augmentation massive des limites vectorielles",
        "summary": "Azure AI Search supporte désormais des milliards de vecteurs par index avec une latence milliseconde, optimisé pour les applications RAG à grande échelle.",
        "provider": "Azure",
        "service": "AI Search",
        "category": "ML",
        "impact_level": 2,
        "impact_analysis": "Essentiel pour les entreprises déployant des Copilots sur de grandes bases de connaissances.",
        "link": "https://azure.microsoft.com/updates/ai-search-vector-capacity",
        "days_ago": 40
    },
    {
        "title": "OneLake Shortcuts : Support pour S3 et Google Cloud Storage",
        "summary": "Microsoft Fabric OneLake permet de virtualiser des données stockées sur AWS S3 et GCP sans les déplacer, renforçant la stratégie multi-cloud.",
        "provider": "Azure",
        "service": "Microsoft Fabric",
        "category": "Stockage",
        "impact_level": 3,
        "impact_analysis": "Élimine les coûts d'egress et les pipelines de copie de données complexes.",
        "link": "https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts",
        "days_ago": 65
    },
    {
        "title": "Azure Synapse : Copilot pour l'écriture SQL et PySpark",
        "summary": "L'assistant IA Copilot est intégré dans Synapse Studio pour aider à écrire, déboguer et optimiser le code SQL et Python.",
        "provider": "Azure",
        "service": "Synapse Analytics",
        "category": "ML",
        "impact_level": 2,
        "impact_analysis": "Boost de productivité significatif pour les développeurs Data.",
        "link": "https://azure.microsoft.com/updates/synapse-copilot-preview",
        "days_ago": 100
    },
    {
        "title": "Azure Databricks : Support de DBR 14.3 LTS et Spark 3.5",
        "summary": "Nouvelle version Long Term Support de Databricks Runtime incluant les dernières optimisations de Spark et Photon.",
        "provider": "Azure",
        "service": "Databricks",
        "category": "Compute",
        "impact_level": 1,
        "impact_analysis": "Mise à jour standard recommandée pour la stabilité et la performance.",
        "link": "https://learn.microsoft.com/en-us/azure/databricks/release-notes/runtime/14.3lts",
        "days_ago": 140
    },
    {
        "title": "Cosmos DB for MongoDB vCore : Recherche vectorielle intégrée",
        "summary": "Cosmos DB ajoute le support natif des vecteurs pour l'API MongoDB, permettant de construire des apps IA sans changer de base de données.",
        "provider": "Azure",
        "service": "Cosmos DB",
        "category": "Stockage",
        "impact_level": 2,
        "impact_analysis": "Convergence des bases de données transactionnelles et vectorielles.",
        "link": "https://azure.microsoft.com/updates/cosmos-db-mongodb-vector",
        "days_ago": 85
    },
    {
        "title": "Azure Stream Analytics : Support de Delta Lake en sortie",
        "summary": "Écriture directe des flux de données temps réel au format Delta Lake, optimisant l'analyse post-traitement dans Synapse et Databricks.",
        "provider": "Azure",
        "service": "Stream Analytics",
        "category": "ETL",
        "impact_level": 2,
        "impact_analysis": "Simplifie l'architecture Lambda/Kappa sur Azure.",
        "link": "https://azure.microsoft.com/updates/stream-analytics-delta",
        "days_ago": 120
    },

    # ==============================
    # GCP (Google Cloud Platform)
    # ==============================
    {
        "title": "BigQuery Omni : Cross-Cloud Joins disponibles",
        "summary": "BigQuery permet désormais de faire des jointures SQL entre des données locales et des données stockées sur AWS S3 ou Azure Blob sans déplacement massif.",
        "provider": "GCP",
        "service": "BigQuery",
        "category": "Compute",
        "impact_level": 3,
        "impact_analysis": "Fonctionnalité clé pour les stratégies véritablement multi-cloud.",
        "link": "https://cloud.google.com/bigquery/docs/omni-introduction",
        "days_ago": 25
    },
    {
        "title": "Google Cloud Spanner Data Boost : Analytique sans impact sur la prod",
        "summary": "Data Boost permet d'exécuter des requêtes analytiques lourdes sur Spanner en utilisant des ressources de calcul indépendantes, sans ralentir les transactions.",
        "provider": "GCP",
        "service": "Spanner",
        "category": "Compute",
        "impact_level": 2,
        "impact_analysis": "Permet le HTAP (Hybrid Transactional/Analytical Processing) à grande échelle.",
        "link": "https://cloud.google.com/spanner/docs/databoost/databoost-overview",
        "days_ago": 55
    },
    {
        "title": "Gemini in Looker : Génération de tableaux de bord par chat",
        "summary": "Looker intègre Gemini pour permettre aux utilisateurs métier de créer des visualisations et des rapports complets simplement en conversant avec l'IA.",
        "provider": "GCP",
        "service": "Looker",
        "category": "ML",
        "impact_level": 2,
        "impact_analysis": "Démocratisation de la BI pour les utilisateurs non techniques.",
        "link": "https://cloud.google.com/blog/products/business-intelligence/gemini-in-looker",
        "days_ago": 10
    },
    {
        "title": "BigQuery Studio : Environnement unifié pour SQL et Python",
        "summary": "Lancement de BigQuery Studio, un IDE unique pour l'analyse SQL, le Machine Learning et la programmation Python (Notebooks Colab intégrés).",
        "provider": "GCP",
        "service": "BigQuery",
        "category": "Gouvernance",
        "impact_level": 2,
        "impact_analysis": "Unifie l'expérience développeur Data et Data Scientist.",
        "link": "https://cloud.google.com/blog/products/data-analytics/bigquery-studio-generative-ai",
        "days_ago": 95
    },
    {
        "title": "AlloyDB AI : Vecteurs et ML intégrés pour PostgreSQL",
        "summary": "AlloyDB pour PostgreSQL intègre des capacités vectorielles natives pour construire des applications d'IA générative ultra-rapides.",
        "provider": "GCP",
        "service": "AlloyDB",
        "category": "Stockage",
        "impact_level": 2,
        "impact_analysis": "Concurrent direct de pgvector avec les performances de l'infrastructure Google.",
        "link": "https://cloud.google.com/alloydb/ai",
        "days_ago": 70
    },
    {
        "title": "Dataplex : Gouvernance automatique des lacs de données",
        "summary": "Nouvelles fonctionnalités d'auto-découverte et de classification des données sensibles dans Dataplex pour renforcer la sécurité.",
        "provider": "GCP",
        "service": "Dataplex",
        "category": "Sécurité",
        "impact_level": 2,
        "impact_analysis": "Indispensable pour la conformité PII/GDPR à l'échelle du Petabyte.",
        "link": "https://cloud.google.com/dataplex",
        "days_ago": 115
    },
    {
        "title": "Cloud Storage FUSE : Performances améliorées pour le training ML",
        "summary": "Mise à jour du système de fichiers FUSE pour GCS, optimisant le chargement de données pour l'entraînement de modèles sur GKE et Vertex AI.",
        "provider": "GCP",
        "service": "Cloud Storage",
        "category": "Stockage",
        "impact_level": 1,
        "impact_analysis": "Réduit les goulots d'étranglement I/O pour les gros modèles de Deep Learning.",
        "link": "https://cloud.google.com/blog/products/storage/cloud-storage-fuse-csi-driver",
        "days_ago": 145
    },
    {
        "title": "BigQuery Data Clean Rooms : Partage sécurisé sans copie",
        "summary": "Disponibilité générale des Data Clean Rooms pour partager des données avec des partenaires externes tout en préservant la confidentialité.",
        "provider": "GCP",
        "service": "BigQuery",
        "category": "Sécurité",
        "impact_level": 3,
        "impact_analysis": "Facilite les collaborations B2B et l'enrichissement de données marketing.",
        "link": "https://cloud.google.com/bigquery/docs/data-clean-rooms",
        "days_ago": 80
    }
]

count = 0

for news in historical_news:
    # Génération d'une date passée précise
    past_date = datetime.now() - timedelta(days=news["days_ago"])
    formatted_date = past_date.isoformat()

    # Préparation de l'objet pour Supabase
    data_to_insert = {
        "title": news["title"],
        "link": news["link"], # Lien unique
        "summary": news["summary"],
        "provider": news["provider"],
        "service": news["service"],
        "category": news["category"],
        "impact_level": news["impact_level"],
        "impact_analysis": news["impact_analysis"],
        "raw_source": f"Official {news['provider']} Source",
        "created_at": formatted_date # Date simulée réaliste
    }

    try:
        # On utilise upsert pour ne pas planter si on relance le script
        # On ignore les doublons potentiels basés sur le lien
        supabase.table("news").upsert(data_to_insert, on_conflict="link").execute()
        print(f"✅ Ajouté (Il y a {news['days_ago']} jours) : {news['title'][:40]}...")
        count += 1
    except Exception as e:
        print(f"❌ Erreur sur {news['title'][:20]}: {e}")

print(f"\n🎉 Terminé ! {count} articles réalistes (5 derniers mois) ont été ajoutés.")