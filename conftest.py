import os

import pytest
from helper.webui import WebUI
from helper.global_config import private_config, shared_config
from helper.reporting import (
    allure_environment,
    allure_reporting,
    attach_browser_console_logs,
    start_percy_session,
    stop_percy_session,
    take_screenshot
)
from keywords.api.put import API_PUT
from keywords.webui.common import Common


# Close WebUI and move Allure report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print(f"\nTotal time (in seconds) spent on hard delays using WebUI.delay(): {WebUI.total_time_waited()} seconds waited")
    # stop_percy_session only stop percy session if PERCY_TOKEN environment variable is set.
    # stop_percy_session()
    allure_environment()
    allure_reporting()
    WebUI.quit()


def pytest_sessionstart(session):
    # start_percy_session only start percy session if PERCY_TOKEN environment variable is set.
    # start_percy_session()
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
    if report.when in ['call', "setup", "teardown"]:
        setattr(item, 'report', report)
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            attach_browser_console_logs()
            print(report.nodeid)
            screenshot_name = report.nodeid.partition(".py")[0].split("/")[-1]
            print(f'Screenshot name: {screenshot_name}')
            take_screenshot(screenshot_name)
