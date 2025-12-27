# ☁️ Cloud Watcher Pro — AI-Powered Tech Watch

Welcome to **Cloud Watcher Pro**! This is an intelligent technical watch dashboard designed for Cloud Architects and Data Engineers. It uses **Generative AI (Google Gemini)** to automatically scrape, analyze, and categorize the latest updates from AWS, Azure, and Google Cloud.

<p align="center">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-blue" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini%20Flash-magenta" />
  <img src="https://img.shields.io/badge/Database-Supabase-green" />
  <img src="https://img.shields.io/badge/Frontend-Alpine.js%20%7C%20Tailwind-blueviolet" />
  <img src="https://img.shields.io/badge/Live-Demo-success" />
</p>

🎯 **Live Demo:** https://mariabdj.github.io/technology-watch-spa/

---

## 🧩 Project Overview

Keeping up with the cloud ecosystem (AWS, Azure, GCP) is overwhelming. This project automates the process by scraping official RSS feeds and using an **LLM (Large Language Model)** to act as an expert filter.

The system does not just display links; it **understands** them. It assigns impact levels (Critical, Major, Minor), categorizes updates (ML, Storage, Security...), and generates executive summaries in French.

**Key Features:**
- 📡 **Automated Scraping:** Polls AWS, Azure, and GCP feeds every 6 hours.
- 🧠 **AI Analysis:** Uses `Gemini 2.5 Flash` to summarize and rate the strategic impact of every article.
- 📊 **Analytics Dashboard:** Visualizes trends by provider and category.
- 💬 **Strategic Advisor:** An integrated chatbot that answers questions based *only* on the collected news context.
- 🌑 **Modern UI:** Responsive design with Dark Mode support.

---

## 🧠 How It Works (The Pipeline)

| Stage | Technology | Description |
| :--- | :--- | :--- |
| **1. Ingestion** | `scraper.py` | Custom XML parser fetches RSS/Atom feeds from Cloud Providers. |
| **2. Analysis** | `analyzer.py` | Google **Gemini 2.5 Flash** reads the content and outputs a structured JSON (Summary, Impact 1-3, Category). |
| **3. Storage** | `database.py` | Data is stored in **Supabase** (PostgreSQL) with UTC timestamps. |
| **4. API** | `main.py` | **FastAPI** serves the data and manages background tasks (`APScheduler`). |
| **5. Frontend** | `index.html` | **Alpine.js** & **Tailwind CSS** fetch data from the API and render the dashboard. |

---

## 🌐 Interface Features

✅ **Smart Filtering:** Filter news by Provider (AWS/Azure/GCP), Impact (Critical/Major), or Category.  
✅ **Impact Badges:** Visual indicators for "Critical" updates (Level 3).  
✅ **AI Advisor:** A chat interface to ask "What's new in Big Data this week?" or "Summarize the risks."  
✅ **Real-time Status:** Progress bar showing the scraping and analysis status.  
✅ **Bookmarks:** Save important articles for later reading.  
✅ **Responsive:** Fully functional on mobile and desktop.

---

## 📂 Technologies Used

| Area | Stack |
| :--- | :--- |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, APScheduler |
| **AI Model** | Google Gemini 2.5 Flash (`google-generativeai`) |
| **Database** | Supabase (PostgreSQL client) |
| **Frontend** | HTML5, Tailwind CSS (CDN), Alpine.js, Chart.js, Remix Icons |
| **Hosting** | Render (Web Service) |

---

## 🖥️ Folder Structure

```bash
📁 /cloud-watcher-pro
│
├── 📄 main.py           # API Entry point & Scheduler
├── 📄 scraper.py        # Robust RSS/Atom XML Parser
├── 📄 analyzer.py       # AI Logic (Prompt Engineering)
├── 📄 database.py       # Supabase CRUD operations
│
├── 📄 index.html        # Main Dashboard UI
├── 📄 style.css         # Custom styles & Animations
├── 📄 script.js         # Frontend Logic (Alpine.js)
│
├── 📄 requirements.txt  # Python dependencies
└── 📄 .env              # API Keys (Gemini, Supabase) - Not in repo

```

---

## 🛠️ How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/mariabdj/technology-watch-spa
cd cloud-watcher

```


2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Configure Environment**
Create a `.env` file at the root:
```env
GEMINI_API_KEY="your_google_api_key"
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_anon_key"

```


4. **Run the Server**
```bash
uvicorn main:app --reload

```


5. **Access the App**
Open `index.html` in your browser (Live Server recommended) or visit `http://127.0.0.1:8000/docs` for the API Swagger.

---

## 👨‍🎓 Author

**Maria Boudjelal** - *Data Engineering Student*

---

## ✨ Future Improvements

* [ ] **Email Alerts:** Send weekly digests for "Critical" news via SMTP.
* [ ] **Multi-User Auth:** Allow different users to have private bookmarks.
* [ ] **More Sources:** Add Databricks, Snowflake, and OpenAI blogs.

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

### 🙏 Acknowledgements

* [Google AI Studio](https://aistudio.google.com/) for the Gemini API.
* [Supabase](https://supabase.com/) for the amazing database tier.
* [Render](https://render.com/) for hosting.
