import pytest
import logging
import os
from src.page_objects.pom.login_page import LoginPage  # Ensure this path is correct


@pytest.mark.usefixtures("setup")
class TestVWOLogin:

    @pytest.mark.qa
    def test_vwo_login_positive(self, setup):
        LOGGER = logging.getLogger(__name__)
        LOGGER.info("Starting the Testcase")

        # Unpack the values from the setup fixture
        driver, username, password = setup

        # Use the driver and credentials
        driver.get(os.getenv("BASE_URL"))
        login_page = LoginPage(driver)
        login_page.login(usr=username, pwd=password)
