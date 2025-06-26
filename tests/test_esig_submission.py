"""
Test module for electronic signature submission workflows.
Contains parameterized tests for various user scenarios and approval processes.
"""

# Third-party imports
import pytest

# Project imports
from business.login_action import LoginActions
from business.requirements_action import RequirementsActions
from business.submission_actions import SubmissionActions
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
def test_esig_submission(browser_context, user_data):
    """
    Test electronic signature submission workflow.
    
    Args:
        browser_context: Pytest fixture providing browser page context
        user_data (dict): Parameterized test data for user scenarios
    """
    page = browser_context

    # Fetch password securely from environment
    username = user_data["username"]
    user_data["username"], user_data["password"] = EnvUtils.get_credentials(username)

    # Initialize business logic classes
    login_business = LoginActions(page)
    req_business = RequirementsActions(page)
    submit_business = SubmissionActions(page)

    # Execute test workflow
    login_business.login(
        user_data["username"], 
        user_data["password"], 
        EnvUtils.get_base_url()
    )

    req_business.create_requirement_if_not_exists(
        folder=user_data["folder_name"],
        name=user_data["requirement_name"],
        desc=user_data["description"],
        criticality=user_data["criticality"],
        gxp=user_data["gxp"]
    )

    submit_business.submit_esig_flow(user_data)