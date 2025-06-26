"""
Page Object Model for Electronic Signature and Submission functionality.
Contains locators and basic interactions for e-signature workflows.
"""

# Project imports
from utilities.wait_utils import WaitUtils
from utilities.constants import (
    BUTTON_SUBMIT_FOR_APPROVAL,
    BUTTON_ESIGN,
    SUBMIT_FOR_APPROVAL_LABEL,
    BUTTON_SUBMIT,
    BUTTON_REFRESH
)


class EsigPopup:
    """
    Page Object for Electronic Signature Popup functionality.
    Encapsulates e-signature popup elements and basic interactions.
    """

    def __init__(self, page):

         """
        Initialize e-signature popup with Playwright page object.

        Args:
            page: Playwright page object
        """
         self.page = page

    def open_esig_popup(self):
        """Open the electronic signature popup."""
        self.page.get_by_role("button", name=BUTTON_ESIGN).click()
        self.page.get_by_text(BUTTON_SUBMIT_FOR_APPROVAL).click()

    def get_frame(self):
        """
        Get the iframe containing the e-signature form.

        Returns:
            Playwright frame locator: Frame containing the e-signature form
        """
        return self.page.frame_locator("iframe")

    def select_approvers(self, frame, approvers: dict):

        """
        Select approvers from dropdown menus.

        Args:
            frame: Playwright frame locator
            approvers (dict): Dictionary mapping team IDs to approver lists
        """
        for team_id, approver_list in approvers.items():
            dropdown = frame.locator(f"select#{team_id}")
            WaitUtils(self.page).wait_for_navigation()
            dropdown.select_option(approver_list)

    def fill_comment(self, frame, comment="Automated submission"):
        """
        Fill the comment field in the e-signature form.

        Args:
            frame: Playwright frame locator
            comment (str): Comment to add to the submission
        """
        frame.locator("#comment").click()
        frame.locator("#comment").fill(comment)

    def submit_popup(self, frame):
        dialog_message = {}
        """
        Submit the e-signature popup form.

        Args:
            frame: Playwright frame locator
        """
        # Handle potential alert that may block frame actions

        def handle_dialog(dialog):
            print(f"⚠️ Dialog appeared: {dialog.message}")
            dialog_message["text"] = dialog.message
            dialog.dismiss()

        self.page.once("dialog", handle_dialog)

        # Trigger submission flow
        self.page.get_by_label(SUBMIT_FOR_APPROVAL_LABEL).locator("div").filter(has_text="Submit for Approval").click()
        frame.get_by_role("button", name=BUTTON_SUBMIT).click()

        # Wait briefly to let dialog register (safely)
        self.page.wait_for_timeout(1000)

        return dialog_message.get("text")

    def get_phase_combobox(self):
        self.page.get_by_role("button", name=BUTTON_REFRESH).click()

        """
        Get the phase combobox element after refreshing.

        Returns:
            Playwright element: Phase combobox element
        """

        return self.page.get_by_role("combobox", name="Phase :")
