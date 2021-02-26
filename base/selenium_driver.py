from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_messages_logger as cl
import logging
import time
import os


# Wrap all methods provided by selenium webdriver in a custom class so that we can use them later in our framework
class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        #Prepare the path where the screeshots will be saved
        fileName = resultMessage + '.' + str(round(time.time() * 1000)) + '.png'
        screeshotsFolder = '../screenshots'
        relativeFileName = screeshotsFolder + fileName
        currentFolder = os.path.dirname(__file__)
        destinationFile = os.path.join(currentFolder, relativeFileName)
        destinationFolder = os.path.join(currentFolder, screeshotsFolder)

        #Take the screenshot
        try:
            # Check if the destinationFolder does not exist
            if not os.path.exists(destinationFolder):
                os.makedirs(destinationFolder)
            self.driver.save_screenshot(destinationFile)
            self.log.info('Screenshot saved successfuly.')
        except:
            self.log.error('Exception occured.')
            print_stack()



    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType='id'):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info(f'Element found with locator {locator} and locator type {locatorType}')
        except:
            self.log.info('Element with locator {locator} and locator type {locatorType} was not found.')
        return element

    def getElementList(self, locator, locatorType="id"):
        """
        NEW METHOD
        Get list of elements
        """
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        except:
            self.log.info("Element list not found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        return element

    # Create our own custom click method
    def clickElement(self, locator, locatorType='id', element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info(f'Clicked the element with {locator} and locator type {locatorType}')
        except:
            self.log.info(f'Cannot click the element with {locator} and locator type {locatorType}.')
            print_stack()

    # Create our own custom method: sendKeys
    def sendKeys(self, data, locator, locatorType='id', element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info(f'Sent data on element with {locator} and locator type {locatorType}')
        except:
            self.log.info(f'Cannot send data on element with {locator} and locator type {locatorType}.')
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator: # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " +  info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator, locatorType='id', element=None):
        try:
            if locator:
                element = self.driver.getElement(locator, locatorType)
            if element is not None:
                self.log.info('Element found')
                return True
            else:
                self.log.info('Element not found.')
                return False
        except:
            self.log.info('Element not found.')
            return False

    def elementPrecenceCheck(self, locator, byType):
        try:
            elementsList = self.driver.find_elements(byType, locator)
            if len(elementsList) > 0:
                self.log.info('Element found')
                return True
            else:
                self.log.info('Element not found.')
                return False
        except:
            self.log.info('Element not found.')
            return False

    # Method to create custom explicit wait and error handling
    def waitForElement(self, locatorType='id', timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info(f"Waiting for maximum {timeout} for the element to be clickable.")
            wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, "searchButton")))
            self.log.info("Element appeared  on the web page.")
        except:
            self.log.info("Element not on the web page.")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")
'''
This class should be now inherited by every class within the pages package
Ex: pages/homepage/login
'''