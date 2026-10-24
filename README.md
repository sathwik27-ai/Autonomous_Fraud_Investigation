# 🛡️ Autonomous Fraud Investigation System

An AI-powered system that not only detects fraud but investigates relationships between entities using Graph Intelligence, AI Agents, and RAG-based reasoning.

> ⚡ Unlike traditional fraud detection systems that only score transactions, this system **analyzes networks, explains decisions, and simulates real-world fintech investigation workflows**.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🌐 Live Deployments & Endpoints

| Service | URL | Notes |
|---|---|---|
| **Backend API (Render)** | [https://fraud-investigation-backend.onrender.com](https://fraud-investigation-backend.onrender.com) | Live FastAPI service |
| **Interactive API Docs** | [https://fraud-investigation-backend.onrender.com/docs](https://fraud-investigation-backend.onrender.com/docs) | Swagger UI for exploring & testing endpoints |
| **Health Check** | [https://fraud-investigation-backend.onrender.com/health](https://fraud-investigation-backend.onrender.com/health) | Reports status & active graph backend |
| **Frontend Dashboard** | Deployable on Vercel / Render | See deployment guide below |

---

## 🚀 Features

- 🧠 **AI-Based Fraud Detection**
  - Risk scoring using intelligent rules + ML-style logic
- 🌐 **Graph Intelligence (Neo4j + In-Memory Fallback)**
  - Detects hidden relationships between users, devices, and transactions
- 🔍 **Relationship-Based Fraud Analysis**
  - Identifies fraud rings, shared devices, suspicious clusters
- 📊 **Interactive Dashboard**
  - Real-time visualization of fraud insights, live transaction feed, and interactive subgraph
- 🤖 **AI Investigation Agent**
  - Explains *why* a transaction is fraudulent using Claude or deterministic rule-engine
- 📚 **RAG (Retrieval-Augmented Generation)**
  - Uses past fraud cases (FAISS vector store) to ground decisions in historical context
- 🔗 **Automation Ready (n8n)**
  - Extendable to real-world alerting and compliance workflows

---

## 🧠 Problem Statement

### Traditional fraud detection systems:
- Work on **isolated transactions**
- Generate **high false positives**
- Lack **explainability**

### Modern systems are shifting toward:
- Graph-based fraud detection
- AI-driven investigation pipelines
- Explainable decision systems

👉 This project simulates that **next-generation fraud investigation system**.

---

## 🏗️ System Architecture

```
Frontend (Next.js 15 Dashboard on Vercel)
         │  (HTTPS / REST)
         ▼
Backend API (FastAPI on Render: https://fraud-investigation-backend.onrender.com)
   ┌─────┴─────────────────────────┐
   │                               │
   ▼                               ▼
Relational DB (PostgreSQL)    Graph DB (Neo4j / AuraDB / Memory Fallback)
   │                               │
   └───────────────┬───────────────┘
                   ▼
      Agentic AI Engine (Claude / Rules) + RAG (FAISS)
```

---

## 📊 Workflow

1. User submits transaction / `user_id`
2. Backend calculates fraud risk score
3. Graph DB analyzes relationships and shared entities
4. RAG retrieves similar historical fraud cases
5. AI Agent synthesizes evidence and generates structured explanation
6. Frontend displays:
   - Risk Score & Action (Approve / Review / Block)
   - Graph Intelligence & Cluster Links
   - Full Investigation Report & Reasoning Log

---

## 🖥️ Tech Stack

### 🔹 Backend
- FastAPI
- Python 3.11+ / 3.12
- SQLAlchemy & Alembic
- FAISS (Vector Store for RAG)

### 🔹 Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS

### 🔹 Databases
- PostgreSQL (Relational Data & Investigation History)
- Neo4j (Graph Database for Entity Links & Fraud Rings)

### 🔹 AI Layer
- RAG (Custom embeddings + FAISS)
- AI Agents (Claude / Deterministic Weighted Rule Engine)

### 🔹 DevOps
- Docker & Docker Compose
- Render (Backend deployment)
- Vercel (Frontend deployment)

---

## ☁️ Cloud Deployment Guide

### 1. Deploying the Frontend (Vercel)

The frontend is built with **Next.js 15** and includes `vercel.json` for zero-configuration deployment on **Vercel**:

1. Go to [Vercel](https://vercel.com) and click **"Add New Project"**.
2. Select your repository: `https://github.com/sathwik27-ai/Autonomous_Fraud_Investigation.git`.
3. Configure the project:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
4. In **Environment Variables**, add:
   ```env
   NEXT_PUBLIC_API_URL=https://fraud-investigation-backend.onrender.com
   NEXT_PUBLIC_API_KEY=
   ```
5. Click **Deploy**. Your dashboard will be live on `https://your-project.vercel.app`!

---

### 2. Connecting Cloud PostgreSQL (Render / Neon / Supabase)

By default, the backend operates on SQLite or fallback storage. To connect persistent PostgreSQL:

1. Create a free PostgreSQL instance on **[Render](https://render.com)**, **[Neon.tech](https://neon.tech)**, or **[Supabase](https://supabase.com)**.
2. Copy the connection string. Both `postgresql://` and `postgres://` formats are supported.
3. In your **Render Dashboard** → Backend Web Service (`fraud-investigation-backend`) → **Environment**:
   - Add `DATABASE_URL`:
     ```env
     DATABASE_URL=postgresql://user:password@hostname:5432/dbname?sslmode=require
     ```
4. Save and restart. The backend automatically initializes and verifies all tables (`investigations`, `transaction_events`) on startup!

---

### 3. Connecting Cloud Neo4j (Neo4j AuraDB Free)

The backend has an automatic fallback to an in-memory graph built from datasets (`users.csv`, `user_devices.csv`, `transactions.csv`).

To connect a managed cloud Neo4j instance:

1. Sign up for **[Neo4j AuraDB Free](https://neo4j.com/cloud/platform/aura-graph-database/)** (100% free cloud instance).
2. Create an instance and save the credentials.
3. In your **Render Dashboard** → Backend Service → **Environment**, add:
   ```env
   NEO4J_URI=neo4j+s://<your-instance-id>.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=<your-auradb-password>
   ```
4. Trigger a restart. When verified, `/health` will report:
   ```json
   {"status": "ok", "graph_backend": "neo4j"}
   ```

---

### 4. Backend Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | No | `sqlite:///./fraud.db` | PostgreSQL connection URL (Render/Neon/Supabase) |
| `NEO4J_URI` | No | `bolt://localhost:7687` | Neo4j URI (`neo4j+s://` for AuraDB, `bolt://` for local) |
| `NEO4J_USER` | No | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | No | `fraudgraph` | Neo4j password |
| `CORS_ORIGINS` | No | `*` | Allowed origins (comma-separated or `*` for all) |
| `ANTHROPIC_API_KEY` | No | `""` | Claude API key (if empty, uses deterministic rule engine) |
| `API_KEY` | No | `""` | Optional secret key for endpoint protection (`X-API-Key`) |
| `WEBHOOK_SECRET` | No | `""` | Optional HMAC key for secure ingestion webhooks |

---

## 💻 Local Setup (Docker Compose)

### 🔹 Prerequisites
- Docker Desktop
- Git

### 🔹 Run the Project Locally

```bash
# 1. Clone the repository
git clone https://github.com/sathwik27-ai/Autonomous_Fraud_Investigation.git
cd Autonomous_Fraud_Investigation

# 2. Setup environment file
cp .env.example .env

# 3. Start all services (Backend, Frontend, Postgres, Neo4j, n8n)
docker compose up --build
```

### 🔹 Access Local Applications

- 🌐 **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- ⚙️ **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🧠 **Neo4j Browser**: [http://localhost:7474](http://localhost:7474)
- 🔁 **n8n Automation**: [http://localhost:5678](http://localhost:5678)

---

## 📈 Impact

1. Detects fraud beyond rule-based systems
2. Uses graph relationships instead of isolated data
3. Reduces false positives using network intelligence
4. Simulates real fintech fraud investigation pipelines
5. Modern fraud systems increasingly rely on:
   - Graph analysis
   - AI reasoning
   - Real-time pipelines

---

## 🔥 Key Highlight

💡 “This system doesn’t just detect fraud — it investigates it.”

---

## 🧪 Example Use Case & Decision Output

1. User A makes a transaction.
2. System detects:
   - Same device used by 3 accounts
   - Suspicious transfer pattern
3. Graph reveals fraud ring.
4. AI explains decision:

```
Fraud Score: 0.99
Confidence: High
Action: Block + Manual Review

Reasons:
1. Transaction is 8.54x the sender's average of $304.42
2. Transaction from AE — outside the sender's usual countries
3. Initiated at an unusual hour (2:00)
4. High-risk merchant category: crypto_exchange
5. Graph link to 5 flagged account(s): U020, U033, U051, U052
6. Matches known fraud pattern 'crypto_offramp' (case C014, similarity 0.41)
```

---

## 🧩 Future Improvements

1. Real-time streaming (Kafka / Redpanda)
2. Advanced ML models (XGBoost / LightGBM)
3. Cloud deployment scaling (AWS / GCP Kubernetes)
4. Real payment gateway webhooks (Stripe / Adyen)
5. Production-grade distributed monitoring (Prometheus + Grafana)

---

## 👨‍💻 Contributors

This project was collaboratively developed as part of an AI-driven fraud investigation system.

| Contributor | Role |
|---|---|
| **Sathwik** | Backend Development, AI Agent Design, Graph Intelligence, System Architecture |
| **Rochita** | Frontend Development, Dashboard Design, Integration, Testing, Documentation |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
