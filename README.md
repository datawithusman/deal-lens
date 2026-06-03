<div align="center">

# 🔍 DealLens

**AI-Powered Startup Research Tool for VC Analysts**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)]()
[![GLM-5.1](https://img.shields.io/badge/GLM--5.1-41299A?style=flat-square)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)]()
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)]()
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)]()
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)]()

*Evaluate startups in seconds, not hours. DealLens automates the research pipeline so VC analysts can focus on decisions, not data collection.*

</div>

---

## 🎯 The Problem

VC analysts spend **60-70% of their time** on manual research — scraping data, reading pitch decks, comparing metrics, and writing investment memos. DealLens eliminates this bottleneck.

## ✨ Features

- **🔍 Startup Intelligence** — Instant company analysis powered by GLM-5.1
- **📊 Automated Scoring** — Multi-factor evaluation across market, team, traction, and technology
- **📄 Research Reports** — Auto-generated investment memos with key metrics
- **⚡ Real-time Pipeline** — FastAPI backend with LangChain orchestration
- **🎨 Clean Dashboard** — Next.js frontend with intuitive data visualization
- **🔗 API-First Design** — RESTful endpoints for integration with existing workflows

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│              TypeScript + Tailwind CSS               │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
                       ▼
┌─────────────────────────────────────────────────────┐
│                 FastAPI Backend                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  LangChain   │  │   GLM-5.1    │  │  Research   │ │
│  │  Orchestr.   │──│   Engine     │──│  Pipeline   │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│  ┌─────────────┐  ┌──────────────┐                  │
│  │   Scoring    │  │   Report     │                  │
│  │   Engine     │──│  Generator   │                  │
│  └─────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- GLM-5.1 API key

### Installation

```bash
# Clone the repository
git clone https://github.com/datawithusman/deal-lens.git
cd deal-lens

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend
cd ../frontend
npm install
```

### Configuration

Create a `.env` file in the backend directory:

```env
GLM_API_KEY=your_glm_api_key_here
LANGCHAIN_API_KEY=your_langchain_key_here
```

### Usage

```python
# Start the FastAPI backend
cd backend
uvicorn main:app --reload --port 8000

# Start the Next.js frontend
cd frontend
npm run dev
```

### API Example

```python
import requests

# Analyze a startup
response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "company_name": "TechStartup Inc.",
        "website": "https://techstartup.com",
        "industry": "SaaS"
    }
)

report = response.json()
print(report["score"])        # Overall score: 78/100
print(report["recommendation"])  # "Strong potential — schedule meeting"
```

---

## 📁 Project Structure

```
deal-lens/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Config & settings
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   └── chains/        # LangChain pipelines
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities
│   ├── package.json
│   └── tailwind.config.ts
└── README.md
```

---

## 👤 Built by

**Muhammad Usman** — AI Systems Developer @ Nobel AI

[![Portfolio](https://img.shields.io/badge/Portfolio-datawithusman.com-6C63FF?style=flat-square)](https://datawithusman.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/datawithusman)
[![GitHub](https://img.shields.io/badge/GitHub-datawithusman-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/datawithusman)

---

<div align="center">

**If DealLens helped your investment research, drop a ⭐!**

</div>