# 🧠 Smart Waste Routing System (IntelliRoute)

A production-grade, Explainable AI (XAI) logistics dashboard powered by a Hybrid GA-ACO (Genetic Algorithm + Ant Colony Optimization) routing engine.

This capstone project bridges the gap between complex mathematical routing algorithms and intuitive SaaS UX by providing real-time, derived decision intelligence for smart city waste management.

---

## 📸 Dashboard Overview

![Dashboard Operations](docs/images/dashboard_operations.png)
*(Placeholder for actual dashboard screenshot)*

![Analytics Research Mode](docs/images/analytics_mode.png)
*(Placeholder for actual analytics screenshot)*

---

## 🌟 Key Features

1. **Hybrid GA-ACO Routing Engine**: Computes highly optimized geographic routes by fusing genetic crossover logic with pheromone-based pathfinding.
2. **Explainable AI (XAI) Drawer**: A dynamic, fixed right-side drawer that explains *why* the AI selected or skipped specific geographic nodes, updating flawlessly on map clicks.
3. **Strict Single Source of Truth**: The React frontend cross-references geographic coordinates natively using epsilon-proximity (`geo.js`) to guarantee the visual UI always matches the raw JSON output from the background workers.
4. **Predictive Node Filtering**: Intelligently identifies and isolates low-priority nodes to conserve fuel and time, presenting exactly how many nodes were pruned.
5. **Research Validation Mode**: Real-world experimental data backing the efficacy of the system against standard baseline approaches, dynamically rendered via Recharts.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19 + Vite
- **Styling**: Tailwind CSS v4
- **Maps**: React Leaflet
- **Icons & Charts**: Lucide React, Recharts

### Backend
- **API Framework**: FastAPI (Python)
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Database**: PostgreSQL
- **Algorithm Layer**: Hybrid GA-ACO (NumPy, SciPy)

---

## 📐 System Architecture

1. **Ingestion Layer**: Fast API securely accepts and stores telemetry data in PostgreSQL.
2. **Asynchronous Execution**: Intensive route calculations are instantly offloaded to a Celery Worker via Redis.
3. **Frontend Polling**: The React frontend polls the backend for completion without locking the UI.
4. **Decision Intelligence**: Frontend derives real-time visual explanations based solely on mathematical matching between the route output and the known telemetry nodes.

---

## 🚀 Setup Instructions

### Prerequisites
- Node.js (v18+)
- Docker & Docker Compose
- Python 3.10+

### Local Development

1. **Start the backend infrastructure (FastAPI, Postgres, Redis, Celery):**
   ```bash
   docker-compose up --build
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 📈 Research Results

Based on our experimental analysis stored in `frontend/src/data/research.json`:
- **Distance Reduction**: Consistently achieved significant travel distance reductions compared to naive nearest-neighbor baseline approaches.
- **Node Pruning**: Successfully isolated unneeded low-priority nodes, drastically reducing required fleet deployment time.
- **Convergence**: The Hybrid GA-ACO engine converges to optimal paths in fewer generations than standard ACO implementations.

---

## 🔮 Future Scope
- Real-time live fleet tracking integration via WebSockets.
- Dynamic rerouting based on active traffic APIs (e.g., Google Maps Distance Matrix).
- Advanced historic forecasting for predictive waste generation modeling.

---

## 👨‍💻 Author Details

Developed as an advanced engineering capstone project demonstrating production-grade SaaS design, full-stack orchestration, and artificial intelligence integration.
