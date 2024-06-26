import pyperclip
import time
from helper.global_config import shared_config
from percy import percy_snapshot
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def browser() -> WebDriver:
    """
    This method returns the webdriver with its settings

    :return: the webdriver with its settings

        Example:
            - WebUI.browser()
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(shared_config['IMPLICITLY_WAIT'])
    return driver


class WebUI(object):
    time_waited = 0
    web_driver = browser()
    execute_script = web_driver.execute_script

    @classmethod
    def add_time_waited(cls, seconds: float) -> None:
        """
        This method adds the given amount of seconds to the total time waited

        Example:
            - WebUI.add_time_waited(3)
            - WebUI.add_time_waited(10.3)
        """
        cls.time_waited = (cls.time_waited + seconds)

    @classmethod
    def close_window(cls) -> None:
        """
        This method closes the current window

        Example:
            - WebUI.close_window()
        """
        cls.web_driver.close()

    @classmethod
    def current_window_handle(cls) -> str:
        """
        This methode returns the handle of the current window

        :return: the handle of the current window

        Example:
            - WebUI.current_window_handle()
        """
        return cls.web_driver.current_window_handle

    @classmethod
    def current_url(cls) -> str:
        """
        This method return the URL of the current page.

        :return: the URL of the current page.

        Example:
            - WebUI.current_url()
        """
        return cls.web_driver.current_url

    @classmethod
    def delay(cls, seconds: float) -> None:
        """
        This method sleep the number of seconds provided.

        :param seconds: is the number of seconds to sleep.

        Example:
            - WebUI.delay(3)
            - WebUI.delay(10.3)
        """
        time.sleep(seconds)
        cls.add_time_waited(seconds)

    @classmethod
    def drag_and_drop(cls, from_xpath: str, to_xpath: str) -> None:
        """
        This method simulate Holds down the left mouse button on the source element, then moves to the target
        element and releases the mouse button.

        :param from_xpath: the xpath text of the element to drag
        :param to_xpath: the xpath text of the element to drag at
        :return: return the ActionChains

        Example:
            - WebUI.drag_and_drop('fromXpath', 'toXpath')
        """
        assert cls.wait_until_visible(from_xpath) is True
        source = cls.xpath(from_xpath)
        target = cls.xpath(to_xpath)
        action = ActionChains(cls.web_driver)
        action.click_and_hold(source)
        assert cls.wait_until_visible(to_xpath) is True
        action.move_to_element(target)
        action.pause(0.5)
        action.release(target)
        action.perform()

    @classmethod
    def find_xpath(cls, xpath: str) -> list[WebElement]:
        """
        This method return a list of web elements that matches the xpath.

        :param xpath: the xpath of elements
        :return: a list of web elements that matches the xpath.

        Example:
            - WebUI.find_xpath('xpath')
        """
        return cls.web_driver.find_elements(By.XPATH, xpath)

    @classmethod
    def get(cls, url: str) -> None:
        """
        This method loads the URL web page in the current window.

        :param url: is the URL to load in the current window.

        Example:
            - WebUI.get('http://my_url')
        """
        cls.web_driver.get(url)

    @classmethod
    def get_attribute(cls, xpath: str, attribute: str) -> str:
        """
        This method return the attribute of the given xpath element.

        :param xpath: is text of the xpath.
        :param attribute: is the attribute of the element.
        :return: return the attribute of the given xpath element.

        Example:
            - WebUI.get_attribute('xpath', 'attribute')
        """
        return cls.xpath(xpath).get_attribute(attribute)

    @classmethod
    def get_console_log(cls) -> any:
        """
        This method get the console log and returns it.

        :return: return the console log.

        Example:
            - WebUI.get_console_log()
        """
        return cls.web_driver.get_log('browser')

    @classmethod
    def get_clipboard_text(cls) -> any:
        """
        This method get the clipboard text and returns it.

        :return: return the clipboard text.

        Example:
            - WebUI.get_clipboard_text()
        """
        return pyperclip.paste()

    @classmethod
    def get_screenshot_as_png(cls) -> bytes:
        """
        This method saves a screenshot in the given filename (saves as .png).

        Example:
            - WebUI.save_screenshot_as_png()
        """
        return cls.web_driver.get_screenshot_as_png()

    @classmethod
    def get_text(cls, xpath: str) -> str:
        """
        This method return the text the given xpath element.

        :param xpath: is text of the xpath.
        :return: return the text the given xpath element.

        Example:
            - WebUI.get_text('xpath')
        """
        return cls.xpath(xpath).text

    @classmethod
    def get_window_index(cls, handle: str) -> int:
        """
        This methode returns the index of the given handle of the current window

        :param handle: is the handle of the window.
        :return: the index of the handle of the current window

        Example:
            - WebUI.get_window_index('windowHandle')
        """
        return WebUI.window_handles().index(handle)

    @classmethod
    def quit(cls) -> None:
        """
        This method Closes the browser and shuts down the driver executable.

        Example:
            - WebUI.quit()
        """
        cls.web_driver.quit()

    @classmethod
    def refresh(cls) -> None:
        """
        This method refreshes the current window.

        Example:
            - WebUI.refresh()
        """
        cls.web_driver.refresh()
        cls.delay(1)

    @classmethod
    def send_key(cls, key: str) -> None:
        """
        This method sends the key to the current window.

        :param key: is the key to send.

        Example:
            - WebUI.send_key('escape')
        """
        match key.lower():
            case 'enter' | 'return':
                key_code = Keys.ENTER
            case 'esc' | 'escape':
                key_code = Keys.ESCAPE
            case 'tab':
                key_code = Keys.TAB
            case _:
                key_code = Keys.ESCAPE
        ActionChains(cls.web_driver).send_keys(key_code).perform()

    @classmethod
    def scroll_to_bottom_of_page(cls) -> None:
        """
        This method uses the height of the page and scrolls to the bottom of it.
        Example:
            - WebUI.scroll_to_bottom_of_page()
        """
        cls.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        cls.delay(1)

    @classmethod
    def scroll_to_element(cls, xpath: str) -> None:
        """
        This method scroll to xpath of the element.

        :param xpath: the xpath of the element to scroll at.

        Example:
            - WebUI.scroll_to_element('xpath')
        """
        element = cls.xpath(xpath)
        cls.execute_script("arguments[0].scrollIntoView(true);", element)
        cls.delay(1)

    @classmethod
    def scroll_to_top_of_page(cls) -> None:
        """
        This method scrolls to the top of the page.

        Example:
            - WebUI.scroll_to_top_of_page()
        """
        cls.execute_script("window.scrollTo(0, document.body.scrollTop);")
        cls.delay(1)

    @classmethod
    def set_window_size(cls, width: int, height: int) -> None:
        """
        This method change the window size to the width and height provided.

        :param width: is the width number to change.
        :param height: is the height number to change.

        Example:
            - WebUI.set_window_size(300, 100)
        """
        cls.web_driver.set_window_size(width, height)

    @classmethod
    def switch_to_window_index(cls, index: int) -> None:
        """
        This method switch to the window index provided.

        :param index: window or tab index number.

        Example:
            - WebUI.switch_to_window_index(1)
        """
        cls.web_driver.switch_to.window(cls.web_driver.window_handles[index])

    @classmethod
    def take_percy_snapshot(cls, name: str, scope: str = None) -> None:
        """
        This method takes a snapshot for percy of the current window.

        :param name: is the name of the snapshot.
        :param scope: is the xpath of the element that is the scope of the snapshot.

        Example:
            - WebUI.percy_snapshot('name')
        """
        if scope:
            percy_snapshot(cls.web_driver, name, scope=scope)
        else:
            percy_snapshot(cls.web_driver, name, widths=[1920])

    @classmethod
    def total_time_waited(cls) -> float:
        """
        This method returns the amount of total time waited in seconds

        :return: total time waited in seconds

        Example:
            - WebUI.total_time_waited()
        """
        return cls.time_waited

    @classmethod
    def wait_until_clickable(cls, xpath: str, timeout: int = shared_config['WAIT']) -> WebElement:
        """
        This method returns the element if it is clickable before the timeout

        :param xpath: is the xpath to wait to be clickable.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: the element if the xpath element is clickable before the timeout

        Example:
            - WebUI.wait_until_clickable('xpath')
            - WebUI.wait_until_clickable('xpath', shared_config['SHORT_WAIT'])
        """
        wait = WebDriverWait(cls.web_driver, timeout)
        # Some field like checkbox input may not be visible but are present and clickable.
        assert cls.wait_until_presence_is_located(xpath, timeout) is True
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    @classmethod
    def wait_until_field_populates(cls, xpath: str, prop: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the input field is populated before timeout otherwise it returns False.

        :param xpath: is the xpath of the field.
        :param prop: is the property of the field to check.
        :param timeout: is optional and is the number of seconds to wait before timeout.
        :return: True if the input field is populated before timeout otherwise it returns False.
        """
        val = cls.xpath(xpath).get_property(prop)
        i = 0
        while val == '':
            WebUI.delay(2)
            val = cls.xpath(xpath).get_property(prop)
            i += 2
            if i > timeout:
                return False
        return True

    @classmethod
    def wait_until_not_visible(cls, xpath: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the xpath element is not visible before timeout otherwise it returns False.

        :param xpath: is the xpath to wait to be visible.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the xpath element is not visible before timeout otherwise it returns False.

        Example:
            - WebUI.wait_until_not_visible('xpath')
            - WebUI.wait_until_not_visible('xpath', shared_config['SHORT_WAIT'])
        """
        wait = WebDriverWait(cls.web_driver, timeout)
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    @classmethod
    def wait_until_number_of_windows_to_be(cls, number: int, timeout: int = shared_config['MEDIUM_WAIT']) -> bool:
        """
        This method return True if the number of windows is given number before the timeout otherwise it returns False.

        :param number: is the number of window.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the number of windows is given number before the timeout otherwise it returns False.

        Example:
            - WebUI.wait_until_number_of_windows_to_be(2)
            - WebUI.wait_until_number_of_windows_to_be(1, shared_config['SHORT_WAIT'])
        """
        wait = WebDriverWait(cls.web_driver, timeout)
        return wait.until(EC.number_of_windows_to_be(number))

    @classmethod
    def wait_until_presence_is_located(cls, xpath: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the xpath element is present before timeout otherwise it returns False.

        :param xpath: is the xpath to wait to be present.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the xpath element is present before timeout otherwise it returns False.

        Example:
            - WebUI.wait_until_present('xpath')
            - WebUI.wait_until_present('xpath', shared_config['SHORT_WAIT'])
        """
        wait = WebDriverWait(cls.web_driver, timeout)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    @classmethod
    def wait_until_visible(cls, xpath: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the xpath element is visible before timeout otherwise it returns False.

        :param xpath: is the xpath to wait to be visible.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the xpath element is visible before timeout otherwise it returns False.

        Example:
            - WebUI.wait_until_visible('xpath')
            - WebUI.wait_until_visible('xpath', shared_config['SHORT_WAIT'])
        """
        wait = WebDriverWait(cls.web_driver, timeout)
        try:
            return wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).is_displayed()
        except TimeoutException:
            return False

    @classmethod
    def window_handles(cls) -> list:
        """
        This method returns the handles of all windows within the current session.

        :return: the handles of all windows within the current session

        Example:
            - WebUI.window_handles()
        """
        return cls.web_driver.window_handles

    @classmethod
    def xpath(cls, xpath: str) -> WebElement:
        """
        This method return the WebElement of the xpath and is used to click, send keys and more.

        :param xpath: the xpath of the element.
        :return: the WebElement of the xpath specified.

        Example:
            - WebUI.xpath('xpath')
        """
        time.sleep(shared_config['EXECUTION_DELAY'])
        return cls.web_driver.find_element(By.XPATH, xpath)
