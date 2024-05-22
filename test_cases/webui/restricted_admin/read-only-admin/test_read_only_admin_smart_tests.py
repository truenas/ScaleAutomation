import allure
import pytest

from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as SHARE
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'SMART Tests', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Smart_Tests:
    """
    This test class tests read-only admin SMART Tests
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        Summary: This setup fixture create the SMART test for all test cases.
        """
        API_DELETE.delete_smart_test("Short Hour")
        API_POST.create_smart_test("hour", "0", "SHORT", "Short Hour")
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self):
        """
        Summary: This teardown fixture delete the SMART test and read-only admin for all test cases.
        """
        yield
        API_DELETE.delete_smart_test("Short Hour")

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The SMART Tests")
    def test_read_only_admin_can_see_the_smart_tests(self):
        """
        Summary: This test verifies the read-only admin is able to see SMART tests.

        Test Steps:
        1. Verify the read-only admin is able to see SMART tests
        2. Navigate to SMART test page
        3. Verify the read-only admin is able to see SMART tests
        """
        assert DP.assert_smart_test_description("Short Hour") is True
        DP.click_card_page_link('Periodic S.M.A.R.T. Tests')
        assert DP.assert_smart_page_smart_test_description("Short Hour") is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View the Configured SMART Test")
    def test_read_only_admin_can_view_the_configured_smart_test(self):
        """
        Summary: This test verifies the read-only admin is able to view the configured SMART test.

        Test Steps:
        1. Click Edit SMART test
        2. Verify SMART test fields (description, direction, bucket-input, etc.)
        3. Verify subsections (Transfer, Remote, Control, Advanced Options)
        4. Verify can view Custom Schedule dialog
        5. Close right panel
        6. Navigate to SMART test page
        7. Verify the SMART test page test fields (description, direction, bucket-input, etc.)
        """
        DP.click_edit_smart_test("Short Hour")
        assert SHARE.assert_share_configuration_field_visible("smart", "all disks") is True
        # assert SHARE.assert_share_configuration_field_visible("smart", "disks") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "type") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "description") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "schedule") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "save") is True

        # Verify can view Custom Schedule Dialog
        COM.select_option('schedule-presets', 'schedule-presets-custom')
        assert DP.assert_preset_dialog_visible() is True
        COM.click_button("done")
        COM.close_right_panel()

        # Navigate to SMART Test page
        DP.click_card_page_link('Periodic S.M.A.R.T. Tests')
        DP.click_edit_smart_test("Short Hour")

        # Verify SMART Test page fields
        assert SHARE.assert_share_configuration_field_visible("smart", "all disks") is True
        # assert SHARE.assert_share_configuration_field_visible("smart", "disks") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "type") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "description") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "schedule") is True
        assert SHARE.assert_share_configuration_field_visible("smart", "save") is True
        COM.close_right_panel()
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to add a SMART test")
    def test_read_only_admin_can_not_add_smart_test(self):
        """
        Summary: This test verifies the read-only admin is not able to add a SMART test.

        Test Steps:
        1. Verify the add SMART test button is locked and not clickable
        2. Navigate to SMART test page
        3. Verify the SMART test page add SMART test button is locked and not clickable
        """
        assert DP.assert_add_smart_test_button_is_restricted() is True
        DP.click_card_page_link('Periodic S.M.A.R.T. Tests')
        assert DP.assert_smart_page_add_smart_test_button_is_restricted() is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a SMART test")
    def test_read_only_admin_can_not_delete_smart_test(self):
        """
        Summary: This test verifies the read-only admin is not able to delete a SMART test.

        Test Steps:
        1. Verify the delete SMART test button is locked and not clickable
        2. Navigate to SMART test page
        3. Verify the SMART test page delete SMART test button is locked and not clickable
        """
        assert DP.assert_delete_smart_test_button_is_restricted("Short Hour") is True
        DP.click_card_page_link('Periodic S.M.A.R.T. Tests')
        assert DP.assert_smart_page_delete_smart_test_button_is_restricted("SHORT") is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a SMART test")
    def test_read_only_admin_can_not_modify_smart_test(self):
        """
        Summary: This test verifies the read-only admin is not able to modify a SMART test.

        Test Steps:
        1. Click Edit SMART test
        2. Verify the save SMART test button is locked and not clickable
        3. Close right panel
        4. Navigate to SMART test page
        5. Verify the SMART test page save SMART test button is locked and not clickable
        """
        DP.click_edit_smart_test("Short Hour")
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()
        DP.click_card_page_link('Periodic S.M.A.R.T. Tests')
        DP.click_edit_smart_test("Short Hour")
        assert DP.assert_smart_page_save_smart_test_button_is_restricted() is True
        COM.close_right_panel()
        COM.click_link('breadcrumb-data-protection')
