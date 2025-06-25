from utilities.wait_utils import WaitUtils
from pages.login_page import LoginPage
from utilities.env_utils import EnvUtils

class LoginActions:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.wait = WaitUtils(page)

    def login(self, username, password, base_url):
        base_url = EnvUtils.get_base_url()
        self.page.goto(base_url)
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_authenticate()
        self.wait.wait_for_element(self.login_page.login_button)
        self.login_page.click_login()
