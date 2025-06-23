from utilities.wait_utils import WaitUtils
class EsigPopup:
    def __init__(self, page):
        self.page = page

    def open_esig_popup(self):
        self.page.get_by_role("button", name="Esig").click()
        self.page.get_by_text("Submit for Approval").click()

    def get_frame(self):
        return self.page.frame_locator("iframe")

    def select_approvers(self, frame, approvers: dict):
        for team_id, approver_list in approvers.items():
            dropdown = frame.locator(f"select#{team_id}")
            WaitUtils(self.page).wait_for_navigation()
            print(f"Selecting {approver_list} for {team_id}")
            dropdown.select_option(approver_list)
            #This is facing some issues not every time but sometimes, 
            # so just check if u can run it a few times by changing the req names in the user_data
        # frame.locator("#team0").select_option(["SaDev", "SaDev2"])
        # frame.locator("#team1").select_option("fauser")
        # frame.locator("#team2").select_option("Samanager")

    def fill_comment(self, frame, comment="Automated submission"):
        frame.locator("#comment").click()
        frame.locator("#comment").fill(comment)

    def submit_popup(self, frame):
    # Handle potential alert that may block frame actions
        def handle_dialog(dialog):
            print(f"Dialog appeared: {dialog.message}")
            dialog.dismiss()

        self.page.once("dialog", handle_dialog)

        self.page.get_by_label("Submit for Approval").locator("div").filter(has_text="Submit for Approval").click()
        frame.get_by_role("button", name="Submit").click()

    def get_phase_combobox(self):
        self.page.get_by_role("button", name="Refresh").click()
        return self.page.get_by_role("combobox", name="Phase :")
