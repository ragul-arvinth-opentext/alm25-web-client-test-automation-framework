class EsigPopup:
    def __init__(self, page):
        self.page = page

    def click_esig_and_submit(self):
        self.page.get_by_role("button", name="Esig").click()
        self.page.get_by_text("Submit for Approval").click()

    def get_frame(self):
        return self.page.frame_locator("iframe")

    def fill_comment_and_submit(self, frame, comment="Submitting for approval"):
        frame.locator("#comment").fill(comment)
        self.page.get_by_label("Submit for Approval").locator("div").filter(has_text="Submit for Approval").click()
        frame.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        self.page.get_by_role("button", name="Refresh").click()
        return self.page.get_by_role("combobox", name="Phase :")
