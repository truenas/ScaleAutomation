import pytest
from keywords.webui.common import Common


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    Common.create_non_admin_user_by_api('smbuser', 'smbuser Full', 'testing', 'True')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    Common.delete_user_by_api('smbuser')
