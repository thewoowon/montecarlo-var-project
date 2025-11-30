"""
Master Script: Run All Experiments for Paper
Executes all research questions (RQ1-RQ5) in sequence
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

def run_experiment(script_name, description):
    """Run a single experiment script"""
    print("\n" + "=" * 80)
    print(f"RUNNING: {description}")
    print("=" * 80)

    start_time = time.time()

    try:
        # Import and run the experiment
        if script_name == "convergence":
            from experiments import convergence_analysis
            convergence_analysis.main()
        elif script_name == "variance_reduction":
            from experiments import variance_reduction_analysis
            variance_reduction_analysis.main()
        elif script_name == "stress_backtesting":
            from experiments import stress_backtesting
            stress_backtesting.main()
        elif script_name == "boundary_conditions":
            from experiments import boundary_conditions
            boundary_conditions.main()

        elapsed = time.time() - start_time
        print(f"\n✅ {description} completed in {elapsed:.1f} seconds")
        return True

    except Exception as e:
        print(f"\n❌ {description} failed with error:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 80)
    print("MONTE CARLO vs QUASI-MONTE CARLO VaR/CVaR ANALYSIS")
    print("Full Experimental Pipeline")
    print("=" * 80)

    experiments = [
        ("convergence", "RQ1 & RQ3: Convergence Analysis (MC vs QMC)"),
        ("variance_reduction", "RQ2: Variance Reduction Techniques"),
        ("stress_backtesting", "RQ4: Stress Period Backtesting (2020/2022/2023)"),
        ("boundary_conditions", "RQ5: Boundary Condition Analysis"),
    ]

    results = {}
    total_start = time.time()

    for script_name, description in experiments:
        success = run_experiment(script_name, description)
        results[description] = "✅ Success" if success else "❌ Failed"

    total_elapsed = time.time() - total_start

    # Print summary
    print("\n" + "=" * 80)
    print("EXPERIMENTAL PIPELINE SUMMARY")
    print("=" * 80)

    for description, status in results.items():
        print(f"{status:12s} | {description}")

    print(f"\nTotal execution time: {total_elapsed:.1f} seconds ({total_elapsed/60:.1f} minutes)")

    # Check if all succeeded
    all_success = all("Success" in status for status in results.values())

    if all_success:
        print("\n" + "=" * 80)
        print("🎉 ALL EXPERIMENTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nResults saved to:")
        print(f"  - {PROJECT_ROOT / 'results' / 'simulation'}")
        print(f"  - {PROJECT_ROOT / 'results' / 'backtesting'}")
        print(f"  - {PROJECT_ROOT / 'plots'}")
        print("\nYou can now proceed to:")
        print("  1. Review results in CSV files")
        print("  2. Check plots in /plots directory")
        print("  3. Generate paper tables and figures")
    else:
        print("\n" + "=" * 80)
        print("⚠️  SOME EXPERIMENTS FAILED")
        print("=" * 80)
        print("Please check error messages above and fix issues.")

if __name__ == "__main__":
    main()
