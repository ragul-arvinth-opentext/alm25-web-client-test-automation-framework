from business.login_action import LoginActions
from business.requirements_action import RequirementsActions
from business.submisson_actions import SubmissionActions
import pytest

@pytest.mark.parametrize("user_data", [
    {
        "username": data["username"],
        "password": data["password"],
        "team": data["team"],
        "folder_name": data["folder_name"],
        "requirement_name": data["requirement_name"],
        "description": data["description"],
        "criticality": data["criticality"],
        "gxp": data["gxp"]
    } for data in __import__('json').load(open("test_data/test_data.json"))
])
def test_esig_submission(browser_context, config, user_data):
    page = browser_context

    login_business = LoginActions(page)
    req_business = RequirementsActions(page)
    submit_business = SubmissionActions(page)

    login_business.login(user_data["username"], user_data["password"])

    req_business.create_requirement_if_not_exists(
        folder=user_data["folder_name"],
        name=user_data["requirement_name"],
        desc=user_data["description"],
        criticality=user_data["criticality"],
        gxp=user_data["gxp"]
    )

    submit_business.submit_for_approval(team=user_data["team"])
