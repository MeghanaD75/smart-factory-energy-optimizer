import pandas as pd

def sensor_agent(file):
    if file is None:
        return "Please upload a CSV file."

    df = pd.read_csv(file)

    # Select the latest 5 rows as recent data
    latest_data = df.tail(5)
    results = latest_data.to_dict(orient='records')

    return results
