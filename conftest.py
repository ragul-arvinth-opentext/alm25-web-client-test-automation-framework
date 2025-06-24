import time
import pytest
import allure
import _pytest.terminal
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

if not hasattr(_pytest.terminal.TerminalReporter, "_sessionstarttime"):
    _pytest.terminal.TerminalReporter._sessionstarttime = time.time()

CONFIG = {
    "base_url": "https://almqa503.aws.swinfra.net:8443/qcbin/webrunner/#/login",
    "default_timeout": 5000
}

@pytest.fixture(scope="function")
def config():
    """Returns global configuration values."""
    return CONFIG

@pytest.fixture(scope="function")
def browser_context(request):
    """Launches browser and captures screenshot on failure."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to headless=True if needed
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page

        # After test — if it failed, take screenshot
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{request.node.name}_{timestamp}.png"
            filepath = screenshot_dir / filename

            # Take screenshot
            page.screenshot(path=str(filepath), full_page=True)

            # Attach to Allure
            with open(filepath, "rb") as f:
                allure.attach(
                    f.read(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Make the test result available to fixtures using item.rep_call.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)
