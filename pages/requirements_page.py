"""
Page Object Model for Requirements Management Page.
Contains locators and basic interactions for requirements functionality.
"""

# Project imports
from utilities.wait_utils import WaitUtils
from utilities.constants import (
    REQUIREMENTS_MODULE,
    FUNCTIONAL_CATEGORY,
    UNDEFINED_LABEL,
    BUTTON_NEW_REQUIREMENT,
    BUTTON_SUBMIT,
    NEW_REQUIREMENT_DIALOG_TITLE
)


class RequirementsPage:
    """
    Page Object for Requirements Management functionality.
    Encapsulates requirements page elements and basic interactions.
    """
    
    def __init__(self, page):
        """
        Initialize requirements page with Playwright page object.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.wait = WaitUtils(page)

    def go_to_requirements_module(self):
        """Navigate to the requirements module."""
        link = self.page.get_by_role("link", name=REQUIREMENTS_MODULE)
        self.wait.wait_for_element(link)
        link.click()

    def open_folder(self, folder_name):
        """
        Open a specific folder in the requirements tree.
        
        Args:
            folder_name (str): Name of the folder to open
        """
        self.wait.wait_for_element(self.page.get_by_text(folder_name))
        folder_element = self.page.get_by_label("Requirements Tree", exact=True).locator(f"text={folder_name}").first
        folder_element.click()

    def expand_folder(self, folder_name):
        """
        Expand a folder in the requirements tree.
        
        Args:
            folder_name (str): Name of the folder to expand
        """
        folder_element = self.page.get_by_label("Requirements Tree", exact=True).locator(f"span:has-text('{folder_name}')").first
        folder_element.dblclick()

    def requirement_exists(self, req_name):
        """
        Check if a requirement exists in the current view.
        
        Args:
            req_name (str): Name of the requirement to check
            
        Returns:
            bool: True if requirement exists, False otherwise
        """
        tree_locator = self.page.get_by_label("Requirements Tree", exact=True)

        for _ in range(3):
            try:
                req_locator = tree_locator.get_by_text(req_name, exact=True)
                req_locator.scroll_into_view_if_needed(timeout=3000)
                req_locator.wait_for(timeout=2000)
                print(f"Requirement '{req_name}' found after scroll.")
                return True
            except:
                self.page.keyboard.press("PageDown")  # Scroll down manually as fallback
                self.page.wait_for_timeout(500)

        print(f"Requirement '{req_name}' not found after scrolling.")
        return False

    def open_existing_requirement(self, req_name):
        """
        Open an existing requirement for editing.
        
        Args:
            req_name (str): Name of the requirement to open
        """
        self.page.get_by_text(req_name).click()

    def open_new_requirement_form(self):
        """Open the new requirement creation form."""
        self.page.get_by_role("button", name=BUTTON_NEW_REQUIREMENT).click()
        self.wait.wait_for_dialog_title(NEW_REQUIREMENT_DIALOG_TITLE)

    def fill_requirement_fields(self, name, desc, criticality, gxp):
        """
        Fill in all requirement form fields.
        
        Args:
            name (str): Requirement name
            desc (str): Requirement description
            criticality (str): Criticality level
            gxp (str): GxP classification
        """
        self.page.get_by_role("textbox", name="Name").fill(name)
        self.page.get_by_label(UNDEFINED_LABEL, exact=True).get_by_role("button", name="Open").click()
        self.page.get_by_label(FUNCTIONAL_CATEGORY).click()
        self.wait.wait_for_navigation()

        self.page.get_by_role("combobox", name="Criticality :").click()
        self.page.get_by_label(criticality).click()
        self.page.get_by_role("combobox", name="GxP :").click()
        self.page.get_by_label(gxp, exact=True).click()
        self.page.get_by_role("application").get_by_label("Description").fill(desc)

    def submit_requirement(self):
        """Submit the requirement form."""
        self.page.get_by_role("button", name=BUTTON_SUBMIT).click()

    def get_phase_combobox(self):
        """
        Get the phase combobox element.
        
        Returns:
            Playwright element: Phase combobox element
        """
        return self.page.get_by_role("combobox", name="Phase :")
