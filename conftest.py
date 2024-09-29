import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against (e.g., qa, staging)"
    )
    parser.addoption(
        "--browsers", action="store", default="chrome,firefox,edge", help="Comma-separated list of browsers to run tests on (e.g., chrome, firefox, edge)"
    )

@pytest.fixture(scope="session", autouse=True)
def load_environment(pytestconfig):
    # Load the .env file
    load_dotenv()

    # Get the selected environment from the command line
    selected_env = pytestconfig.getoption("env").lower()

    # Dynamically select the environment variables based on the selected environment
    if selected_env == "qa":
        os.environ["BASE_URL"] = os.getenv("QA_BASE_URL")
        os.environ["API_KEY"] = os.getenv("QA_API_KEY")
        os.environ["ENV"] = os.getenv("QA_ENV")
    elif selected_env == "prod":
        os.environ["BASE_URL"] = os.getenv("PROD_BASE_URL")
        os.environ["API_KEY"] = os.getenv("PROD_API_KEY")
        os.environ["ENV"] = os.getenv("PROD_ENV")
    else:
        raise ValueError(f"Unknown environment: {selected_env}")

    print(f"Running tests in {selected_env} environment")


@pytest.fixture(scope="function", params=["chrome", "firefox", "edge"])
def setup(request):
    browser = request.param.lower()

    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()

    # Load credentials from environment variables
    username = os.getenv("LOGINUSERNAME")
    password = os.getenv("PASSWORD")

    yield driver, username, password

    driver.quit()
