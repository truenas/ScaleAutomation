import pytest
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    API_POST.create_non_admin_user('nfs_test_user', 'NFS Test User', 'testing', 'True')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    API_DELETE.delete_user('nfs_test_user')
