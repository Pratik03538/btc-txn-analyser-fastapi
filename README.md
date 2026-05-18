<div align="center">

# ⛓️ BTC Transaction Analyser & Dashboard

### Real-Time Bitcoin Blockchain Explorer & Scam Detection Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white">
  <img src="https://img.shields.io/badge/Blockchain-Bitcoin-orange?style=for-the-badge">
</p>

### ⚡ Lightning-Fast Blockchain Intelligence Engine

</div>

---

# 🌍 Overview

**BTC Transaction Analyser & Dashboard** is a modern blockchain analytics platform built using **FastAPI**, **SQLite**, and asynchronous Python architecture.

The application fetches live Bitcoin blockchain transaction data, stores it locally, and visualizes blockchain activity through a premium dashboard interface with analytics, address tracking, and scam detection capabilities.

This project is designed for:

- Blockchain Analytics
- Bitcoin Transaction Monitoring
- Wallet Investigation
- Scam Detection Research
- Educational Blockchain Exploration
- BTC Fee & Volume Analysis

---

# 🚀 Core Features

## ⚡ High-Speed Async Architecture

- Built with **FastAPI** + asynchronous `httpx`
- Non-blocking blockchain requests
- Handles large transaction batches efficiently
- Fast real-time synchronization

---

## 🗄️ Optimized Local Database

- SQLite database engine
- WAL (Write-Ahead Logging) enabled
- High-speed bulk transaction inserts
- Lightweight & portable storage system

---

## 🔍 Deep Bitcoin Transaction Explorer

Track complete BTC transaction details:

- Transaction Hash
- Inputs & Outputs
- Witness Data
- Miner Fees (sats/vB)
- Transaction Weight
- Replace-By-Fee (RBF) Detection
- Raw Blockchain Data

---

## 📊 Real-Time Analytics Dashboard

Interactive charts powered by **Chart.js**

Includes:

- Transactions Per Block
- Fee Trend Analysis
- Blockchain Activity Tracking
- Live Transaction Statistics

---

## 🕵️ Wallet Address Intelligence

Analyze any Bitcoin wallet address instantly:

- Total Received
- Total Sent
- Final Balance
- Address Transaction History
- Wallet Activity Insights

---

## 🚨 Scam Detection Analytics

Experimental analytics module for detecting:

- Suspicious wallet activity
- Abnormal transaction patterns
- Repeated interaction behavior
- Potential scam transaction flows

---

## 📥 CSV Export Support

Export synchronized blockchain data locally:

- CSV format
- Excel compatible
- Data-science ready
- Pandas compatible

---

# 📸 Dashboard Previews

## 🖥️ Main Dashboard

<p align="center">
  <img width="1912" height="961" alt="Screenshot 2026-05-18 223912" src="https://github.com/user-attachments/assets/76d80c40-96a0-482e-8702-92d53d376a87" />

</p>

> 

---

## 📊 Analytics & Wallet Tracking

<p align="center">
  <img width="1902" height="958" alt="Screenshot 2026-05-18 224038" src="https://github.com/user-attachments/assets/0c7ee0e2-ea75-4bdd-8ac1-146c3d636748" />

</p>

> 

---

# 📁 Project Structure

```text
btc-txn-analyser-fastapi/
│
├── main.py
├── requirements.txt
├── README.md
├── btc_data.db
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── exports/
│   └── transactions.csv
│
└── __pycache__/
```

---

# 📋 Prerequisites

Before starting, ensure the following are installed:

| Requirement | Version |
|---|---|
| Python | 3.9+ |
| Git | Latest |
| SQLite | Embedded |

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Pratik03538/btc-txn-analyser-fastapi.git

cd btc-txn-analyser-fastapi
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🖥️ Running The Application

## Start FastAPI Server

```bash
uvicorn main:app --reload
```

> Replace `main:app` if your entry file has a different name.

---

# 🌐 Open Dashboard

Visit:

```text
http://127.0.0.1:8000
```

---

# 🔄 Fetch Blockchain Data

1. Open the dashboard
2. Click **Fetch Blocks**
3. The system will:
   - Connect to blockchain APIs
   - Fetch latest BTC blocks
   - Parse transaction data
   - Store it locally
   - Update charts in real-time

---

# 🏗️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| API Server | Uvicorn |
| Database | SQLite3 |
| Frontend | HTML5 + TailwindCSS |
| Charts | Chart.js |
| Async Requests | httpx |
| Data Processing | Pandas + asyncio |

---

# 💎 Performance Highlights

- Async architecture for maximum throughput
- Lightweight local database engine
- Real-time analytics rendering
- Minimal memory overhead
- Optimized blockchain parsing
- Fast dashboard response times

---

# ⚠️ Disclaimer

This project is intended strictly for:

- Educational purposes
- Blockchain analytics
- Security research
- Data visualization

The scam detection module provides **experimental analytics only** and should not be considered financial, legal, or investigative advice.

Always independently verify blockchain data before making financial decisions.

---

# ⭐ Support The Project

If you found this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🛠️ Contribute improvements
- 🧠 Share feedback

---

# 📜 License

This project is licensed under the MIT License.

---

<div align="center">

### 🚀 Built for High-Speed Blockchain Intelligence

</div>
