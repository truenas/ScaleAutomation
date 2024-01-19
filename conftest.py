from helper.global_config import workdir
from helper.webui import WebUI
from pathlib import Path
import os


# Close WebUI after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '"+str(WebUI.total_time_waited())+"' seconds waited")
    WebUI.quit()
    allure_results = str(Path('/allure-results'))
    full_allure_results_path = str(Path(os.getcwd()).as_posix()) + allure_results
    # use workdir from helper.global_config for the path the put the reports folder.
