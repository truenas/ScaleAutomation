from helper.webui import WebUI
from pathlib import Path
import os
from helper.cli import Local_Command_Line
from datetime import datetime


# Close WebUI and move report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '"+str(WebUI.total_time_waited())+"' seconds waited")
    allure_results = str(Path('/allure-results').as_posix())
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d-%H_%M_%S")
    test_name = str(Path(os.getcwd()).as_posix())
    test_name = test_name.rsplit('/', 1)
    test_name = str(f'{timestamp}-{test_name[1]}')
    full_allure_results_path = str(Path(os.getcwd()).as_posix()) + allure_results
    full_allure_results_path = full_allure_results_path.replace("C:", "/mnt/c")
    str_path = str(session.path)
    str_path = str_path.replace("\\", "/")
    str_path = str_path.replace("C:", "/mnt/c")
    command = Local_Command_Line(f'mkdir -p {str_path}/Reports/{test_name}')
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    command = Local_Command_Line(f'cp -r {full_allure_results_path} {str_path}/Reports/{test_name}')
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    command = Local_Command_Line(f'cd {str_path}/Reports/{test_name} ; allure generate -c allure-results')
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    print(f'Report generated. Folder name: | {test_name} |')
    WebUI.quit()
    # use workdir from helper.global_config for the path the put the reports folder.


