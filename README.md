
# 🛡️ LogSentinel AI: Zero-Day Infrastructure Guard

**LogSentinel AI** is a high-scale security observability system designed to detect "Zero-Day" anomalies in cloud infrastructure logs. By utilizing **Self-Supervised Learning (SSL)** and **Vector Similarity Search**, LogSentinel identifies suspicious system behaviors that bypass traditional rule-based alerts.

### 🚀 Key Technical Highlights
*   **Semantic Anomaly Detection:** Unlike traditional regex-based log monitors, LogSentinel uses a **distilled BERT architecture** (`all-MiniLM-L6-v2`) to capture the "structural grammar" of system logs.
*   **Enterprise-Scale Vector Engine:** Powered by **Zilliz Cloud (Managed Milvus)**, enabling sub-second similarity searches across millions of log entries using **Data Partitioning** and **Auto-Indexing**.
*   **Zero-Day Forensics:** When an "Out-of-Distribution" log pattern is detected (low semantic similarity), the system triggers an autonomous **GenAI Security Analyst** via **Groq** to provide immediate risk assessment.
*   **Hybrid Data Architecture:** Combines unstructured log embeddings with structured metadata (Timestamps, Log Levels, and Regional Partitions) for multi-dimensional filtering.

### 🛠️ The Stack
*   **Vector Database:** Zilliz Cloud (Milvus)
*   **Inference (Brain):** Llama-3.1-8b-instant via **Groq**
*   **SSL Encoder:** BERT-based Sentence Transformers
*   **Deployment:** Streamlit
*   **Dataset:** [LogHub HDFS (Hadoop Distributed File System)](https://www.kaggle.com/datasets/ayenuryrr/loghub-hdfs-hadoop-distributed-file-system-data)

### 🏗️ How it Works
1.  **Ingestion:** Raw HDFS logs are parsed and truncated for semantic integrity.
2.  **Embedding:** Each log line is mapped into a 384-dimensional latent space.
3.  **Search:** The **Sentinel Scan** queries Zilliz to find the "Nearest Known Normal" behavior.
4.  **Analysis:** If the similarity score falls below a specific threshold (the "Semantic Noise Floor"), **Groq** analyzes the delta between the known and unknown log to determine the threat type (e.g., Buffer Overflow, Injection, or Hardware Failure).


**Data Schema**


```sql
/* 
  ZILLIZ (MILVUS) COLLECTION SCHEMA 
  Collection Name: logs_collection
  Metric Type: COSINE
*/

CREATE COLLECTION logs_collection (
    primary_key INT64 AUTO_ID,          -- Primary Key
    vector FLOAT_VECTOR(384),           -- BERT-based SSL Embeddings
    timestamp VARCHAR(100),             -- Log Event Time
    log_level VARCHAR(20),              -- INFO, WARN, FATAL
    message VARCHAR(2048)               -- Raw Log Content (Truncated)
);
```

### 📦 Setup & Installation
1. **Clone the repo:** `git clone https://github.com/TorshaMajumder/LogSentinel-AI.git`
2. **Install requirements:** `pip install -r requirements.txt`
3. **Database Setup:** 
   * Create a Zilliz Cloud cluster and a collection named `logs_collection` (384 Dimensions).
   * Ensure your IP is **whitelisted** in the Zilliz Security settings.
4. **Environment Variables:** Provide your `ZILLIZ_ENDPOINT`, `ZILLIZ_TOKEN`, and `GROQ_API_KEY` in the Streamlit sidebar.
5. **Run the Sentinel Console:** `streamlit run app.py`

---

## 🚀 Live Demo

<div align="center">
  <video src="YOUR_DRAGGED_LINK_HERE" width="100%" autoplay loop muted playsinline></video>

  <br/>

</div>


---

