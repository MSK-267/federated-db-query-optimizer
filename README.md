🌐 Federated DB Query Optimizer  
Python 3.11 · PostgreSQL · MongoDB · Docker · License: MIT

The **Federated DB Query Optimizer** is a **federated query processing system** that enables a *single logical query* to be executed across **heterogeneous databases**, specifically **PostgreSQL (relational)** and **MongoDB (document-oriented)**, using a **cost-based query optimizer**.

This project demonstrates the **core principles behind modern federated database systems**, including logical query planning, cost-based optimization, predicate pushdown, and cross-database execution — without requiring users to manually split or coordinate queries.

Built for **database systems coursework and academic evaluation**, with an emphasis on **clarity, correctness, and architectural soundness**.

---

## ✨ Key Features

### 🎯 Federated Query Execution
- Single-query execution across PostgreSQL and MongoDB
- Unified query interface over heterogeneous data models
- Centralized result merging at the coordinator

### 🧠 Cost-Based Query Optimization
- Logical → physical query plan transformation
- Join order optimization
- Predicate pushdown to source databases
- Source-aware execution decisions

### ⚡ Efficient Execution Model
- Reduced cross-database data movement
- Join placement based on estimated cost
- Optimized vs baseline execution comparison

### 🧪 Academic & Systems-Focused Design
- Clean operator abstraction
- Readable optimizer logic
- Deterministic demos for evaluation
- Reproducible architecture via Docker

---

## 📈 System Overview

| Metric | Value |
|------|------|
| Databases Supported | PostgreSQL, MongoDB |
| Query Model | Federated |
| Optimizer | Heuristic Cost-Based |
| Execution Engine | Single-node Coordinator |
| Target Use | Systems Coursework / Research |
| SQL Coverage | Subset (Select, Join, Filter, Group) |

---

## 🏗️ Architecture
┌──────────────────────────────────────────────┐
│ Federated Query Optimizer Architecture │
└──────────────────────────────────────────────┘
│
User Query
│
▼
Query Parser
│
▼
Logical Plan
(Operator Tree)
│
▼
Cost-Based Optimizer
│
▼
Execution Engine
┌────────────┴────────────┐
▼ ▼
[PostgreSQL Connector] [MongoDB Connector]
│ │
└────────────┬────────────┘
▼
Result Merger
│
▼
Final Output

---

## 🧩 Technology Stack

### Backend
- **Language**: Python 3.11
- **Query Engine**: Custom logical & physical operators
- **Optimization**: Heuristic cost estimation model

### Databases
- **PostgreSQL 16+** — relational query execution
- **MongoDB 6+** — document-based execution

### Infrastructure
- **Docker Compose** — multi-database orchestration
- **Virtual Environments** — dependency isolation

---

## 🧠 Optimizer Design

The optimizer evaluates multiple candidate execution plans using a **heuristic cost model** that considers:

- Estimated cardinality of intermediate results
- Predicate selectivity
- Join placement cost
- Cross-database data transfer overhead
- Source-specific execution efficiency

The final plan minimizes **total estimated execution cost**, not just local execution time.

---

## 🔬 Query Scope (Prototype)

Supported query features include:
- `SELECT`
- `FROM`
- `WHERE`
- Basic `JOIN`
- Simple `GROUP BY`

Not supported:
- Nested subqueries
- Window functions
- Transactions
- Stored procedures

This scoped design is **intentional** and aligned with academic objectives.

---

## 📂 Project Structure

federated-db-query-optimizer/
├── main.py # Query engine entry point
├── demo.py # Federated query demo
├── demo_timing.py # Optimized vs baseline timing
├── demo_force_legacy.py # Baseline execution path
├── optimizer/ # Cost model & plan selection
├── executor/ # Physical execution operators
├── connectors/ # PostgreSQL & MongoDB adapters
├── bench/ # Benchmark scripts
├── docker-compose.yml # Database orchestration
├── requirements.txt
└── README.md

---

## ⚠️ Limitations

- Partial SQL support (prototype scope)
- No distributed transaction management
- Single-node coordinator
- Heuristic (non-statistical) cost model

These limitations are **expected** for a pedagogical federated database system.

---

## 🛣️ Roadmap

- Runtime statistics–driven cost model
- Rule-based query rewrite phase
- Query plan visualization
- Support for additional data sources
- Automated regression tests

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📧 Contact

Project Author  
GitHub: https://github.com/MSK-267  

⭐ If this project helped demonstrate federated database concepts, please consider starring the repositor

