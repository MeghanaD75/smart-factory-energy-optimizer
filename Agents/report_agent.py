import pandas as pd

def report_agent(file):
    if file is None:
        return "Please upload a CSV file."

    df = pd.read_csv(file)

    if 'energy_usage' not in df.columns:
        return "CSV must contain an 'energy_usage' column."

    avg_usage = df['energy_usage'].mean()
    peak_usage = df['energy_usage'].max()
    min_usage = df['energy_usage'].min()

    report = f"""📋 Energy Report:

Average Usage: {avg_usage:.2f}
Peak Usage: {peak_usage:.2f}
Minimum Usage: {min_usage:.2f}"""

    return report
