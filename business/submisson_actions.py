from pages.submission_page import EsigPopup
from utilities.wait_utils import WaitUtils
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

class SubmissionActions:
    def __init__(self, page):
        self.page = page
        self.popup = EsigPopup(page)
        self.wait = WaitUtils(page)


    def submit_esig_flow(self, user_data):
        max_attempts = 2
        attempts = 0

        while attempts < max_attempts:
            self.popup.open_esig_popup()
            frame = self.popup.get_frame()
            self.wait.wait_for_element(frame.locator("#phases"))

            # Check the current phase value
            phase_value = frame.locator("#phases").input_value()
            print(f"🌀 Detected phase: {phase_value}")

            if phase_value == "Routing For Approval(s)":
                print("✅ Phase is 'Draft' → Submitting for approval")
                self.popup.fill_comment(frame, comment="Submitting for approval")
                self.popup.submit_popup(frame)
                self.wait.wait_until_value(self.popup.get_phase_combobox(), "Routing For Approval(s)")
                attempts += 1
                continue  # Go back and reopen popup for approval assignment

            elif phase_value == "Approved":
                print("✅ Phase is 'Approved' → Assigning approvers")
                self.popup.select_approvers(frame, user_data["approvers"])
                self.popup.fill_comment(frame, comment="Assigning approvers")
                self.popup.submit_popup(frame)
                break  # Done

            elif phase_value == "Canceled":
                print("❌ Submission rejected: No rule defined or unauthorized user")
                break

            else:
                raise Exception(f"❌ Unknown eSig phase: '{phase_value}' — cannot proceed.")

        else:
            print("⚠️ Max submission attempts reached without successful approval flow.")