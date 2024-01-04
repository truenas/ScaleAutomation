from helper.webui import WebUI


# Close WebUI after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '"+str(WebUI.total_time_waited())+"' seconds waited")
    WebUI.quit()


