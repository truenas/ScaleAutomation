import allure
import pytest

import xpaths
from keywords.webui.alert_settings import Alert_Settings as ALERT
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'System Settings', 'Alert Settings Page', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_System_Settings_Alert_Settings:

    @pytest.fixture(autouse=True, scope='class')
    def setup_system_settings_alert_settings(self):
        """
        Summary: This setup fixture System Settings Alert Settings page for all test cases.
        """
        NAV.navigate_to_system_settings_alert_settings()

    @allure.tag("Read")
    @allure.issue('NAS-129415', 'NAS-129415')
    @allure.issue('NAS-129437', 'NAS-129437')
    @allure.story("Read Only Admin Can See the System Settings Alert Settings Page")
    def test_read_only_admin_can_see_the_system_settings_alert_settings(self):
        """
        Summary: This test verifies the read-only admin is able to access and see all details in the System Settings > Alert Settings view.

        Test Steps:
        1. Verify the read-only admin is able to see Alert Settings view page (title, Columns, Add)
        2. Verify the read-only admin is able to see various Card details (Alert Settings, Category)
        """
        assert COM.assert_page_header('Alert Settings')

        # Alert Services Card
        assert COM.is_text_visible('Alert Services') is True
        assert COM.is_input_visible('search') is True
        assert COM.is_button_visible('columns') is True
        assert COM.is_button_visible('alert-service-add') is True
        assert COM.is_visible(xpaths.common_xpaths.edit_row_button('snmp-trap')) is True
        assert COM.is_visible(xpaths.common_xpaths.delete_row_button('snmp-trap')) is True

        # Category Card
        # TODO: NAS-129437 - convert to is_card_visible()
        # assert COM.is_card_visible('Category') is True
        assert COM.is_text_visible('Category') is True
        assert COM.is_button_visible('categories') is True
        # TODO: NAS-129415
        # Application Update Available
        assert COM.is_select_by_row_visible('level') is True
        assert COM.is_select_by_row_visible('policy') is True
        # Catalog Not Healthy
        assert COM.is_select_by_row_visible('level', 2) is True
        assert COM.is_select_by_row_visible('policy', 2) is True
        # Unable to Configure Applications
        assert COM.is_select_by_row_visible('level', 3) is True
        assert COM.is_select_by_row_visible('policy', 3) is True
        # Unable to Start Applications
        assert COM.is_select_by_row_visible('level', 4) is True
        assert COM.is_select_by_row_visible('policy', 4) is True
        # Unable to Sync Catalog
        assert COM.is_select_by_row_visible('level', 5) is True
        assert COM.is_select_by_row_visible('policy', 5) is True

        assert COM.is_button_visible('save') is True

    @allure.tag("Create")
    @allure.story("Read Only Admin Is Not Able to Add Any Alert Services")
    def test_read_only_admin_not_able_to_add_any_alert_services(self):
        """
        Summary: This test verifies the read-only user is not able to add any alert services.

        Test Steps:
        1. Verify Add button is locked and not clickable
        """
        assert COM.assert_button_is_restricted('alert-service-add') is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able to Modify Any Alert Settings Settings")
    def test_read_only_admin_not_able_to_modify_any_alert_settings_settings(self):
        """
        Summary: This test verifies the read-only user is not able to modify any alert settings settings.

        Test Steps:
        1. Click Alert Service options button (three dots)
        2. Click edit option
        3. Verify the Save Debug button is locked and not clickable
        4. Verify Send Test Alert button is locked and not clickable
        """
        COM.click_on_element(xpaths.common_xpaths.edit_row_button('snmp-trap'))
        assert COM.assert_right_panel_header('Edit Alert Service')
        assert COM.assert_button_is_restricted('save') is True
        assert COM.assert_button_is_restricted('send-test-alert') is True
        COM.close_right_panel()

    @allure.tag("Delete")
    @allure.story("Read Only Admin Is Not Able to Delete Any Alert Services")
    def test_read_only_admin_not_able_to_delete_any_alert_services(self):
        """
        Summary: This test verifies the read-only user is not able to delete any alert services.

        Test Steps:
        1. Verify Delete button is locked and not clickable
        """
        assert COM.assert_element_is_restricted(xpaths.common_xpaths.delete_row_button('snmp-trap')) is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able to Modify Any Category Settings")
    def test_read_only_admin_not_able_to_modify_any_category_settings(self):
        """
        Summary: This test verifies the read-only user is not able to modify any category settings.

        Test Steps: (for each category)
        1. Click category button (Applications, Certificates, Directory Services)
        2. Verify the Save Debug button is locked and not clickable
        """
        ALERT.assert_alert_category_save_button_restricted('applications')
        ALERT.assert_alert_category_save_button_restricted('certificates')
        ALERT.assert_alert_category_save_button_restricted('directory-service')
        ALERT.assert_alert_category_save_button_restricted('hardware')
        ALERT.assert_alert_category_save_button_restricted('kmip')
        ALERT.assert_alert_category_save_button_restricted('network')
        ALERT.assert_alert_category_save_button_restricted('reporting')
        ALERT.assert_alert_category_save_button_restricted('sharing')
        ALERT.assert_alert_category_save_button_restricted('storage')
        ALERT.assert_alert_category_save_button_restricted('system')
        ALERT.assert_alert_category_save_button_restricted('tasks')
        ALERT.assert_alert_category_save_button_restricted('ups')
