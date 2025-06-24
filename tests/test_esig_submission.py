import pytest
from business.login_action import LoginActions
from business.requirements_action import RequirementsActions
from business.submisson_actions import SubmissionActions
from utilities.env_utils import EnvUtils
from utilities.data_loader import load_test_data

@pytest.mark.parametrize("user_data", [
    {
        "username": data["username"],
        "team": data["team"],
        "folder_name": data["folder_name"],
        "requirement_name": data["requirement_name"],
        "description": data["description"],
        "criticality": data["criticality"],
        "gxp": data["gxp"],
        "approvers": data.get("approvers", {})
    } for data in load_test_data()
])


def test_esig_submission(browser_context, config, user_data):
    page = browser_context

    # Fetch password securely from environment
    username = user_data["username"]
    user_data["username"], user_data["password"] = EnvUtils.get_credentials(username)

    login_business = LoginActions(page)
    req_business = RequirementsActions(page)
    submit_business = SubmissionActions(page)

    login_business.login(user_data["username"], user_data["password"], config["base_url"])

    req_business.create_requirement_if_not_exists(
        folder=user_data["folder_name"],
        name=user_data["requirement_name"],
        desc=user_data["description"],
        criticality=user_data["criticality"],
        gxp=user_data["gxp"]
    )

    submit_business.submit_esig_flow(user_data)
