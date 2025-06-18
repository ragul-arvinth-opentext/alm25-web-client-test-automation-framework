class RequirementsPage:
    def __init__(self, page):
        self.page = page

    def go_to_requirements(self):
        self.page.get_by_role("link", name="Requirements").click()

    def expand_folder_if_collapsed(self, folder_name):
        self.page.locator(f"span:has-text('{folder_name}')").first.dblclick()

    def click_folder(self, folder_name):
        self.page.get_by_text(folder_name).click()

    def create_requirement_fields(self, name, desc, criticality, gxp):
        self.page.get_by_role("button", name="New Requirement").click()
        self.page.get_by_role("textbox", name=" Name :").fill(name)
        self.page.get_by_role("combobox", name="Criticality :").click()
        self.page.get_by_label(criticality).click()
        self.page.get_by_role("combobox", name="GxP :").click()
        self.page.get_by_label(gxp, exact=True).click()
        self.page.get_by_role("application").get_by_label("Description").fill(desc)

    def click_submit(self):
        self.page.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        return self.page.get_by_role("combobox", name="Phase :")

    def requirement_exists(self, req_name):
        return self.page.locator(f"text={req_name}").count() > 0
