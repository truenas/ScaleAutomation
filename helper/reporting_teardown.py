from pathlib import Path
import os
from helper.cli import Local_Command_Line
from datetime import datetime


def reporting_teardown(session):
    """
    This method creates a unique directory, moves the allure-results contents into it and generates the
    allure report.

    :param session: the session of information from the pytest run used for pathing.
    """
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
    # use workdir from helper.global_config for the path the put the reports folder.

