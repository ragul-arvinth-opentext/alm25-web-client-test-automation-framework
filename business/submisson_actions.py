from pages.submission_page import EsigPopup
from utilities.wait_utils import WaitUtils

class SubmissionActions:
    def __init__(self, page):
        self.page = page
        self.popup = EsigPopup(page)
        self.wait = WaitUtils(page)

    def submit_for_approval(self, team):
        self.popup.click_esig_and_submit()
        frame = self.popup.get_frame()
        self.wait.wait_for_element(frame.locator("#phases"))

        if "author" in team.lower():
            self.popup.fill_comment_and_submit(frame)
            self.wait.wait_until_value(self.popup.get_phase_combobox(), "Routing For Approval(s)")
        else:
            self.wait.wait_until_value(frame.locator("#phases"), "Canceled")
