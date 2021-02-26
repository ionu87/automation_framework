# from selenium.webdriver.common.by import By
from base.selenium_driver import SeleniumDriver
import logging
import utilities.custom_messages_logger as cl
import time


# This is a wrapper method to login
class Login(SeleniumDriver):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        # Calling the __init__ method of super class
        super().__init__(driver)
        self.driver = driver

    # Locators so that when something changes in the code this is the only place that needs updating
    _login_page = 'ast-button'
    _email_field = 'email'
    _password_field = 'password'
    _login_button = "//input[@value='Login']"

    '''Create methods for every locator element so that we can call them anywhere in the framework
    without writing every time the same code  
    '''
    # def getLoginPage(self):
    #     return self.driver.find_element(By.CLASS_NAME, self._login_page)
    #
    # def getEmailField(self):
    #     return self.driver.find_element(By.ID, self._email_field)
    #
    # def getPasswordField(self):
    #     return self.driver.find_element(By.ID, self._password_field)
    #
    # def getLoginButton(self):
    #     return self.driver.find_element(By.XPATH, self._login_button)

    # Write action methods for every method element identified above
    def clickLoginPage(self):
        self.clickElement(self._login_page, locatorType='class')

    def enterEmail(self, email):
        self.sendKeys(email, self._email_field)

    def enterPassword(self, password):
        self.sendKeys(password, self._password_field)

    def clickLoginButton(self):
        self.clickElement(self._login_button, locatorType="xpath")

    # Main method to login by calling all the above methods
    def login(self, email='', password=''):
        self.clickLoginPage()
        self.clearFields()
        self.enterEmail(email)
        self.enterPassword(password)
        time.sleep(5)
        self.clickLoginButton()

    def verifyLoginWasSuccessful(self):
        result = self.isElementPresent("//h1[contains(text(),'All Courses')]", locatorType="xpath")
        return result

    def verifyLoginFailed(self):
        result = self.isElementPresent("//span[contains(text(),'Your username or password is invalid. Please try again.')]", locatorType="xpath")
        return result

    def clearFields(self):
        emailField = self.getElement(locator=self._email_field)
        emailField.clear()
        passwordField = self.getElement(locator=self._password_field)
        passwordField.clear()


    def verifyPageTitle(self):
        if "Let's Lode It" in self.getTitle():
            return True
        else:
            return False