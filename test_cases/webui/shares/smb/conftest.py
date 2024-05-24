import pytest

from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    API_POST.create_non_admin_user('smbuser', 'smbuser Full', 'testing', 'True')
    API_POST.stop_service('cifs')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    API_DELETE.delete_user('smbuser')
