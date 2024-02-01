from helper.webui import WebUI
from helper.global_config import private_config
from keywords.webui.common import Common
import helper.reporting_teardown as RT


# Close WebUI and move Allure report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '" + str(WebUI.total_time_waited()) + "' seconds waited")
    RT.reporting_teardown(session)
    WebUI.quit()


def pytest_sessionstart(session):
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
