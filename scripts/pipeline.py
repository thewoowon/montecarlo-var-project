"""
Full Pipeline: Data Download -> Preprocessing -> All Experiments
"""

import os
import sys
from pathlib import Path

def main():
    print("=" * 80)
    print("MONTE CARLO vs QUASI-MONTE CARLO VaR/CVaR")
    print("Complete Research Pipeline")
    print("=" * 80)

    # Step 1: Data Download
    print("\n[STEP 1/4] Downloading market data...")
    ret = os.system("python3 download/download_data.py")
    if ret != 0:
        print("❌ Data download failed!")
        sys.exit(1)

    # Step 2: Compute Returns
    print("\n[STEP 2/4] Computing returns...")
    ret = os.system("python3 preprocessing/compute_returns.py")
    if ret != 0:
        print("❌ Returns computation failed!")
        sys.exit(1)

    # Step 3: Compute Covariance
    print("\n[STEP 3/4] Computing covariance matrices...")
    ret = os.system("python3 preprocessing/compute_covariance.py")
    if ret != 0:
        print("❌ Covariance computation failed!")
        sys.exit(1)

    print("\n✅ Data preparation complete!")

    # Step 4: Run All Experiments
    print("\n[STEP 4/4] Running all experiments...")
    print("\nThis will run:")
    print("  - RQ1 & RQ3: Convergence Analysis")
    print("  - RQ2: Variance Reduction Techniques")
    print("  - RQ4: Stress Period Backtesting")
    print("  - RQ5: Boundary Condition Analysis")

    response = input("\nProceed with experiments? This may take 20-30 minutes. (y/n): ")
    if response.lower() == 'y':
        ret = os.system("python3 run_all_experiments.py")
        if ret != 0:
            print("❌ Some experiments failed!")
            sys.exit(1)
    else:
        print("\nSkipping experiments. You can run them later with:")
        print("  python3 scripts/run_all_experiments.py")

    print("\n" + "=" * 80)
    print("🎉 PIPELINE COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Review results in /results directory")
    print("  2. Check plots in /plots directory")
    print("  3. Use results to write your paper!")

if __name__ == "__main__":
    main()
