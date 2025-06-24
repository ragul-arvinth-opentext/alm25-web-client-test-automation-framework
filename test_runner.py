import pytest

if __name__ == "__main__":
    pytest_args = [
        "-v",
        "--maxfail=4",
        "--disable-warnings",
        "--html-report=./reports",
        '--title="eSign Submission"',
        "tests/"
    ]
    pytest.main(pytest_args)

