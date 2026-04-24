# ♻️ Smart Waste Routing System (IntelliRoute)

A production-grade, Explainable AI (XAI) logistics dashboard powered by a Hybrid GA-ACO (Genetic Algorithm + Ant Colony Optimization) routing engine.

This project bridges the gap between complex optimization algorithms and intuitive SaaS UX by providing real-time, explainable decision intelligence for smart city waste management.

---

# 📸 Dashboard Overview

> Add screenshots in `docs/images/` and update paths below

![Dashboard](docs/images/dashboard.png)
![Research Mode](docs/images/research.png)

---

# 🌟 Key Features

* **Hybrid GA-ACO Routing Engine**
  Combines genetic optimization with pheromone-based pathfinding for efficient routing.

* **Explainable AI (XAI) Drawer**
  Interactive panel explaining why nodes are selected or skipped.

* **Single Source of Truth (geo matching)**
  UI strictly reflects backend output using coordinate matching logic.

* **Predictive Node Filtering**
  Reduces unnecessary visits by prioritizing high-fill bins.

* **Research Validation Mode**
  Displays experimental results (distance reduction, RMSE, convergence).

---

# 🛠️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* React Leaflet
* Recharts

### Backend

* FastAPI
* Celery + Redis
* PostgreSQL
* NumPy / SciPy

---

# 📐 System Architecture

```text
Frontend (React)
        ↓
FastAPI Backend
        ↓
Redis (Queue)
        ↓
Celery Worker (GA-ACO Engine)
        ↓
PostgreSQL
```

---

# 🚀 Local Setup Guide

## ⚠️ Prerequisites

Make sure you have installed:

* Node.js (v18+)
* Python (3.10+)
* Docker & Docker Compose

---

# 🔥 Step 1 — Clone Repository

```bash
git clone https://github.com/mankitraj915/smart-waste-routing-system.git
cd smart-waste-routing-system
```

---

# 🔥 Step 2 — Backend Setup (Docker)

Start full backend stack:

```bash
docker-compose up --build
```

This will start:

* FastAPI → http://localhost:8000
* PostgreSQL
* Redis
* Celery Worker

---

# 🔥 Step 3 — Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

👉 http://localhost:5173

---

# 🔥 Step 4 — Environment Configuration (Optional)

### Backend `.env` (if needed)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db
REDIS_URL=redis://localhost:6379
```

### Frontend `.env`

```env
VITE_API_URL=http://localhost:8000
```

---

# 🧪 How to Test the System

1. Open frontend (http://localhost:5173)
2. Click **"Initiate Dispatch"**
3. Observe:

   * Route generation on map
   * Node selection
   * Explainable AI drawer

---

# 📈 Research Results

Based on experimental analysis:

* **Distance Reduction:** ~20–25% improvement over baseline
* **Node Pruning:** ~60% reduction in active nodes
* **Convergence:** Faster than standalone ACO

---

# 📂 Project Structure

```text
frontend/        → React dashboard
backend/         → FastAPI server
worker/          → Celery tasks
docs/            → screenshots & report
docker-compose.yml
```

---

# ⚠️ Common Issues & Fixes

### 1. Port already in use

```bash
docker-compose down
```

---

### 2. Frontend cannot reach backend

Check:

```env
VITE_API_URL=http://localhost:8000
```

---

### 3. Redis / Celery not working

Restart:

```bash
docker-compose down
docker-compose up --build
```

---

# 🔮 Future Scope

* Real-time fleet tracking (WebSockets)
* Traffic-aware routing
* Multi-vehicle optimization
* Predictive ML for waste generation

---

# 👨‍💻 Author

Ankit Raj
B.Tech CSE Capstone Project

---

# ⭐ Final Note

This project demonstrates:

* Full-stack system design
* AI + optimization integration
* Explainable decision systems
* SaaS-level UI architecture

If you found this useful, consider ⭐ starring the repository.
