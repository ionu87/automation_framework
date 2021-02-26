import pytest
from selenium import webdriver
from base.webdriverfactory import WebDriverFactory
from pages.homepage.login import Login

# Generic method used to run before and after every test case
@pytest.yield_fixture()
def setUp():
    print("Running method level setUp")
    yield
    print("Running method level tearDown")


@pytest.yield_fixture(scope="module")
def oneTimeSetUp(request, browser):
    print("Running conftest demo one time setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()
    lp = Login(driver)
    lp.login("test@email.com", "abcabc")
    # if browser == 'firefox':
    #     print('Running tests on chrome')
    #     baseURL = 'https://letskodeit.com/'
    #     driver = webdriver.Firefox()
    #     driver.maximize_window()
    #     driver.implicitly_wait(5)
    #     driver.get(baseURL)
    # # If i don't provide the browser time it will run by default on Chrome
    # else:
    #     baseURL = "https://letskodeit.com/"
    #     driver = webdriver.Chrome()
    #     driver.get(baseURL)
    #     print('Running tests on Chrome')

    if request is not None:
        request.driver = driver

    yield driver
    driver.quit()
    print("Running conftest demo one time tearDown")


# Run test on different browsers or operating systems
def pytest_addoption(parser):
    parser.addoption('--browser')
    parser.addoption('--osType', help='Type or operating system')


# Create also fixtures for this
@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def osType(request):
    return request.config.getoption('--osType')