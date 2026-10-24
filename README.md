# 🛡️ Autonomous Fraud Investigation System

An AI-powered system that investigates complex fraud relationships between financial entities using Graph Intelligence (Neo4j Aura), Autonomous AI Agents (LangGraph), and Vector RAG (FAISS).

> ⚡ Unlike traditional rule-based filters that score transactions in complete isolation, this system **analyzes multi-hop entity graphs, explains investigations with audit trails, and coordinates event-driven fintech workflows**.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Next.js: 15](https://img.shields.io/badge/Next.js-15-black.svg)
![FastAPI: 1.0](https://img.shields.io/badge/FastAPI-1.0-teal.svg)

---

## 🌐 Live Deployments & Endpoints

| Service | URL | Status & Description |
|---|---|---|
| **Frontend SOC Console (Vercel)** | [https://autonomous-fraud-investigation.vercel.app](https://autonomous-fraud-investigation.vercel.app) | Live Next.js SOC console with live IST clock, telemetry, network graphs & alert triage |
| **Backend API (Render)** | [https://autonomous-fraud-investigation.onrender.com](https://autonomous-fraud-investigation.onrender.com) | Live FastAPI service with PostgreSQL database & Neo4j Aura integration |
| **Interactive API Documentation** | [https://autonomous-fraud-investigation.onrender.com/docs](https://autonomous-fraud-investigation.onrender.com/docs) | OpenAPI / Swagger UI for testing endpoints and schemas |
| **Production Health Probe** | [https://autonomous-fraud-investigation.onrender.com/health](https://autonomous-fraud-investigation.onrender.com/health) | Reports status, environment, active engine, and verified graph backend connectivity |

---

## 🧠 Problem Statement & Motivation

Traditional financial fraud detection architectures suffer from critical structural weaknesses:
1. **Isolated Transaction Evaluation**: Scored individually without relationship context or historical pattern matching across related accounts.
2. **High False-Positive Overhead**: Static threshold rules flag legitimate high-value customers while missing sophisticated multi-account velocity attacks.
3. **Black-Box Opacity**: Traditional ML classifiers output a probability without human-readable reasoning or actionable evidence for compliance officers.

### Modern Solution Architecture
Modern risk engineering combines:
- **Graph Intelligence**: Detecting entity sharing, circular fund movement, and multi-hop connections to known fraudulent syndicates.
- **Agentic AI Investigation**: Autonomous orchestration of tools (baseline profiling, anomaly checks, graph neighborhood analysis, and similar case vector matching).
- **RAG Grounding**: Case-law vector search ensuring investigations cite historical typologies (e.g. romance scams, crypto off-ramps, bust-out fraud).

---

## 🚀 Key Features

- **Continuous Fraud Risk Scoring & Deterministic Decision Thresholds**:
  - Risk score strictly bounded in `[0.0, 1.0]`.
  - `< 0.50` $\rightarrow$ **Allow** (Normal baseline activity).
  - `0.50 – 0.79` $\rightarrow$ **Hold / Manual Review** (Elevated anomaly, high velocity, or geographical deviation).
  - `≥ 0.80` $\rightarrow$ **Block + Manual Review** (Severe risk, direct fraud ring association, flagged beneficiary).
- **Graph Intelligence (Neo4j Aura + In-Memory Fallback)**:
  - Models users, devices, and financial transfers as a property graph.
  - Cypher-powered traversal finds shared devices, transfer chains, and connections to flagged bad actors.
  - Resilient design: automatically falls back to an in-memory graph from CSV datasets if Neo4j is offline, and self-heals when reconnected.
- **Dual Investigation Engine**:
  - **Claude-Powered Planner**: Multi-step LangGraph ReAct agent that autonomously selects investigation tools and constructs structured findings when an Anthropic API key is provided.
  - **Deterministic Rules Planner**: Zero-dependency weighted heuristic fallback that runs identically out-of-the-box without requiring third-party API keys.
- **RAG Knowledge Base (FAISS)**:
  - 30 indexed historical fraud typologies with vector embeddings for semantic matching.
- **Real-Time SOC Telemetry & Dashboard**:
  - Live **Asia/Kolkata (IST · UTC+05:30)** session clock and unambiguous timestamps.
  - Interactive force-directed network subgraphs and detailed agent reasoning step logs.
  - Financial amounts formatted safely in standard USD notation ($0.01 to $10,000,000.00).

---

## 🏗️ System Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Client["Frontend (Next.js 15 on Vercel)"]
        UI["SOC Dashboard / Console"]
        Form["Investigation Form"]
        GraphUI["Network Subgraph Viewer"]
    end

    subgraph Gateway["Backend (FastAPI on Render)"]
        Routes["API Router / Ingestion"]
        RateLimit["Rate Limiter (240 req/min)"]
        Auth["Security Layer (API Key / Webhook HMAC)"]
    end

    subgraph CoreEngine["Agentic Investigation Layer"]
        Planner{"Planner Engine"}
        ClaudeEngine["Claude 3.7 / 3.5 Sonnet (LangGraph)"]
        RulesEngine["Deterministic Weighted Engine (Scoring)"]
    end

    subgraph DataStorage["Data & Intelligence Layer"]
        PG[("PostgreSQL: Events & Investigations")]
        Neo4j[("Neo4j AuraDB / In-Memory Graph")]
        FAISS[("FAISS Vector Index: 30 Fraud Typologies")]
        CSVs[("Dataset CSVs: Users, Devices, Transactions")]
    end

    UI -->|REST / HTTPS| Routes
    Form -->|POST /investigate| Routes
    Routes --> RateLimit --> Auth
    Auth --> Planner
    Planner -->|ANTHROPIC_API_KEY Set| ClaudeEngine
    Planner -->|Fallback / Default| RulesEngine
    ClaudeEngine & RulesEngine -->|Execute Tools| Neo4j & FAISS & CSVs
    Routes -->|Persist History| PG
    GraphUI -->|GET /graph/:userId| Neo4j
```

---

## 💻 Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 15 (App Router), React 19, TypeScript, Vanilla CSS & Tailwind utilities, Canvas Particles & Globe |
| **Backend** | FastAPI, Python 3.11+, Pydantic v2, Uvicorn, Starlette |
| **Databases** | PostgreSQL (Relational schema via SQLAlchemy), Neo4j Aura (Graph DB), In-memory graph fallback |
| **Agent & RAG** | LangGraph, Anthropic Python SDK, FAISS (Facebook AI Similarity Search), Sentence Embeddings |
| **DevOps & Cloud** | Docker, Docker Compose, Render (Backend API), Vercel (Frontend), GitHub Actions |

---

## ⚖️ Fraud Scoring & Decision Thresholds

The backend evaluates risk factors across 4 distinct intelligence sources:
1. **Sender Baseline**: Historical 90-day volume, average amount, usual merchant categories, and signup longevity.
2. **Transaction Pattern**: Deviation ratio vs. average amount, unusual country of origin, off-hours initiation, and rapid 10-minute velocity.
3. **Graph Intelligence**: Shared physical devices ($N \ge 2$), transfer hops, and direct links to flagged accounts.
4. **Vector RAG**: Cosine similarity against known fraud patterns (similarity $\ge 0.35$ adds contextual penalty).

```
Score Range:    0.00 ──────────────── 0.49 ────── 0.50 ──────────────── 0.79 ────── 0.80 ──────────────── 1.00
Action:                  ALLOW                        HOLD / MANUAL REVIEW                     BLOCK
Meaning:         Low risk / Baseline verified         Suspicious anomaly / Velocity spike     Critical syndicate / Ring
```

---

## 🤖 AI / Agent Workflow & Dual Engine Execution

1. **Claude-Powered Mode**:
   - Activated when `ANTHROPIC_API_KEY` is configured in backend environment.
   - Claude evaluates incoming transaction parameters, dynamically queries tools via the tool registry (`get_user_history`, `check_transaction_pattern`, `get_linked_accounts`, `search_similar_cases`), and submits a structured `finalize_decision`.
2. **Deterministic Rules Mode (Default)**:
   - When `ANTHROPIC_API_KEY` is unset or if the Anthropic API encounters network interruption, the system degrades seamlessly to `_rules_planner`.
   - Executes the deterministic pipeline (`RULES_PLAN`), computes weighted anomaly scores, and generates human-readable audit explanations without crashing.

---

## 🔍 Graph Intelligence & Neo4j Integration

- **Entities**:
  - `User`: Account ID, flagged status.
  - `Device`: Unique device hardware signature.
- **Relationships**:
  - `(User)-[:USED_DEVICE]->(Device)`
  - `(User)-[:TRANSFERRED_TO]->(User)`
- **Live Incremental Updates**:
  - When new transactions are processed via `/transactions` or `/investigate`, the backend merges new nodes and updates relationship counts in real time.
- **Failover**:
  - If Neo4j Aura is unreachable, queries seamlessly execute against the in-memory graph constructed from `data/*.csv`. The backend periodically checks Neo4j connectivity and automatically reconnects once live.

---

## 🗄️ Database Schema & Entities

The relational database (PostgreSQL in production, SQLite in local dev) tracks two primary models:
1. **`TransactionEvent`**:
   - Raw ingestion records (`tx_id`, `user_id`, `receiver_id`, `amount`, `country`, `device_id`, `merchant_category`, `prefilter_risk`, `status`, `timestamp`).
2. **`Investigation`**:
   - Audit trail records (`id`, `tx_id`, `user_id`, `amount`, `fraud_score`, `confidence`, `action`, `reasons`, `reasoning_log`, `explanation`, `engine`, `created_at`).

---

## 📂 Repository Structure

```
FraudDetection/
├── backend/
│   ├── alembic/                 # Database migrations
│   ├── app/
│   │   ├── agents/              # LangGraph ReAct agent & rules scoring engine
│   │   ├── api/                 # FastAPI routes (/health, /investigate, /stats)
│   │   ├── core/                # Rate limiter and HMAC/API-key security
│   │   ├── db/                  # SQLAlchemy models and session initialization
│   │   ├── graph/               # Neo4j client and in-memory graph fallback
│   │   ├── rag/                 # FAISS vector store and embedding engine
│   │   └── tools/               # Registry for profiling and pattern tools
│   ├── tests/                   # Regression and boundary unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Next.js 15 App Router pages & layout
│   ├── components/              # SystemStatus, NetworkGraph, ScoreChart, LiveFeed
│   ├── lib/                     # API client and IST formatting utilities
│   ├── Dockerfile
│   └── package.json
├── data/                        # Sample users, devices, and transaction datasets
├── n8n/                         # Event automation workflow configurations
├── docker-compose.yml           # Complete multi-service orchestration
└── README.md
```

---

## 🛠️ Local Setup & Installation

### Option A: Manual Setup

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run frontend development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

### Option B: Docker Compose (All-in-One)

```bash
# Clone the repository
git clone https://github.com/sathwik27-ai/Autonomous_Fraud_Investigation.git
cd Autonomous_Fraud_Investigation/FraudDetection

# Copy environment template
cp .env.example .env

# Spin up all containers (Backend, Frontend, PostgreSQL, Neo4j)
docker compose up --build -d
```

- **Frontend Console**: [http://localhost:3000](http://localhost:3000)
- **Backend API & Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Neo4j Browser**: [http://localhost:7474](http://localhost:7474)

---

## 🧪 Testing Instructions

Run the backend test suite covering boundary thresholds, extreme amount validation, IST timezone handling, and health endpoints:

```bash
# From the FraudDetection directory:
# Windows (PowerShell):
$env:PYTHONPATH="backend"; python -m unittest backend/tests/test_production_issues.py

# Linux / macOS:
PYTHONPATH=backend python -m unittest backend/tests/test_production_issues.py
```

Run frontend linting and type checking:
```bash
cd frontend
npm run build
```

---

## 🔐 Environment Variables Reference

Copy `.env.example` to `.env` and configure credentials:

| Variable | Target | Description | Example / Default |
|---|---|---|---|
| `DATABASE_URL` | Backend | PostgreSQL database connection string | `postgresql://user:pass@host:5432/db` |
| `NEO4J_URI` | Backend | Neo4j Aura or local Bolt URI | `neo4j+s://xxxx.databases.neo4j.io` |
| `NEO4J_USER` | Backend | Neo4j authentication user | `neo4j` |
| `NEO4J_PASSWORD` | Backend | Neo4j authentication password | `your-secure-password` |
| `ANTHROPIC_API_KEY` | Backend | Anthropic Claude API Key (optional) | `sk-ant-...` (uses rules if blank) |
| `CORS_ORIGINS` | Backend | Allowed CORS origins | `https://autonomous-fraud-investigation.vercel.app` |
| `NEXT_PUBLIC_API_URL` | Frontend | Public Backend API base URL | `https://autonomous-fraud-investigation.onrender.com` |
| `NEXT_PUBLIC_API_KEY` | Frontend | API Key if required | *(leave blank if public)* |

---

## 📈 Known Limitations & Future Improvements

1. **Distributed Rate Limiting**: Transition from in-memory Starlette token-bucket to a Redis-backed distributed limiter for multi-replica horizontal scaling.
2. **Real-Time Streaming**: Ingest live card swipe authorization feeds via Apache Kafka or Redpanda.
3. **Advanced Graph ML**: Train inductive Graph Neural Networks (GNN / GraphSAGE) to compute dynamic node fraud embeddings alongside topological heuristics.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
