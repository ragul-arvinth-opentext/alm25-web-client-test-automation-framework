import pytest

if __name__ == "__main__":
    pytest_args = [
        "-v",
        "--maxfail=2",
        "--disable-warnings",
        "--html=reports/report.html",
        "--self-contained-html",
        "tests/"
    ]
    pytest.main(pytest_args)
