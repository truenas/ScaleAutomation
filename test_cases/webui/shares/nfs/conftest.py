import pytest
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    print('in nfs setup before')
    Common.create_non_admin_user_by_api('nfs_test_user', 'NFS Test User', 'testing', 'True')
    print('in nfs setup after')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    print('in nfs finish before')
    COMSHARE.delete_all_shares_by_sharetype('nfs')
    Common.delete_user_by_api('nfs_test_user')
    NAV.navigate_to_dashboard()
    print('in nfs finish after')
