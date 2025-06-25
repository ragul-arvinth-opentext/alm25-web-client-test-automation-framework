from utilities.constants import (
    BUTTON_AUTHENTICATE,
    BUTTON_LOGIN
)

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="User Name")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.authenticate_button = page.get_by_role("button", name=BUTTON_AUTHENTICATE)
        self.login_button = page.get_by_role("button", name=BUTTON_LOGIN)

    def enter_username(self, username):
        self.username_input.fill(username)

    def enter_password(self, password):
        self.password_input.fill(password)

    def click_authenticate(self):
        self.authenticate_button.click()

    def click_login(self):
        self.login_button.click()
