import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against (e.g., qa, staging)"
    )
    parser.addoption(
        "--browsers", action="store", default="chrome,firefox,edge",
        help="Comma-separated list of browsers to run tests on (e.g., chrome, firefox, edge)"
    )
    parser.addoption(
        "--headless", action="store_true", help="Run tests in headless mode"
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
def setup(request, pytestconfig):
    browser = request.param.lower()
    headless = pytestconfig.getoption("headless")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()

    # Load credentials from environment variables
    username = os.getenv("LOGINUSERNAME")
    password = os.getenv("PASSWORD")

    yield driver, username, password

    driver.quit()
