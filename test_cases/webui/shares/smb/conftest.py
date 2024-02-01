from helper.global_config import private_config
from keywords.webui.common import Common


def pytest_sessionstart(session):
    Common.create_non_admin_user_by_api('smbuser', 'smbuser Full', 'testing', 'True')
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])


def pytest_sessionfinish(session, exitstatus):
    Common.delete_user_by_api('smbuser')
