"""
Business logic layer for Requirements Management operations.
Handles complex requirements workflows and interactions.
"""

# Project imports
from pages.requirements_page import RequirementsPage
from utilities.wait_utils import WaitUtils
from utilities.constants import (
    REQUIREMENTS_MODULE,
    PHASE_DRAFT
)


class RequirementsActions:
    """
    Business logic class for requirements management operations.
    Orchestrates requirements page interactions and validation.
    """
    
    def __init__(self, page):
        """
        Initialize requirements actions with page dependencies.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.req_page = RequirementsPage(page)
        self.wait = WaitUtils(page)

    def create_requirement_if_not_exists(self, folder, name, desc, criticality, gxp):
        """
        Create a new requirement if it doesn't already exist.
        
        Args:
            folder (str): Folder name to create requirement in
            name (str): Requirement name
            desc (str): Requirement description
            criticality (str): Criticality level
            gxp (str): GxP classification
        """
        self.req_page.go_to_requirements_module()
        if not self.req_page.requirement_exists(folder):
            self.req_page.expand_folder(REQUIREMENTS_MODULE)
        self.req_page.expand_folder(folder)
        self.req_page.open_folder(folder)

        if self.req_page.requirement_exists(name):
            self.req_page.open_existing_requirement(name)
            return

        self.req_page.open_new_requirement_form()
        self.req_page.fill_requirement_fields(name, desc, criticality, gxp)
        self.req_page.submit_requirement()

    def verify_phase_draft(self):
        """Verify that the current phase is Draft."""
        self.wait.wait_until_value(self.req_page.get_phase_combobox(), PHASE_DRAFT)
