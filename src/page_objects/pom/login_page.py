from selenium.webdriver.common.by import By

from src.utils.common_waits import webdriver_wait


class LoginPage:  #TODO - 4. Encapsulation

    def __init__(self, driver):  #TODO - 6. Constructor
        self.driver = driver

    # Page Locators
    username = (By.ID, "login-username")
    password = (By.NAME, "password")
    submit_button = (By.XPATH, "//button[@id='js-login-btn']")
    error_message = (By.CSS_SELECTOR, "#js-notification-box-msg")

    def get_username(self):
        return self.driver.find_element(*LoginPage.username)

    def get_password(self):
        return self.driver.find_element(*LoginPage.password)

    def get_submit_button(self):
        return self.driver.find_element(*LoginPage.submit_button)

    def get_error_message(self):
        webdriver_wait(driver=self.driver, element_tuple=self.error_message, timeout=5)
        return self.driver.find_element(*LoginPage.error_message)

    def login(self, usr, pwd):
        self.get_username().send_keys(usr)
        self.get_password().send_keys(pwd)
        self.get_submit_button().click()

    def get_error_message_text(self):
        self.get_error_message().text
