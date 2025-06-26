## ALM WebClient UI Test Automation Framework

### This is a Python-based UI Test Automation framework using **Playwright** and **Pytest** for testing the ALM WebClient application.

---

## Project Structure

```bash
alm25-web-client-test-automation-framework/
│
├── business/                # Business logic for workflows (login, submission, etc.)
│   ├── login_action.py
│   ├── requirements_action.py
│   └── submission_actions.py
│
├── pages/                   # Page object models for UI elements
│   ├── login_page.py
│   ├── requirements_page.py
│   └── submission_page.py
│
├── tests/                   # Test cases (pytest-based)
│   └── test_esig_submission.py
│
├── test_data/               # Test data files (JSON, CSV, etc.)
│   └── test_data.json
│
├── utilities/               # Utility classes and configs
│   ├── constants.py
│   ├── data_loader.py
│   ├── env_utils.py
│   ├── wait_utils.py
│   ├── .env                 # Environment secrets (created from example.env)
│   └── example.env
│
├── reports/                 # Test reports (Allure results, screenshots)
│   ├── allure-results/
│   └── screenshots/
│
├── test_runner.py           # Entry point to execute tests
├── conftest.py              # Pytest fixtures and hooks
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```


---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://gitlab.com/your-username/alm-ui-test-automation.git
cd alm-ui-test-automation
```

### 2. Create Virtual Environment & Activate

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate     # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Set up environment variables for credentials and base URL:

1.Go to utilities/ folder.

2.Copy example.env → .env.

3.Fill in actual values:

```bash
BASE_URL=https://your-base-url.com

SAAUTHOR=saauthor:yourpassword
SADEV=sadev:yourpassword
FAUSER=fauser:yourpassword
```

.env is ignored in version control. Keep it secure.

### 5. Allure Report Setup
To generate and view Allure reports:

Java Required: Allure requires Java 8 or higher.
Recommended: Install OpenJDK 21 (from company portal).

Install Allure CLI (using Scoop for Windows):

```bash
scoop install allure
```

You can verify it with:

```bash
allure --version
```

If scoop is not installed in your machine, please refer this link for installation:
https://scoop.sh/

### Running the Tests
Use the test_runner.py script to execute all tests and collect Allure results:

```bash
python test_runner.py
```

By default, this sets --maxfail=4, --disable-warnings, and generates Allure results in reports/allure-results/.

### View Test Reports
After test execution, run:

```bash
allure serve reports/allure-results
```

This will launch a live, interactive Allure dashboard in your browser.

Best Practices Followed

✅ Page Object Model (POM)

✅ Business Logic Layer

✅ Configurable .env support

✅ Allure reporting with screenshots

✅ Parametrized test data from JSON

✅ Modular and scalable folder structure