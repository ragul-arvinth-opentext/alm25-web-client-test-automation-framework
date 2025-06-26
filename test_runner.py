import pytest
from pathlib import Path

def run_tests():
    allure_results_dir = Path("reports/allure-results")
    allure_results_dir.mkdir(parents=True, exist_ok=True)

    pytest_args = [
        "-v",
        "--maxfail=4",
        "--disable-warnings",
        f"--alluredir={allure_results_dir}",
        "tests/"#common to run all the tests
        # "tests/test_esig_submission.py"#Run only the test_esig_submisson
    ]

    result = pytest.main(pytest_args)

    print("\nTests completed.")
    print("Allure results saved to:", allure_results_dir.resolve())
    print("To generate and view the report, run the following commands in CMD:")
    print("\n    allure serve reports/allure-results\n")

    return result

if __name__ == "__main__":
    run_tests()
