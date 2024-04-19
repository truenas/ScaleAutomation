import allure
import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation as NAV


@allure.tag("Local_Groups")
@allure.epic("Credentials")
@allure.feature("Local Groups")
@pytest.mark.parametrize('built_in', get_data_list('builtin_groups'), scope='function')
class Test_Builtin_Groups:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self) -> None:
        """
        This method navigates to Local Groups, sets the list to 100 items and enables built-in groups toggle.
        """
        NAV.navigate_to_local_groups()
        COM.set_100_items_per_page()
        LG.set_show_builtin_groups_toggle()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self):
        """
        This method unsets the show built-in groups toggle and navigates to dashboard
        """
        yield
        # Clean up environment.
        LG.unset_show_builtin_groups_toggle()
        NAV.navigate_to_dashboard()

    @allure.tag("Read")
    @allure.story("Verify Built in Local Groups")
    @allure.issue("NAS-128406", "NAS-128406")
    def test_built_in_group(self, built_in) -> None:
        """
        Summary: This test verifies built in groups display

        Test Steps:
        1. Verify group Name displays
        2. Verify group gid displays
        3. Verify group builtin displays
        4. Verify group allow sudo commands displays
        5. Verify group samba auth displays
        """
        # COM.set_search_field(built_in['group-name'])
        assert LG.is_group_visible(built_in['group-name']) is True
        assert LG.get_group_list_gid(built_in['group-name']) == built_in['gid']
        assert LG.get_group_list_builtin(built_in['group-name']) == built_in['Builtin']
        assert LG.get_group_list_allow_sudo_commands(built_in['group-name']) == built_in['Allows sudo commands']
        assert LG.get_group_list_samba_auth(built_in['group-name']) == built_in['Samba Authentication']
