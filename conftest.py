import pytest
import json
from playwright.sync_api import sync_playwright

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

@pytest.fixture(scope="function", params=json.load(open("test_data/test_data.json")))
def test_user_data(request):
    return request.param
