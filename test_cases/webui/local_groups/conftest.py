import pytest

from helper.data_config import get_data_list
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_():
    """
    This method starts all tests to navigate to the Data Protection page
    """
    # Ensure we are on the Data Protection page.
    Navigation.navigate_to_local_groups()


@pytest.fixture(scope='class', autouse=True)
@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
def setup_class(groups):
    """
    This method clears any test groups before test is run for a clean environment
    """
    # Setup clean environment.
    LG.delete_group_by_api(groups['group-name'],groups['group-privileges'])
    LG.delete_group_by_api(groups['alt-group-name'],groups['group-privileges'])
