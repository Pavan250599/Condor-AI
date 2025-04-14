# Import necessary libraries
import requests
import pandas as pd
from datetime import datetime
import os

# Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "81MRRZQ2VEHEBF76")
SYMBOL = "RELIANCE.BSE"
OUTPUT_SIZE = "full"
DOWNLOAD_FORMAT = "both"
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "stock_data")  # Save in user's home directory

#Function for fetching stock data
def fetch_stock_data():
    
    """
    Fetch historical stock data from Alpha Vantage API
    """

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": OUTPUT_SIZE,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    print(f"Fetching historical data for {SYMBOL}...")

    try:
        # Save to a custom absolute path
        OUTPUT_DIR = "/workspaces/codespaces-jupyter/Assignment/data"  # Codespaces-specific path

        response = requests.get("https://www.alphavantage.co/query", params=params)
        response.raise_for_status()
        data = response.json()

        if "Time Series (Daily)" not in data:
            error_msg = data.get("Note", data.get("Error Message", "Unknown error"))
            raise ValueError(f"API Error: {error_msg}")

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)

        # Clean and rename columns
        df.columns = [col.split(". ")[1].capitalize() for col in df.columns]
        df.index.name = "Date"
        df = df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        }).sort_index()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{SYMBOL}_historical_{timestamp}"

        # Save files
        saved_files = []
        if DOWNLOAD_FORMAT in ["csv", "both"]:
            csv_filename = os.path.join(OUTPUT_DIR, f"{base_filename}.csv")
            df.to_csv(csv_filename)
            saved_files.append(csv_filename)

        if DOWNLOAD_FORMAT in ["json", "both"]:
            json_filename = os.path.join(OUTPUT_DIR, f"{base_filename}.json")
            df.to_json(json_filename, orient="records")
            saved_files.append(json_filename)

        # Display results
        print("\n✅ Data successfully saved to:")
        for file in saved_files:
            print(f"- {file}")

        print("\n🔍 Data Preview (Last 5 Trading Days):")
        print(df.tail(5))

        return df

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Error processing data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    fetch_stock_data()