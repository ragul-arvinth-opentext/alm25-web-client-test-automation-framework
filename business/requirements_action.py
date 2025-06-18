from pages.requirements_page import RequirementsPage
from utilities.wait_utils import WaitUtils

class RequirementsActions:
    def __init__(self, page):
        self.page = page
        self.req_page = RequirementsPage(page)
        self.wait = WaitUtils(page)

    def create_requirement_if_not_exists(self, folder, name, desc, criticality, gxp):
        # Step 1: Go to Requirements module
        requirements_link = self.page.get_by_role("link", name="Requirements")
        self.wait.wait_for_element(requirements_link)
        requirements_link.click()

        # Step 2: Expand Requirements tree
        self.req_page.expand_folder_if_collapsed("Requirements")

        # Step 3: Click the folder from JSON
        folder_element = self.page.get_by_label("Requirements Tree", exact=True).get_by_text(folder)
        self.wait.wait_for_element(folder_element)
        folder_element.click()

        # Step 4: If requirement with same name exists, skip creation
        if self.req_page.requirement_exists(name):
            return

        # Step 5: Create new requirement
        self.req_page.create_requirement_fields(name, desc, criticality, gxp)
        self.req_page.click_submit()

    def verify_phase_draft(self):
        self.wait.wait_until_value(self.req_page.get_phase_combobox(), "Draft")
