import pandas as pd
import numpy as np
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
os.makedirs(PROCESSED_PATH, exist_ok=True)

def main():
    kospi = pd.read_csv(RAW_PATH / "KOSPI200.csv", index_col=0, parse_dates=True)
    ktb3y = pd.read_csv(RAW_PATH / "KTB3Y.csv", index_col=0, parse_dates=True)
    ktb10y = pd.read_csv(RAW_PATH / "KTB10Y.csv", index_col=0, parse_dates=True)

    # Check available columns and use appropriate price column
    price_col = "Adj Close" if "Adj Close" in kospi.columns else "Close"

    prices = pd.DataFrame({
        "KOSPI200": kospi[price_col],
        "KTB3Y": ktb3y[price_col],
        "KTB10Y": ktb10y[price_col]
    }).dropna()

    returns = np.log(prices / prices.shift(1)).dropna()
    returns.to_csv(PROCESSED_PATH / "returns.csv")

    print("수익률 계산 완료!")
    print(f"Returns shape: {returns.shape}")
    print(f"Date range: {returns.index[0]} to {returns.index[-1]}")

if __name__ == "__main__":
    main()
