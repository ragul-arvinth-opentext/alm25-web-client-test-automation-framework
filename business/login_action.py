from utilities.wait_utils import WaitUtils
from pages.login_page import LoginPage

class LoginActions:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.wait = WaitUtils(page)

    def login(self, username, password):
        self.page.goto("https://almqa503.aws.swinfra.net:8443/qcbin/webrunner/#/login")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_authenticate()
        self.wait.wait_for_element(self.login_page.login_button)
        self.login_page.click_login()
