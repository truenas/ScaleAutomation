import pytest

from helper.global_config import private_config
from keywords.webui.common import Common

@pytest.fixture(scope='class', autouse=True)
def setup_class():
    print('in smb conftest start before')
    Common.create_non_admin_user_by_api('smbuser', 'smbuser Full', 'testing', 'True')
    print('in smb conftest start after')


def pytest_sessionfinish(session, exitstatus):
    print('in smb conftest finish before')
    Common.delete_user_by_api('smbuser')
    print('in smb conftest finish after')
