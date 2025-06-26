"""
Page Object Model for Login Page.
Contains locators and basic interactions for the login page.
"""

# Project imports
from utilities.constants import (
    BUTTON_AUTHENTICATE,
    BUTTON_LOGIN
)


class LoginPage:
    """
    Page Object for Login functionality.
    Encapsulates login page elements and basic interactions.
    """
    
    def __init__(self, page):
        """
        Initialize login page with Playwright page object.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self._initialize_locators()
    
    def _initialize_locators(self):
        """Initialize all page element locators."""
        self.username_input = self.page.get_by_role("textbox", name="User Name")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.authenticate_button = self.page.get_by_role("button", name=BUTTON_AUTHENTICATE)
        self.login_button = self.page.get_by_role("button", name=BUTTON_LOGIN)

    def enter_username(self, username):
        """Enter username in the username field."""
        self.username_input.fill(username)

    def enter_password(self, password):
        """Enter password in the password field."""
        self.password_input.fill(password)

    def click_authenticate(self):
        """Click the authenticate button."""
        self.authenticate_button.click()

    def click_login(self):
        """Click the login button."""
        self.login_button.click()