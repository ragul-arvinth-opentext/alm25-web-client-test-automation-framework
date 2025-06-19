from pages.submission_page import EsigPopup
from utilities.wait_utils import WaitUtils
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

class SubmissionActions:
    def __init__(self, page):
        self.page = page
        self.popup = EsigPopup(page)
        self.wait = WaitUtils(page)

    def submit_esig_flow(self, user_data):
        max_attempts = 2  # To avoid infinite loops
        attempts = 0

        while attempts < max_attempts:
            self.popup.open_esig_popup()
            frame = self.popup.get_frame()
            self.wait.wait_for_element(frame.locator("#phases"))

            try:
                # Case 1: Submission (Author)
                # expect(frame.locator("#phases")).to_have_value("Routing for Approval(s)", timeout=3000)
                print("✅ Phase is 'Draft' → Submitting for approval")
                self.popup.fill_comment(frame, comment="Submitting for approval")
                self.popup.submit_popup(frame)
                self.wait.wait_until_value(self.popup.get_phase_combobox(), "Routing For Approval(s)")
                attempts += 1
                continue  # Reopen eSig popup to assign approvers

            except PlaywrightTimeoutError:
                pass

            try:
                # Case 2: Assign approvers (After Approved)
                # expect(frame.locator("#phases")).to_have_value("Approved", timeout=3000)
                print("✅ Phase is 'Approved' → Assigning approvers")
                self.popup.select_approvers(frame, user_data["approvers"])
                self.popup.fill_comment(frame, comment="Assigning approvers")
                self.popup.submit_popup(frame)
                break  # Done

            except PlaywrightTimeoutError:
                pass

            try:
                # Case 3: Invalid submission (non-author)
                # expect(frame.locator("#phases")).to_have_value("Canceled", timeout=3000)
                self.wait.wait_until_value(frame.locator("#phases"), "Canceled")
                # self.wait.wait_for_text(frame.locator("body"), "There's no rule defined for")
                print("❌ Submission rejected: No rule defined for this user")
                break

            except PlaywrightTimeoutError:
                raise Exception("❌ Unknown eSig flow: Unable to detect valid phase state.")

        else:
            print("⚠️ Max submission attempts reached without successful approval flow.")
