"""
Business logic layer for Electronic Signature and Submission operations.
Handles complex e-signature workflows and approval processes.
"""

# Project imports
from pages.submission_page import EsigPopup
from utilities.wait_utils import WaitUtils
from utilities.constants import (
    PHASE_APPROVED,
    PHASE_DRAFT,
    PHASE_REJECTED,
    PHASE_ROUTING,
    PHASE_CANCELLED
)


class SubmissionActions:
    """
    Business logic class for submission and e-signature operations.
    Orchestrates e-signature workflows and approval processes.
    """
    
    def __init__(self, page):
        """
        Initialize submission actions with page dependencies.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.popup = EsigPopup(page)
        self.wait = WaitUtils(page)

    def submit_esig_flow(self, user_data):
        """
        Execute the complete e-signature submission workflow.
        
        Args:
            user_data (dict): Dictionary containing user and approval data
        """
        max_attempts = 2
        attempts = 0

        while attempts < max_attempts:
            self.popup.open_esig_popup()
            frame = self.popup.get_frame()
            self.wait.wait_for_element(frame.locator("#phases"))

            # Check the next phase value
            phase_value = frame.locator("#phases").input_value()
            print(f"Detected phase: {phase_value}")

            if phase_value == PHASE_ROUTING:
                print("Phase is 'Draft' → Submitting for approval")
                self.popup.fill_comment(frame, comment="Submitting for approval")
                self.popup.submit_popup(frame)
                self.wait.wait_until_value(self.popup.get_phase_combobox(), "Routing For Approval(s)")
                attempts += 1
                continue  # Go back and reopen popup for approval assignment

            elif phase_value == PHASE_APPROVED:
                print("Phase is 'Approved' → Assigning approvers")
                self.popup.select_approvers(frame, user_data["approvers"])
                self.popup.fill_comment(frame, comment="Assigning approvers")
                self.popup.submit_popup(frame)
                break  # Done

            elif phase_value == PHASE_CANCELLED:
                print("Submission rejected: No rule defined or unauthorized user")
                break

            else:
                raise Exception(f"Unknown eSig phase: '{phase_value}' — cannot proceed.")

        else:
            print("Max submission attempts reached without successful approval flow.")

