import pytest
import logging
import selenium.webdriver

@pytest.fixture
def browser():
    # This browser will be local
    # ChromeDriver must be on the system PATH
    b = selenium.webdriver.Chrome()
    logging.info("Wait for 10 seconds before returning the browser object")
    b.implicitly_wait(10)
    yield b
    logging.info("Webdirver is going to quit")
    b.quit()