from helper.webui import WebUI
from pathlib import Path
import os
from helper.cli import Local_Command_Line
from datetime import datetime


# Close WebUI and move report to Reports folder after the test session is completed
def pytest_sessionfinish(session, exitstatus):
    print("\nTotal time (in seconds) spent on hard delays using WebUI.delay(): '"+str(WebUI.total_time_waited())+"' seconds waited")
    # allure_results = str(Path('/allure-results'))
    now = datetime.now()
    timestamp = now.strftime("%H_%M_%S")
    test_name = str(Path(os.getcwd()).as_posix())
    test_name = test_name.rsplit('/', 1)
    test_name = str(timestamp)+'-'+test_name[1]
    print(test_name)
    full_allure_results_path = str(Path(os.getcwd()).as_posix()) + '/allure_results'
    str_path = str(session.path)
    str_path = str_path.replace("\\", "/")
    # str_path = str_path.replace("C:", "/mnt/c")
    # print(allure_results)
    print(full_allure_results_path)
    print(str_path)
    command = Local_Command_Line(f'mkdir -p {str_path}/Reports/{test_name}', wsl=False)
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    command = Local_Command_Line(f'cp -r {full_allure_results_path} {str_path}/Reports/{test_name}', wsl=False)
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    command = Local_Command_Line(f'cd {str_path}Reports/{test_name} ; allure generate -c allure-results', wsl=False)
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    WebUI.quit()
    # use workdir from helper.global_config for the path the put the reports folder.


