import pyperclip
import time
from selenium.common.exceptions import TimeoutException
from helper.global_config import shared_config, screenshots
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
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
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(shared_config['IMPLICITLY_WAIT'])
    return driver


web_driver = browser()


class WebUI(object):
    time_waited = 0
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
        web_driver.close()

    @classmethod
    def current_window_handle(cls) -> str:
        """
        This methode returns the handle of the current window

        :return: the handle of the current window

        Example:
            - WebUI.current_window_handle()
        """
        return web_driver.current_window_handle

    @classmethod
    def current_url(cls) -> str:
        """
        This method return the URL of the current page.

        :return: the URL of the current page.

        Example:
            - WebUI.current_url()
        """
        return web_driver.current_url

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
        cls.wait_until_visible(from_xpath)
        source = cls.xpath(from_xpath)
        cls.wait_until_visible(to_xpath)
        target = cls.xpath(to_xpath)
        # ActionChains(web_driver).drag_and_drop(source, target).perform() does not work.
        ActionChains(web_driver).click_and_hold(source).move_to_element(target).release(target).perform()

    @classmethod
    def find_xpath(cls, xpath: str) -> list[WebElement]:
        """
        This method return a list of web elements that matches the xpath.

        :param xpath: the xpath of elements
        :return: a list of web elements that matches the xpath.

        Example:
            - WebUI.find_xpath('xpath')
        """
        return web_driver.find_elements(By.XPATH, xpath)

    @classmethod
    def get(cls, url: str) -> None:
        """
        This method loads the URL web page in the current window.

        :param url: is the URL to load in the current window.

        Example:
            - WebUI.get('http://my_url')
        """
        web_driver.get(url)

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
    def get_clipboard_text(cls) -> any:
        """
        This method get the clipboard text and returns it.

        :return: return the clipboard text.

        Example:
            - WebUI.get_clipboard_text()
        """
        return pyperclip.paste()

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
        web_driver.quit()

    @classmethod
    def refresh(cls) -> None:
        """
        This method refreshes the current window.

        Example:
            - WebUI.refresh()
        """
        web_driver.refresh()
        cls.delay(1)

    @classmethod
    def save_screenshot(cls, filename) -> None:
        """
        This method saves a screenshot in the given filename (saves as .png).

        :param filename: is the name of the file to save the screenshot.

        Example:
            - WebUI.save_screenshot('screenshot_filename')
        """
        filename = screenshots + "/" + filename + ".png"
        print("@@@ SCREENSHOT: " + filename)
        web_driver.get_screenshot_as_file(filename)

    @classmethod
    def scroll_to_element(cls, xpath: str) -> None:
        """
        This method scroll to xpath of the element.

        :param xpath: the xpath of the element to scroll at.

        Example:
            - WebUI.scroll_to_element('xpath')
        """
        element = cls.xpath(xpath)
        cls.execute_script("arguments[0].scrollIntoView();", element)
        cls.delay(0.1)

    @classmethod
    def set_window_size(cls, width: int, height: int) -> None:
        """
        This method change the window size to the width and height provided.

        :param width: is the width number to change.
        :param height: is the height number to change.

        Example:
            - WebUI.set_window_size(300, 100)
        """
        web_driver.set_window_size(width, height)

    @classmethod
    def switch_to_window_index(cls, index: int) -> None:
        """
        This method switch to the window index provided.

        :param index: window or tab index number.

        Example:
            - WebUI.switch_to_window_index(1)
        """
        web_driver.switch_to.window(web_driver.window_handles[index])

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
        wait = WebDriverWait(web_driver, timeout)
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

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
        wait = WebDriverWait(web_driver, timeout)
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
        wait = WebDriverWait(web_driver, timeout)
        return wait.until(EC.number_of_windows_to_be(number))

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
        wait = WebDriverWait(web_driver, timeout)
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
        return web_driver.window_handles

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
        return web_driver.find_element(By.XPATH, xpath)
