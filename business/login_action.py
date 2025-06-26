"""
Business logic layer for Login operations.
Handles complex login workflows and interactions.
"""

# Project imports
from utilities.wait_utils import WaitUtils
from utilities.env_utils import EnvUtils
from pages.login_page import LoginPage


class LoginActions:
    """
    Business logic class for login operations.
    Orchestrates login page interactions and validation.
    """
    
    def __init__(self, page):
        """
        Initialize login actions with page dependencies.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.login_page = LoginPage(page)
        self.wait = WaitUtils(page)

    def login(self, username, password, base_url=None):
        """
        Execute complete login workflow.
        
        Args:
            username (str): User login name
            password (str): User password
            base_url (str, optional): Base URL to navigate to
        """
        if base_url is None:
            base_url = EnvUtils.get_base_url()
            
        self.page.goto(base_url)
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_authenticate()
        self.wait.wait_for_element(self.login_page.login_button)
        self.login_page.click_login()
