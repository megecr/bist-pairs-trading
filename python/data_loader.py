import os
import yfinance as yf

bist100_tickers = [
    "A1CAP.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS",
    "AKFGY.IS", "AKFYE.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ANSGR.IS",
    "ARCLK.IS", "ARDYZ.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENP.IS", "BIMAS.IS", "BINHO.IS",
    "BIOEN.IS", "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS",
    "CWENE.IS", "DOAS.IS", "DOHOL.IS", "ECILC.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS",
    "EREGL.IS", "EUPWR.IS", "EUREK.IS", "FROTO.IS", "GARAN.IS", "GESAN.IS", "GOKNR.IS", "GUBRF.IS",
    "GWIND.IS", "HALKB.IS", "HEKTS.IS", "ISCTR.IS", "ISGYO.IS", "ISMEN.IS", "KAYSE.IS",
    "KCAER.IS", "KCHOL.IS", "KLSER.IS", "KMPUR.IS", "KONTR.IS", "KORDS.IS", "KOZAL.IS", "KOZAA.IS",
    "KRDMD.IS", "KZGYO.IS", "MAVI.IS", "MGHOL.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OTKAR.IS",
    "OYAKC.IS", "PETKM.IS", "PGSUS.IS", "REAGR.IS", "SAHOL.IS", "SASA.IS", "SISE.IS",
    "SKBNK.IS", "SOKM.IS", "TAVHL.IS", "TCHOL.IS", "TKFEN.IS", "THYAO.IS", "TOASO.IS",
    "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUPRS.IS", "TURSG.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS",
    "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "AGROT.IS", "OBAMS.IS", "ENTRA.IS"
]

# Getting the current directory where this folder resides
current_dir = os.path.dirname(os.path.abspath(__file__))

# Target folder where the CSV files will be saved
output_folder = os.path.join(os.path.dirname(current_dir), "data")

# If data folder doesn't exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"The download process is starting for a total of {len(bist100_tickers)} selected tickers...")

for ticker in bist100_tickers:
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