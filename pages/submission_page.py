from utilities.wait_utils import WaitUtils
from utilities.constants import (
    BUTTON_SUBMIT_FOR_APPROVAL,
    BUTTON_ESIGN,
    SUBMIT_FOR_APPROVAL_LABEL 
)
class EsigPopup:
    def __init__(self, page):
        self.page = page

    def open_esig_popup(self):
        self.page.get_by_role("button", name=BUTTON_ESIGN).click()
        self.page.get_by_text(BUTTON_SUBMIT_FOR_APPROVAL).click()

    def get_frame(self):
        return self.page.frame_locator("iframe")

    def select_approvers(self, frame, approvers: dict):
        for team_id, approver_list in approvers.items():
            dropdown = frame.locator(f"select#{team_id}")
            WaitUtils(self.page).wait_for_navigation()
            print(f"Selecting {approver_list} for {team_id}")
            dropdown.select_option(approver_list)

    def fill_comment(self, frame, comment="Automated submission"):
        frame.locator("#comment").click()
        frame.locator("#comment").fill(comment)

    def submit_popup(self, frame):
    # Handle potential alert that may block frame actions
        def handle_dialog(dialog):
            print(f"Dialog appeared: {dialog.message}")
            dialog.dismiss()

        self.page.once("dialog", handle_dialog)

        self.page.get_by_label("Submit for Approval").locator("div").filter(has_text="Submit for Approval").click()
        frame.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        self.page.get_by_role("button", name="Refresh").click()
        return self.page.get_by_role("combobox", name="Phase :")
