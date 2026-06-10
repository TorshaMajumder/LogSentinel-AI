import os
import yaml
from groq import Groq
import streamlit as st
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer



def main(config):
    # Config
    st.set_page_config(page_title="LogSentinel AI", layout="wide")
    st.title("🛡️ LogSentinel: Zero-Day Infrastructure Guard")

    # Sidebar for Keys
    with st.sidebar:
        zilliz_uri = st.text_input("Zilliz Endpoint", type="password")
        zilliz_token = st.text_input("Zilliz Token", type="password")
        groq_key = st.text_input("Groq API Key", type="password")

        st.divider()
        st.subheader("Quick Test Samples")
        sample_type = st.selectbox("Choose a sample log:", ["Select...", "Normal Log", "Security Threat", "System Crash"])
        
        if sample_type == "Normal Log":
            sample_text = "INFO dfs.DataNode$DataXceiver: Receiving block blk_123 src: /10.250.19.102:54106"
        elif sample_type == "Security Threat":
            sample_text = "WARN auth: Unauthorized access attempt from IP 192.168.1.50 using 'admin' credentials."
        elif sample_type == "System Crash":
            sample_text = "FATAL: Out of memory (OOM) killer terminated process 4056 (java)."
        else:
            sample_text = ""

    if zilliz_uri and zilliz_token and groq_key:
        # Initialize
        client = MilvusClient(uri=zilliz_uri, token=zilliz_token)
        model = SentenceTransformer(config["embedding_model_name"])
        groq_client = Groq(api_key=groq_key)

        # UI
        st.write("### 🔍 Real-time Log Analysis")
        # Then in your main UI text area:
        new_log = st.text_area("Paste a log line to analyze:", value=sample_text)
        # new_log = st.text_area("Paste a log line to analyze:", placeholder="e.g. INFO dfs.DataNode: Receiving block...")

        if st.button("Scan for Anomalies"):
            # Vector Search
            query_vec = model.encode(new_log).tolist()
            results = client.search(
                collection_name="logs_collection",
                partition_names=["hdfs"],
                data=[query_vec],
                limit=1,
                output_fields=["message"],
                search_params={"metric_type": "COSINE"}
            )

            score = results[0][0]['distance']
            st.metric("Semantic Similarity Score", f"{score:.4f}")

            # Logic
            if score < 0.45: # Adjust this threshold based on your data
                st.error("🚨 POTENTIAL ZERO-DAY ANOMALY DETECTED")
                
                # GenAI Analyst
                with st.spinner("Analyzing threat signature..."):
                    prompt = f"Analyze this suspicious log: {new_log}. Closest normal log was: {results[0][0]['entity']['message']}. Explain the security risk."
                    explanation = groq_client.chat.completions.create(
                        model=config["groq_model_name"],
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.subheader("Cybersecurity Analysis")
                    st.info(explanation.choices[0].message.content)
            else:
                st.success("✅ Log Pattern Recognized: Normal Operations.")

    else:
        st.info("Enter your credentials in the sidebar to start the Sentinel.")



if __name__ == "__main__":

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_to_config = os.path.join(ROOT_DIR, "config.yaml")
    
    with open(path_to_config, 'r') as file:
        config = yaml.safe_load(file)
    
    main(config)