from pages.homepage.login import Login
from utilities.teststatus import TestStatus
import unittest
import pytest
import time

@pytest.mark.usefixtures('oneTimeSetUp', 'setUp')
class LoginTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.loginPage = Login(self)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=2)
    def test_ValidLogin(self):
        # Call the login method from pages->homepage->login.py
        self.loginPage.login('test@email.com', 'abcabc')
        result1 = self.loginPage.verifyPageTitle()
        self.ts.mark(result1, 'Title is incorrect')
        result2 = self.loginPage.verifyLoginWasSuccessful()
        self.ts.markFinal('test_valiLogin', result2, 'Login was not successful')

    @pytest.mark.run(order=1)
    def test_InvalidLogin(self):
        # Call the login method from pages->homepage->login.py
        self.loginPage.login('test@email.com', 'abcabcabc')
        time.sleep(5)
        result = self.loginPage.verifyLoginFailed()
        assert result == True