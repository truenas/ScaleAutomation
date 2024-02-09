from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV


def pytest_sessionstart(session):
    print('in nfs conftest start before')
    Common.create_non_admin_user_by_api('nfs_test_user', 'NFS Test User', 'testing', 'True')
    print('in nfs conftest start after')


def pytest_sessionfinish(session, exitstatus):
    print('in nfs conftest finish before')
    COMSHARE.delete_all_shares_by_sharetype('nfs')
    Common.delete_user_by_api('nfs_test_user')
    NAV.navigate_to_dashboard()
    print('in nfs conftest finish after')
