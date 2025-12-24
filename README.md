# Federated DB Query Optimizer

A **federated query engine prototype** that executes a single logical query across **PostgreSQL** and **MongoDB**, selecting an execution plan using a **cost-based optimizer**. :contentReference[oaicite:1]{index=1}

> Status: prototype / coursework-style system. Expect rough edges and incomplete SQL coverage.

---

## What this project does

This project provides a minimal “federated DBMS” workflow:

1. **Parse** an input query
2. **Plan** it into an operator tree (scan / filter / join / group / sort, etc.)
3. **Optimize** the plan with basic cost estimation (choose join order, pushdowns when possible)
4. **Execute** subplans on:
   - PostgreSQL for relational data
   - MongoDB for document/event-style data
5. **Combine** results and return them to the user

---

## Key features

- **Federated execution** across PostgreSQL + MongoDB :contentReference[oaicite:2]{index=2}  
- **Cost-based optimization** (prototype-level) :contentReference[oaicite:3]{index=3}
- Simple demos/bench scripts to compare “optimized vs legacy” execution behavior
- Docker Compose workflow for local setup (recommended)

---

## Repository layout (high-level)

Typical layout in this repo:

- `main.py` — primary entry point / CLI runner
- `demo*.py` — demo runners for specific scenarios (timing, forcing legacy plans, etc.)
- `docker-compose.yml` — local Postgres + Mongo setup
- `exec/connectors/` — database connectors / adapters
- `bench/` — benchmarking scripts / helpers

(If your folder names differ slightly, edit this section.)

---

## Prerequisites

- Python 3.10+ (3.11+ recommended)
- Docker + Docker Compose (recommended for local DBs)
- A running PostgreSQL instance and a running MongoDB instance

---

## Quickstart (recommended: Docker Compose)

### 1) Start databases
```bash
docker compose up -d
