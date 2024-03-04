import os
import pytest
from helper.webui import WebUI
from helper.global_config import private_config, shared_config
from helper.reporting import allure_reporting, take_screenshot, allure_environment
from keywords.api.put import API_PUT
from keywords.webui.common import Common


# Close WebUI and move Allure report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print(f"\nTotal time (in seconds) spent on hard delays using WebUI.delay(): {WebUI.total_time_waited()} seconds waited")
    allure_environment()
    allure_reporting()
    WebUI.quit()


def pytest_sessionstart(session):
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
    # Set up a unique hostname for the test session.
    # PID is unique for each session
    shared_config['HOSTNAME'] = f'pytest-{os.getpid()}'
    # set up host name to avoid conflicts with other systems.
    API_PUT.set_hostname()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot whenever test fails.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            print(report.nodeid)
            screenshot_name = report.nodeid.partition(".py")[0].split("/")[-1]
            print(f'Screenshot name: {screenshot_name}')
            take_screenshot(screenshot_name)
