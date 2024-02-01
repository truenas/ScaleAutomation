from helper.global_config import private_config
from keywords.webui.common import Common


def pytest_sessionstart(session):
    Common.create_non_admin_user_by_api('nfs_test_user', 'NFS Test User', 'testing', 'True')


def pytest_sessionfinish(session, exitstatus):
    Common.delete_user_by_api('nfs_test_user')