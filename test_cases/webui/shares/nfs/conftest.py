import pytest
from keywords.api.post import API_POST
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    # API_POST.create_non_admin_user('nfs_test_user', 'NFS Test User', 'testing', 'True')
    API_POST.start_service('nfs')
    NAV.navigate_to_shares()
    COMSHARE.delete_all_shares_by_share_type('nfs')


# @pytest.fixture(scope='class', autouse=True)
# def teardown_class():
#     yield
    # API_DELETE.delete_user('nfs_test_user')
