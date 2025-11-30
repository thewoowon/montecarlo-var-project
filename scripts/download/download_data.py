import yfinance as yf
import pandas as pd
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw"

os.makedirs(DATA_PATH, exist_ok=True)

tickers = {
    "KOSPI200": "069500.KS",
    "KTB3Y": "114820.KS",
    "KTB10Y": "148070.KS",
    "USD": "138230.KS",  # TIGER USD Money Market ETF
    "GOLD": "132030.KS"  # TIGER Gold Futures ETF
}

start = "2018-01-01"
end   = "2024-12-31"

def main():
    for name, tkr in tickers.items():
        print(f"Downloading {name}...")
        df = yf.download(tkr, start=start, end=end, progress=False)
        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.to_csv(DATA_PATH / f"{name}.csv")
        print(f"  Saved {name}: {df.shape[0]} rows")
    print("데이터 다운로드 완료!")

if __name__ == "__main__":
    main()
