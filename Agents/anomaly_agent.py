import pandas as pd

def anomaly_agent(file):
    if file is None:
        return "Please upload a CSV file."

    df = pd.read_csv(file)

    if 'energy_usage' not in df.columns:
        return "CSV must contain an 'energy_usage' column."

    mean = df['energy_usage'].mean()
    std_dev = df['energy_usage'].std()
    threshold = 2 * std_dev

    anomalies = df[df['energy_usage'] > mean + threshold]

    if anomalies.empty:
        return "✅ No anomalies detected in recent energy usage."
    else:
        return f"⚠️ Anomalies detected at rows: {anomalies.index.tolist()}"
