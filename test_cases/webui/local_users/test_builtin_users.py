import allure
import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@allure.tag("Local_Users")
@allure.epic("Credentials")
@allure.feature("Local Users")
@pytest.mark.parametrize('builtin_users', get_data_list('builtin_users'), scope='function')
class Test_Builtin_Users:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self) -> None:
        """
        This method navigates to Local Users, sets the list to 100 items and enables built-in users toggle.
        """
        NAV.navigate_to_local_users()
        COM.set_100_items_per_page()
        LU.set_show_builtin_users_toggle()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self):
        """
        This method unsets the show built-in users toggle
        """
        yield
        # Clean up environment.
        LU.unset_show_builtin_users_toggle()

    @allure.tag("Read")
    @allure.story("Verify Built in Local Users")
    def test_built_in_users(self, builtin_users) -> None:
        """
        Summary: This test verifies a built-in user in the list of users

        Test Steps:
        1. Verify Built-in User Name is visible
        2. Verify Built-in User UID is visible
        3. Verify 'is Built-in' is visible
        4. Verify Built-in User Fullname is visible
        """
        # COM.set_search_field(builtin_users['username'])
        assert LU.is_user_visible(builtin_users['username'])
        assert LU.get_users_list_uid(builtin_users['username']) == builtin_users['uid']
        assert LU.get_users_list_builtin(builtin_users['username'])
        assert LU.get_users_list_full_name(builtin_users['username']) == builtin_users['full-name']
