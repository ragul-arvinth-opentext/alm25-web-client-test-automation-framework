"""
Business logic layer for Electronic Signature and Submission operations.
Handles complex e-signature workflows and approval processes.
"""

# Project imports
import pytest
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
            self.popup.open_esig_popup()  # Opens the e-signature modal
            frame = self.popup.get_frame()  # Switch to iframe inside popup
            self.wait.wait_for_element(frame.locator("#phases"))  # Wait until phase field is ready

            # Fetch the current eSig phase value
            phase_value = frame.locator("#phases").input_value()
            print(f"Detected phase: {phase_value}")

            if phase_value == PHASE_ROUTING:
                # Phase is Draft → Move to Routing for Approval
                print("Phase is 'Draft' → Submitting for approval")
                self.popup.fill_comment(frame, comment="Submitting for approval")

                # SUBMISSION step might trigger dialog popup if approval is already ongoing
                dialog_text = self.popup.submit_popup(frame)

                # If dialog appears indicating submission is blocked (already in approval), handle it
                if dialog_text and "has not completed the e-signature approval process" in dialog_text:
                    print("Approvers already assigned or approval process still running.")
                    break  # Stop flow, nothing more to do

                # Confirm UI reflects transition to 'Routing For Approval(s)'
                self.wait.wait_until_value(self.popup.get_phase_combobox(), "Routing For Approval(s)")
                attempts += 1
                continue  # Reopen popup to assign approvers in next loop

            elif phase_value == PHASE_APPROVED:
                # Once requirement reaches "Approved", assign approvers
                print("Phase is 'Approved' → Assigning approvers")
                self.popup.select_approvers(frame, user_data["approvers"])
                self.popup.fill_comment(frame, comment="Assigning approvers")

                # Submission may again show a dialog if already assigned
                dialog_text = self.popup.submit_popup(frame)

                if dialog_text and "has not completed the e-signature approval process" in dialog_text:
                    print("Approvers already assigned")
                    pytest.fail(
                        "Approvers already assigned, Submission Invalid. "
                        f"Dialog Box Message: {dialog_text}"
                    )
                    break  # Stop assigning again

                break  # Done assigning approvers

            elif phase_value == PHASE_CANCELLED:
                print("Submission rejected: No rule defined or unauthorized user.")
                break

            else:
                # Unexpected value encountered
                pytest.fail(
                    f"Unknown eSig phase: '{phase_value}' — cannot proceed. "
                    f"Expected one of: [{PHASE_ROUTING}, {PHASE_APPROVED}, {PHASE_CANCELLED}, {PHASE_DRAFT}, {PHASE_REJECTED}]"
                )

        else:
            # Max attempts reached, approval flow did not succeed
            print("Max submission attempts reached without successful approval flow.")

