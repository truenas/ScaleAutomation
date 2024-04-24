import pytest
from keywords.api.post import API_POST


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    API_POST.start_service('nfs')

