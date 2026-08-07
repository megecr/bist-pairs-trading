import os
import yfinance as yf

selected_tickers = [ "GARAN.IS", "AKBNK.IS", "ISCTR.IS", "YKBNK.IS", "TUPRS.IS", 
    "EREGL.IS", "KCHOL.IS", "SAHOL.IS", "SISE.IS", "THYAO.IS", "BIMAS.IS" ]

# Getting the current directory where this folder resides
current_dir = os.path.dirname(os.path.abspath(__file__))

# Target folder where the CSV files will be saved
output_folder = os.path.join(os.path.dirname(current_dir), "data")

# If data folder doesn't exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"The download process is starting for a total of {len(selected_tickers)} selected tickers...")

for ticker in selected_tickers:
    try:
        print(f"Getting the daily values for {ticker}...")

        #Getting the daily values for the past 5 years
        data = yf.download(ticker, period="5y", interval="1d")

        if not data.empty:
            # Naming the output file as the ticker name
            file_name = f"{output_folder}/{ticker.replace('.IS', '')}.csv"

            data.to_csv(file_name)
            print(f"{file_name} is saved successfully")
        else:
            print(f"Error: no data was found for {ticker}")

    except Exception as e:
        print(f"Error: An error {e} happened while downloading {ticker}")

print("\nSuccesfully downloaded all of the data for the selected stocks")