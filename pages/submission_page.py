class EsigPopup:
    def __init__(self, page):
        self.page = page

    def open_esig_popup(self):
        self.page.get_by_role("button", name="Esig").click()
        self.page.get_by_text("Submit for Approval").click()

    def get_frame(self):
        return self.page.frame_locator("iframe")
    
    
    
    def select_approvers(self, frame, approvers: dict):
        iframe = self.page.frame_locator("iframe")
    # `approvers` is a dictionary like: { "team0": ["SaDev", "SaDev2"], "team1": ["fauser"], "team2": ["saauthor"] }
        # count = 0
        # for team_id, values in approvers.items():
        #     frame.locator(f"#team{count}").select_option(f"#{team_id}", values)
        #     count+=1
        iframe.locator("#team0").select_option(["SaDev", "SaDev2"])
        iframe.locator("#team1").select_option("fauser")
        iframe.locator("#team2").select_option("Samanager")
 

    

    def fill_comment(self, frame, comment="Automated submission"):
        frame.locator("#comment").click()
        frame.locator("#comment").fill(comment)
        self.page.get_by_label("Submit for Approval").locator("div").filter(has_text="Submit for Approval").click()


    def submit_popup(self, frame):
        self.page.get_by_label("Submit for Approval").locator("div").filter(has_text="Submit for Approval").click()
        frame.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        self.page.get_by_role("button", name="Refresh").click()
        return self.page.get_by_role("combobox", name="Phase :")
