import allure
from allure_commons.types import AttachmentType
from datetime import datetime
from helper.cli import Local_Command_Line
from helper.global_config import workdir
from helper.webui import WebUI
from keywords.api.get import API_GET
from pathlib import Path


# make the timestamp global

def create_timestamp() -> str:
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d-%H_%M_%S")
    return timestamp


real_workdir = workdir.replace("\\", "/").replace("C:", "/mnt/c")
print(f'real_workdir: {real_workdir}')
real_full_test_path = str(Path.cwd())
full_test_path = str(Path(Path.cwd()).as_posix()).strip()
full_test_path = full_test_path.replace("C:", "/mnt/c")
print(f'full_test_path: {full_test_path}')
test_name = full_test_path.split('/')[-1]
timestamp_test_name = f'{create_timestamp()}-{test_name}'
print(f'timestamp_test_name: {timestamp_test_name}')
report_dir = f'{real_workdir}/Reports/{timestamp_test_name}'
print(f'report_dir: {report_dir}')
mkdircommand = Local_Command_Line(f'mkdir -p {report_dir}')
assert mkdircommand.status is True, f'{mkdircommand.stdout} \n{mkdircommand.stderr}'


def allure_environment():
    product_name = API_GET.get_system_product_name().json()
    product_type = API_GET.get_system_product_type().json()
    version = API_GET.get_system_version().json()
    version_short = API_GET.get_system_version_short().json()
    allure_results = str(Path('/allure-results'))
    environment_properties = str(Path('/environment.properties'))
    with open(f'{real_full_test_path}{allure_results}{environment_properties}', 'w') as file:
        file.write(f'product_name={product_name}\n')
        file.write(f'product_type={product_type}\n')
        file.write(f'version={version}\n')
        file.write(f'short_version={version_short}\n')


def allure_reporting():
    """
    This method creates a unique directory in the reports directory, moves the allure-results contents into it
    and generates the allure report.

    Example:
        - allure_reporting()
    """
    full_allure_results_path = f'{full_test_path}/allure-results'
    print(f'full_allure_results_path: {full_allure_results_path}')
    command = Local_Command_Line(f'cp -r {full_allure_results_path} {report_dir}')
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    command = Local_Command_Line(f'cd {report_dir} ; allure generate -c allure-results')
    assert command.status is True, f'{command.stdout} \n{command.stderr}'
    print(f'Report generated. Folder name: | {timestamp_test_name} |')


def attach_browser_console_logs():
    """
    This method attaches the browser console logs to the allure report.

    Example:
        - allure_attach_browser_console_logs()
    """
    console_logs = '\n'.join(map(str, WebUI.get_console_log()))
    allure.attach(console_logs, name='browser_console.log', attachment_type="text/plain", extension="attach")


def take_screenshot(name):
    """
    This method takes a screenshot of the webui and saves it in the reports folder.

    :param name: The name of the screenshot

    Example:
        - take_screenshot('name')
    """
    allure.attach(WebUI.get_screenshot_as_png(), name, attachment_type=AttachmentType.PNG)
