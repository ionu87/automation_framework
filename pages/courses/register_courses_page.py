import utilities.custom_messages_logger as cl
import logging
from base.basepage import BasePage

class RegisterCoursesPage():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    search_box = "woocommerce-product-search-field-0"
    seach_button = ''
    _course = ""
    _all_courses = ""
    _details_button = ''
    _enroll_button = ""
    _emIL_address = ""
    _first_name = ""
    _last_name = ""
    _enroll_error_message = ""

    def enterCourseName(self, name):
        pass
