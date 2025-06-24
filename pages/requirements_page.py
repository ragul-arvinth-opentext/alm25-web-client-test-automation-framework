from utilities.wait_utils import WaitUtils

class RequirementsPage:
    def __init__(self, page):
        self.page = page
        self.wait = WaitUtils(page)

    def go_to_requirements_module(self):
        link = self.page.get_by_role("link", name="Requirements")
        self.wait.wait_for_element(link)
        link.click()

    def open_folder(self, folder_name):
        self.wait.wait_for_element(self.page.get_by_text(folder_name))
        folder_element = self.page.get_by_label("Requirements Tree", exact=True).locator(f"text={folder_name}").first
        folder_element.click()

    def expand_folder(self, folder_name):
        folder_element = self.page.get_by_label("Requirements Tree", exact=True).locator(f"span:has-text('{folder_name}')").first
        folder_element.dblclick()

    def requirement_exists(self, req_name):
        tree_locator = self.page.get_by_label("Requirements Tree", exact=True)

        for _ in range(3):
            try:
                req_locator = tree_locator.get_by_text(req_name, exact=True)
                req_locator.scroll_into_view_if_needed(timeout=3000)
                req_locator.wait_for(timeout=2000)
                print(f"✅ Requirement '{req_name}' found after scroll.")
                return True
            except:
                self.page.keyboard.press("PageDown")  # Scroll down manually as fallback
                self.page.wait_for_timeout(500)

        print(f"❌ Requirement '{req_name}' not found after scrolling.")
        return False


    def open_existing_requirement(self, req_name):
        self.page.get_by_text(req_name).click()

    def open_new_requirement_form(self):
        self.page.get_by_role("button", name="New Requirement").click()
        self.page.wait_for_selector("h2:has-text('New Requirement')")
        self.wait.wait_for_dialog_title("New Requirement")

    def fill_requirement_fields(self, name, desc, criticality, gxp):
        self.page.get_by_role("textbox", name="Name").fill(name)
        self.page.get_by_label("Undefined", exact=True).get_by_role("button", name="Open").click()
        self.page.get_by_label("Functional").click()
        self.wait.wait_for_navigation()

        self.page.get_by_role("combobox", name="Criticality :").click()
        self.page.get_by_label(criticality).click()
        self.page.get_by_role("combobox", name="GxP :").click()
        self.page.get_by_label(gxp, exact=True).click()
        self.page.get_by_role("application").get_by_label("Description").fill(desc)

    def submit_requirement(self):
        self.page.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        return self.page.get_by_role("combobox", name="Phase :")
