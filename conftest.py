from helper.webui import WebUI
import helper.reporting_teardown as RT


# Close WebUI and move report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '"+str(WebUI.total_time_waited())+"' seconds waited")
    RT.reporting_teardown(session)
    WebUI.quit()


