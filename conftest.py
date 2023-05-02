import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.utils import ChromeType

@pytest.fixture(scope="class")
def setup():
    chrome_driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE, log_level=0, path="/usr/bin/chromedriver").install()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service_obj = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.implicitly_wait(5)
    return driver