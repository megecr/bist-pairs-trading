import os
import numpy as np
import pandas as pd

selected_tickers = [
    "A1CAP.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS",
    "AKFGY.IS", "AKFYE.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALFAS.IS", "ANSGR.IS",
    "ARCLK.IS", "ARDYZ.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIMAS.IS", "BINHO.IS",
    "BIOEN.IS", "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS",
    "CWENE.IS", "DOAS.IS", "DOHOL.IS", "ECILC.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS",
    "EREGL.IS", "EUPWR.IS", "FROTO.IS", "GARAN.IS", "GESAN.IS", "GOKNR.IS", "GUBRF.IS",
    "GWIND.IS", "HALKB.IS", "HEKTS.IS", "ISCTR.IS", "ISGYO.IS", "ISMEN.IS", "KAYSE.IS",
    "KCAER.IS", "KCHOL.IS", "KLSER.IS", "KMPUR.IS", "KONTR.IS", "KORDS.IS",
    "KRDMD.IS", "KZGYO.IS", "MAVI.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OTKAR.IS",
    "OYAKC.IS", "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS",
    "SKBNK.IS", "SOKM.IS", "TAVHL.IS", "TKFEN.IS", "THYAO.IS", "TOASO.IS",
    "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUPRS.IS", "TURSG.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS",
    "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "AGROT.IS", "OBAMS.IS", "ENTRA.IS"
]

print("--- Results ---")

for ticker_name in selected_tickers:
    ticker_name = ticker_name.replace(".IS", "")
    df = pd.read_csv(f"../data/{ticker_name}.csv")

    df['daily_change'] = df['Close'].diff()
    df['lag'] = df['Close'].shift(1)

    df_clean = df.dropna(subset=['daily_change', 'lag'])

    ones_col = np.ones(len(df_clean))
    matrix = np.column_stack((ones_col, df_clean['lag'].values))
    matrix_t = matrix.T

    matrix_multiplication = matrix_t @ matrix
    inv_matrix_multiplication = np.linalg.inv(matrix_multiplication)

    y = df_clean['daily_change'].values
    coefficients = inv_matrix_multiplication @ (matrix_t  @ y)

    intercept = coefficients[0] #Drift
    gamma = coefficients[1] #Gamma in ADF test

    y_pred = matrix @ coefficients #Predicting data according to our model
    residuals = y - y_pred  #Finding the error between the predicted data nad our real data

    n = len(y)
    degrees_of_freedom = n - 2
    residual_variance = np.sum(residuals ** 2) / degrees_of_freedom

    vcov = residual_variance * inv_matrix_multiplication

    se_gamma = np.sqrt(vcov[1,1])

    adf_stat = coefficients[1] / se_gamma #This value is our Dickey-Fuller test statistic
    
    print(f"Results for {ticker_name}: ")
    print(f"Gamma (γ): {coefficients[1]:.6f}")  
    print(f"Gamma Standard: {se_gamma:.6f}")
    print(f"ADF Test Statistic : {adf_stat:.6f}") #Lower than -2.86 is stationary, greater than -2.86 non-stationary
    if adf_stat < -2.86:
        print(f"{ticker_name} is stationary")
        
    print("\n")

results_dir = "../results"
os.makedirs(results_dir, exist_ok=True)

file_paths = {
    "strongly": os.path.join(results_dir, "strongly_cointegrated.txt"),
    "moderately": os.path.join(results_dir, "moderately_cointegrated.txt"),
    "weakly": os.path.join(results_dir, "weakly_cointegrated.txt"),
    "not": os.path.join(results_dir, "not_cointegrated.txt")
}

for path in file_paths.values():
    with open(path, "w", encoding="utf-8") as f:
        f.write("Stock1,Stock2,t_stat\n")

df = pd.read_csv("../data/paired_stocks.csv")

for i in range(0, len(df)):
    stock1_name = df["Stock1"][i].replace(".IS", "")
    stock2_name = df["Stock2"][i].replace(".IS", "")

    df_1 = pd.read_csv((f"../data/{stock1_name}"))
    df_2 = pd.read_csv((f"../data/{stock2_name}"))

    merged_df = pd.merge(df_1[["Price", "Close"]], df_2[["Price", "Close"]], on="Price", suffixes=("_1", "_2")).dropna()

    Y_t = merged_df['Close_1'].values
    X_t = merged_df['Close_2'].values
    ones_col = np.ones(len(merged_df))

    M = np.column_stack((ones_col, merged_df['Close_2'].values))
    M_t = M.T

    M_multiplication = M_t @ M
    inv_M_multiplication = np.linalg.inv(M_multiplication)

    beta = inv_M_multiplication @ M_t @ Y_t

    e_t = Y_t - (beta[0] + beta[1] * X_t)

    e_t_array = e_t.values if hasattr(e_t, "values") else np.array(e_t)
    Ye_t = e_t_array[1:] - e_t_array[:-1]
    Xe_t = e_t_array[:-1]

    gamma = (Xe_t @ Ye_t) / (Xe_t @ Xe_t)

    Y_predicted = gamma * Xe_t
    u = Ye_t - Y_predicted

    N = len(Ye_t)

    sigma_squared = (u @ u) / (N - 1)
    SE_gamma = np.sqrt(sigma_squared / (Xe_t @ Xe_t)) # Standard Error gamma

    t_stat = gamma / SE_gamma

    print(f"t-stat: {t_stat:.4f}")

    #MacKinnon Values
    CRITICAL_1_PERCENT = -3.39
    CRITICAL_5_PERCENT = -2.76
    CRITICAL_10_PERCENT = -2.45

    if t_stat < CRITICAL_1_PERCENT:
        print(f"{stock1_name} and {stock2_name} is strongly cointegrated, strong long-term relationship")
        target_file = file_paths["strongly"]
    elif t_stat < CRITICAL_5_PERCENT:
        print(f"{stock1_name} and {stock2_name} is moderately cointegrated, significant long-term relationship")
        target_file = file_paths["moderately"]
    elif t_stat < CRITICAL_10_PERCENT:
        print(f"{stock1_name} and {stock2_name} is weakly cointegrated, relationship is fragile")
        target_file = file_paths["weakly"]
    else:
        print(f"{stock1_name} and {stock2_name} is not cointegrated, no long-term relationship")
        target_file = file_paths["not"]

    with open(target_file, "a", encoding="utf-8") as f:
        f.write(f"{stock1_name},{stock2_name},{t_stat:.4f}\n")
