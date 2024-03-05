import pytest
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    Common.create_non_admin_user_by_api('nfs_test_user', 'NFS Test User', 'testing', 'True')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    COMSHARE.delete_all_shares_by_sharetype('nfs')
    Common.delete_user_by_api('nfs_test_user')
