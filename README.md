# LLM DataOps Pipeline for Multilingual Text Analytics

A production-grade pipeline for collecting, preprocessing, analyzing, and visualizing multilingual unstructured text using modern NLP and MLOps tools.

## 🚀 Project Goals
- Build a complete pipeline from raw text collection to NLP analysis (NER, NMT)
- Automate operations using Bash + Python scripting
- Deploy and monitor the system with Docker, Kubernetes, Prometheus, and Grafana
- Provide an interactive API and dashboard for NLP results

## 🧱 Architecture

📥 Data Ingestion (Python + Bash cron) 
🧹 Data Cleaning (Python, langdetect, regex) 
🧠 NLP Models (NER, NMT - HuggingFace Transformers, PyTorch) 
🛢️ Storage (PostgreSQL, pgvector) 
📡 API (FastAPI) 
📊 Dashboard (Superset or Streamlit) 
☁️ Deployment (Docker, Kubernetes, Helm) 
📈 Monitoring (Prometheus, Grafana)


## 🛠️ Tech Stack

| Layer       | Tech                                |
|-------------|--------------------------------------|
| Data        | Python, langdetect, BeautifulSoup    |
| NLP         | Transformers, PyTorch, HuggingFace   |
| API         | FastAPI                              |
| Storage     | PostgreSQL, pgvector                 |
| Automation  | Bash, crontab                        |
| Ops/Deploy  | Docker, Kubernetes, Helm             |
| Monitoring  | Prometheus, Grafana                  |
| Dashboard   | Superset, Streamlit                  |

## 📦 Features
- Multilingual text ingestion (news/blogs/etc.)
- Named Entity Recognition (NER) and Neural Machine Translation (NMT)
- Periodic execution with crontab and Bash scripts
- Prometheus metrics export for monitoring
- Grafana dashboard for pipeline performance
- Helm chart for Kubernetes deployment

## 📈 Sample Dashboard
![grafana_sample](./screenshots/grafana_metrics.png)

## 📑 Future Work
- LangChain or DeepSeek integration for LLM tasks
- RAG-based document querying with VectorDB
- Real-time inference API (e.g., Cloud Run or Lambda)

