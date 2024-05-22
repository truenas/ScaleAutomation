import pytest
from helper.global_config import private_config, shared_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common


@pytest.fixture(autouse=True, scope='package')
def setup_user():
    """
    This setup fixture create the read-only admin for the session.
    """
    print(f'Username: {shared_config["ROA_USER"]}')
    API_POST.create_read_only_admin(shared_config['ROA_USER'], shared_config['ROA_FULLNAME'], shared_config['ROA_PASSWORD'])
    API_DELETE.delete_all_periodic_snapshots_tasks()

    Common.logoff_truenas()
    Common.login_to_truenas(shared_config['ROA_USER'], shared_config['ROA_PASSWORD'])


@pytest.fixture(autouse=True, scope='package')
def delete_user():
    """
    This teardown fixture delete the read-only admin for the session.
    """
    yield
    Common.logoff_truenas()
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])

    API_DELETE.delete_user(shared_config['ROA_USER'])
