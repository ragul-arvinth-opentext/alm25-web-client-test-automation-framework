import pytest
import _pytest.terminal
from playwright.sync_api import sync_playwright

if not hasattr(_pytest.terminal.TerminalReporter, "_sessionstarttime"):
    for attr in dir(_pytest.terminal.TerminalReporter):
        if "start" in attr.lower():
            print(f"🛠 Possible replacement for _sessionstarttime found: {attr}")

    import time
    _pytest.terminal.TerminalReporter._sessionstarttime = time.time()


# Inline configuration dictionary
CONFIG = {
    "base_url": "https://almqa503.aws.swinfra.net:8443/qcbin/webrunner/#/login",
    "default_timeout": 5000
}

@pytest.fixture(scope="function")
def config():
    """Returns global configuration values."""
    return CONFIG

@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


