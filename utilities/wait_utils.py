import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

class WaitUtils:
    def __init__(self, page):
        self.page = page

    def wait_for_element(self, locator, timeout=20000):
        try:
            locator.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"Element not visible after {timeout}ms: {locator}")

    def wait_for_element_attached(self, locator, timeout=10000):
        try:
            locator.wait_for(state="attached", timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"Element not attached after {timeout}ms: {locator}")

    def wait_for_text(self, locator, timeout=20000):
        try:
            expect(locator).to_be_visible(timeout=timeout)
            actual_text = locator.inner_text(timeout=timeout).strip()
            if not actual_text:
                pytest.fail(f"Element is visible but contains no text after {timeout}ms.")
        except PlaywrightTimeoutError:
            pytest.fail(f"Element not visible or no text found after {timeout}ms.")

    def wait_until_value(self, locator, value, timeout=10000):
        try:
            expect(locator).to_have_value(value, timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"Value '{value}' not found in element after {timeout}ms")

    def wait_for_navigation(self, timeout=10000):
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"Page did not finish navigation after {timeout}ms")

    def wait_for_url(self, expected_url, timeout=10000):
        try:
            self.page.wait_for_url(expected_url, timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"URL did not match '{expected_url}' after {timeout}ms")

    def wait_for_dialog_title(self, title_text, timeout=10000):
        try:
            self.page.wait_for_selector(f"h2:has-text('{title_text}')", timeout=timeout)
        except PlaywrightTimeoutError:
            pytest.fail(f"Dialog title '{title_text}' not found after {timeout}ms")
