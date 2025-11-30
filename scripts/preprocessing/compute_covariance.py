import pandas as pd
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
PROC = PROJECT_ROOT / "data" / "processed"

def main():
    returns = pd.read_csv(PROC / "returns.csv", index_col=0, parse_dates=True)

    cov20 = returns.rolling(20).cov().dropna()
    cov60 = returns.rolling(60).cov().dropna()

    cov20.to_pickle(PROC / "cov20.pkl")
    cov60.to_pickle(PROC / "cov60.pkl")

    print("공분산 계산 완료!")
    print(f"Cov20 shape: {cov20.shape}")
    print(f"Cov60 shape: {cov60.shape}")

if __name__ == "__main__":
    main()
