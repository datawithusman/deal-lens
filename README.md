<div align="center">

# 🔍 DealLens

### AI-Powered Startup Research Tool for VC Analysts

**Instantly evaluate startups with AI-generated investment snapshots.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Docs](#-api-documentation) • [Tech Stack](#-tech-stack)

</div>

---

## 🎯 What is DealLens?

DealLens helps **venture capital analysts** quickly evaluate startup deals by combining **web scraping** with **AI-powered analysis** (GLM-5.1 or GPT-4). Simply enter a startup's name and website — get a structured VC investment snapshot in seconds.

### 💡 The Problem
VC analysts spend **4-6 hours** researching each startup before deciding whether to pursue a deal. DealLens reduces this to **under 30 seconds**.

### ✨ The Solution
DealLens automatically:
- 🌐 **Scrapes** the startup's website
- 🤖 **Analyzes** using AI (GLM-5.1 / GPT-4)
- 📊 **Generates** a structured investment snapshot with fit scoring

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Startup Analysis** | Enter name + URL → get full VC snapshot |
| 🌐 **Web Scraping** | Auto-extract content from startup websites |
| 🤖 **Dual AI Engine** | GLM-5.1 (Z.ai) or OpenAI GPT-4 |
| 📊 **Fit Scoring** | Sector match, stage match, team quality, market size |
| 📋 **Fund Profiles** | Configure multiple fund investment criteria |
| 📜 **Analysis History** | Track all past analyses with statistics |
| 🔐 **JWT Authentication** | Secure user accounts with bcrypt |
| 🌙 **Dark Mode** | Beautiful dark/light theme support |
| 🎯 **Demo Mode** | Try without API keys using dummy data |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DealLens Architecture                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────────┐         ┌──────────────────────┐     │
│   │   Next.js     │  HTTP   │    FastAPI Backend    │     │
│   │   Frontend    │◄───────►│    (Python)           │     │
│   │   (React)     │  REST   │                       │     │
│   └──────────────┘         │   ┌────────────────┐  │     │
│                            │   │ Scraper Service │  │     │
│   - Landing Page           │   │ (Trafilmatura)  │  │     │
│   - Auth (Login/Signup)    │   └───────┬────────┘  │     │
│   - Dashboard              │           │            │     │
│   - Analyze Startup        │   ┌───────▼────────┐  │     │
│   - Fund Profiles          │   │ AI Analyzer     │  │     │
│   - History                │   │ (GLM-5.1/GPT-4)│  │     │
│                            │   └────────────────┘  │     │
│                            │                       │     │
│                            │   ┌────────────────┐  │     │
│                            │   │ SQLite Database │  │     │
│                            │   │ (SQLAlchemy)    │  │     │
│                            │   └────────────────┘  │     │
│                            └──────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/deal-lens.git
cd deal-lens
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys (optional - demo mode works without them)
```

### 3. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Configure environment
cp .env.local.example .env.local
```

### 4. Run the Application

**Terminal 1 — Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Open in Browser
- 🖥️ **Frontend:** http://localhost:3000
- 📚 **API Docs:** http://localhost:8000/docs
- ❤️ **Health Check:** http://localhost:8000/health

---

## 🎮 Demo Mode

Don't have API keys? No problem! DealLens includes a **demo mode** that returns realistic sample analysis data:

```bash
curl -X POST http://localhost:8000/api/analyze/demo \
  -H "Content-Type: application/json" \
  -d '{"company_name": "TechStart AI", "website_url": "https://example.com"}'
```

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)
| Variable | Required | Description |
|----------|----------|-------------|
| `GLM_API_KEY` | No* | Z.ai GLM-5.1 API key |
| `OPENAI_API_KEY` | No* | OpenAI GPT-4 API key |
| `JWT_SECRET_KEY` | No | Auto-generated if not set |
| `DATABASE_URL` | No | Default: SQLite |
| `CORS_ORIGINS` | No | Default: `http://localhost:3000` |

*\*At least one API key needed for live analysis. Demo mode works without keys.*

### Frontend (`frontend/.env.local`)
| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | No | Default: `http://localhost:8000` |

---

## 📡 API Documentation

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Create account |
| `POST` | `/api/auth/login` | Login & get token |
| `GET` | `/api/auth/me` | Get current user |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze` | Analyze a startup 🔒 |
| `POST` | `/api/analyze/demo` | Demo analysis (no auth) |
| `GET` | `/api/analyze/{id}` | Get analysis 🔒 |
| `DELETE` | `/api/analyze/{id}` | Delete analysis 🔒 |

### History & Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/history` | Analysis history 🔒 |
| `GET` | `/api/history/stats` | Statistics 🔒 |
| `GET` | `/api/profiles` | List fund profiles 🔒 |
| `POST` | `/api/profiles` | Create profile 🔒 |
| `PUT` | `/api/profiles/{id}` | Update profile 🔒 |
| `DELETE` | `/api/profiles/{id}` | Delete profile 🔒 |

🔒 = Requires JWT Authentication

Full interactive docs available at `/docs` when backend is running.

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance Python web framework |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Lightweight database (zero config) |
| **OpenAI SDK** | GPT-4 integration |
| **Trafilmatura** | Web scraping engine |
| **bcrypt** | Password hashing |
| **PyJWT** | JWT token management |
| **Pydantic** | Data validation |
| **Loguru** | Structured logging |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework (App Router) |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first styling |
| **React Context** | State management |
| **Fetch API** | HTTP client |

---

## 📁 Project Structure

```
deal-lens/
├── backend/
│   ├── app/
│   │   ├── config.py          # Settings & configuration
│   │   ├── database.py        # DB connection & session
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models/
│   │   │   ├── db_models.py   # SQLAlchemy models
│   │   │   └── schemas.py     # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── auth.py        # Auth endpoints
│   │   │   ├── analyze.py     # Analysis endpoints
│   │   │   ├── history.py     # History endpoints
│   │   │   └── profiles.py    # Profile endpoints
│   │   └── services/
│   │       ├── analyzer.py    # AI analysis engine
│   │       ├── auth_service.py # Auth & JWT logic
│   │       ├── prompts.py     # LLM prompt templates
│   │       └── scraper.py     # Web scraping service
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Landing page
│   │   ├── login/page.tsx     # Login/Signup
│   │   ├── dashboard/page.tsx # Dashboard
│   │   ├── analyze/page.tsx   # Analysis page
│   │   └── profiles/page.tsx  # Fund profiles
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   └── utils.ts           # Utility functions
│   ├── tailwind.config.ts
│   └── package.json
├── .gitignore
└── README.md
```

---

## 📊 Analysis Output Example

When you analyze a startup, DealLens generates:

```json
{
  "company_name": "TechStart AI",
  "one_liner": "AI-powered enterprise platform automating business workflows",
  "sector": "Enterprise AI / SaaS",
  "stage": "Series A",
  "problem_solution": "Problem & Solution analysis...",
  "target_market": "TAM: $45B | SAM: $12B | SOM: $800M",
  "business_model": "B2B SaaS, 78% gross margin",
  "team_assessment": "Strong technical founding team",
  "traction_signals": "$2.8M ARR, 42 enterprise clients",
  "competitive_landscape": "vs UiPath, Automation Anywhere",
  "fit_score": {
    "total": 78.5,
    "sector_match": 88.0,
    "stage_match": 82.0,
    "team_quality": 85.0,
    "market_size": 80.0,
    "verdict": "Strong Fit"
  }
}
```

---

## 🔮 Roadmap

- [ ] PDF report export
- [ ] Batch analysis (multiple startups)
- [ ] Team collaboration features
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Integration with Crunchbase / PitchBook APIs
- [ ] Chrome extension for quick analysis
- [ ] Multi-language support

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ for the VC community**

[⬆ Back to Top](#-deallens)

</div>