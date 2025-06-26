"""
Pytest configuration and fixtures for web automation testing.
Provides browser context management and screenshot capture on test failures.
"""

# Standard library imports
import time
from pathlib import Path
from datetime import datetime

# Third-party imports
import pytest
import allure
import _pytest.terminal
from playwright.sync_api import sync_playwright

# Module-level initialization
if not hasattr(_pytest.terminal.TerminalReporter, "_sessionstarttime"):
    _pytest.terminal.TerminalReporter._sessionstarttime = time.time()


@pytest.fixture(scope="function")
def browser_context(request):
    """Launches browser and captures screenshot on failure."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page

        rep = getattr(request.node, "rep_call", None)
        if rep and rep.failed:
            screenshot_dir = Path("reports") / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{request.node.name}_{timestamp}.png"
            filepath = screenshot_dir / filename

            try:
                page.screenshot(path=str(filepath), full_page=True)
                allure.attach.file(
                    source=str(filepath),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"[!] Screenshot capture failed: {e}")

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to propagate test result to the request object so it can be accessed in fixture teardown.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)

    if call.when == "call":
        item.rep_call = rep

