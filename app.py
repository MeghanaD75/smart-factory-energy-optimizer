# ----------------- Asyncio Event Loop Fix for Windows Only -----------------
import sys
import platform
import asyncio

if platform.system() == "Windows" and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ----------------- Streamlit Config (Must be first Streamlit command) -----------------
import streamlit as st
st.set_page_config(page_title="Smart Factory Energy Optimizer", layout="centered")

# ----------------- Other Imports -----------------
import pandas as pd
import tempfile
from PyPDF2 import PdfReader
from transformers import pipeline

# ----------------- Initialize LLM -----------------
@st.cache_resource(show_spinner=True)
def load_pipeline():
    return pipeline("text2text-generation", model="google/flan-t5-base")

qa_pipeline = load_pipeline()

# ----------------- Title and Instructions -----------------
st.title("🏭 Smart Factory Energy Optimizer")
st.write("Upload CSV sensor data and PDF guidelines. Ask queries to agents to get energy optimization insights.")

# ----------------- File Upload Section -----------------
uploaded_csv = st.file_uploader("📊 Upload CSV Sensor Data", type="csv")
uploaded_pdf = st.file_uploader("📄 Upload PDF Guidelines", type="pdf")

sensor_data = None
doc_text = ""

# ----------------- Load CSV and ensure energy_usage column -----------------
if uploaded_csv is not None:
    try:
        sensor_data = pd.read_csv(uploaded_csv)
        if 'energy_usage' not in sensor_data.columns:
            if 'Power_Consumption (kW)' in sensor_data.columns:
                sensor_data['energy_usage'] = sensor_data['Power_Consumption (kW)']
            else:
                st.error("❌ CSV must contain 'energy_usage' or 'Power_Consumption (kW)' column.")
                sensor_data = None
        else:
            st.success("✅ CSV loaded successfully.")
    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")

# ----------------- Extract PDF Text -----------------
if uploaded_pdf is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            reader = PdfReader(tmp_file.name)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    doc_text += text + "\n"
        st.success("✅ PDF processed successfully.")
    except Exception as e:
        st.error(f"❌ Error processing PDF: {e}")

# ----------------- Agent Functions -----------------
def sensor_agent(df):
    try:
        if df is not None:
            last_rows = df.tail(5).to_dict(orient='records')
            return "\n".join([f"{row}" for row in last_rows])
        return "⚠️ No sensor data available."
    except Exception as e:
        return f"❌ Error in Sensor Agent: {e}"

def anomaly_agent(df):
    try:
        if df is not None and 'energy_usage' in df.columns:
            mean = df['energy_usage'].mean()
            std = df['energy_usage'].std()
            threshold = mean + 2 * std
            anomalies = df[df['energy_usage'] > threshold]
            if anomalies.empty:
                return "✅ No anomalies detected in recent energy usage."
            return "\n".join([f"{row}" for row in anomalies.tail(5).to_dict(orient='records')])
        return "⚠️ 'energy_usage' column missing or no sensor data uploaded."
    except Exception as e:
        return f"❌ Error in Anomaly Agent: {e}"

def optimization_agent(query, context):
    try:
        if not context.strip():
            return "⚠️ No PDF content available for optimization."
        if not query.strip():
            return "⚠️ Enter a valid question."
        input_text = f"Context: {context}\n\nQuestion: {query}"
        result = qa_pipeline(input_text, max_length=256, do_sample=False)[0]["generated_text"]
        return result.strip()
    except Exception as e:
        return f"❌ Error in Optimization Agent: {e}"

def report_agent(df):
    try:
        if df is not None and 'energy_usage' in df.columns:
            avg = df['energy_usage'].mean()
            peak = df['energy_usage'].max()
            min_ = df['energy_usage'].min()
            return f"""📋 Energy Report:
- Average Usage: {avg:.2f}
- Peak Usage: {peak:.2f}
- Minimum Usage: {min_:.2f}"""
        return "⚠️ Sensor data missing or 'energy_usage' column not found."
    except Exception as e:
        return f"❌ Error in Report Agent: {e}"

# ----------------- Query Section -----------------
query = st.text_input("💬 Ask your question about energy optimization:")

if st.button("Run Agents") and query:
    st.subheader("🤖 Agent Responses")

    st.markdown("### 📡 Sensor Agent")
    st.info(sensor_agent(sensor_data))

    st.markdown("### ⚠️ Anomaly Agent")
    st.info(anomaly_agent(sensor_data))

    st.markdown("### 💡 Optimization Agent")
    st.info(optimization_agent(query, doc_text))

    st.markdown("### 📊 Report Agent")
    st.info(report_agent(sensor_data))
