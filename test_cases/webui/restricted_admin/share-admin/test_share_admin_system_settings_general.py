import allure
import pytest

import xpaths
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'System Settings', 'General Page', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Share Admin')
class Test_Share_Admin_System_Settings_General:

    @pytest.fixture(autouse=True, scope='class')
    def setup_system_settings_general(self):
        """
        Summary: This setup fixture System Settings General page for all test cases.
        """
        NAV.navigate_to_system_settings_general()

    @allure.tag("Read")
    @allure.story("Share Admin Can See the System Settings General Page")
    def test_share_admin_can_see_the_system_settings_general(self):
        """
        Summary: This test verifies the share admin is able to access and see all details in the System Settings > General view.

        Test Steps:
        1. Verify the share admin is able to see General view page (title, Manage Config button)
        2. Verify the share admin is able to see Support Card details
        3. Verify the share admin is able to see GUI Card details
        4. Verify the share admin is able to see NTP LocalizationServers Card details
        5. Verify the share admin is able to see NTP Servers Card details
        6. Verify the share admin is able to see Email Card details
        """
        assert COM.assert_page_header('General')
        assert COM.is_visible(xpaths.common_xpaths.button_field('manage-configuration-menu')) is True

        # Support Card
        assert COM.is_card_visible('Support') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('set-license')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('file-ticket')) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text('TrueNAS Forums')) is True

        # GUI Card
        assert COM.is_card_visible('GUI') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('gui-settings')) is True
        assert COM.is_visible(xpaths.common_xpaths.card_label_and_value('GUI', 'Usage collection:', 'Enabled'))

        # Localization Card
        assert COM.is_card_visible('Localization') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('localization-settings')) is True
        assert COM.is_visible(xpaths.common_xpaths.card_label_and_value('Localization', 'Language:', 'English'))

        # NTP Servers Card
        assert COM.is_card_visible('NTP Servers') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('add-ntp')) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text('0.debian.pool.ntp.org'))
        assert COM.is_visible(xpaths.system_general.delete_ntp_server('0-debian-pool-ntp-org')) is True

        # Email Card
        assert COM.is_card_visible('Email') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('email-settings')) is True
        assert COM.is_visible(xpaths.common_xpaths.card_label_and_value('Email', 'Send Mail Method:', 'SMTP'))

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Update the Software Version")
    def test_share_admin_not_able_to_update_the_software_version(self):
        """
        Summary: This test verifies the share user is not able to update the software version on the system.

        Test Steps:
        1. Verify the Manage Configuration button is locked and not clickable
        """
        assert COM.assert_button_is_restricted('manage-configuration-menu') is True

    @allure.tag("Create")
    @allure.story("Share Admin Is Not Able to Add License")
    def test_share_admin_not_able_to_add_license(self):
        """
        Summary: This test verifies the share user is not able to add a license.

        Test Steps:
        1. Verify the Add License button is locked and not clickable
        """
        assert COM.assert_button_is_restricted('set-license') is True

    @allure.tag("Create")
    @allure.story("Share Admin Can File A Ticket")
    def test_share_admin_can_file_a_ticket(self):
        """
        Summary: This test verifies the share admin is able to file a ticket from the system settings > general view.

        Test Steps:
        1. Verify the File Ticket dialog appears
        2. Verify the Ticket form fields (title, message, attach debug)
        3. Edit title field
        4. Edit message field
        5. Verify the Lod in to Jira button is clickable
        """
        COM.click_button('file-ticket')
        assert COM.assert_page_header('Send Feedback') is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('title')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('message')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('attach-debug')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('take-screenshot')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('attach-images')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('login-to-jira')) is True
        COM.set_input_field('title', 'Auto Test Ticket: Please Remove')
        COM.set_textarea_field('message', 'Auto Test Ticket: Please Remove')
        assert COM.is_clickable(xpaths.common_xpaths.button_field('login-to-jira'))
        COM.click_button('close-feedback-dialog')

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Change GUI Settings")
    def test_share_admin_not_able_to_change_gui_settings(self):
        """
        Summary: This test verifies the share user is not able to change GUI settings.

        Test Steps:
        1. Click the GUI settings button
        2. Verify the GUI settings save button is locked and not clickable
        3. Close right panel
        """
        COM.click_button('gui-settings')
        assert COM.assert_right_panel_header('GUI Settings') is True
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Change Localization Settings")
    def test_share_admin_not_able_to_change_localization_settings(self):
        """
        Summary: This test verifies the share user is not able to change Localization settings.

        Test Steps:
        1. Click the Localization settings button
        2. Verify the Localization settings save button is locked and not clickable
        3. Close right panel
        """
        COM.click_button('localization-settings')
        assert COM.assert_right_panel_header('Localization Settings') is True
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()

    @allure.tag("Create")
    @allure.story("Share Admin Is Not Able to Add an NTP server")
    def test_share_admin_not_able_to_add_an_ntp_server(self):
        """
        Summary: This test verifies the share user is not able to add an NTP server.

        Test Steps:
        1. Verify the Add NTP server button is locked and not clickable
        """
        assert COM.assert_button_is_restricted('add-ntp') is True

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Delete an NTP server")
    def test_share_admin_not_able_to_delete_an_ntp_server(self):
        """
        Summary: This test verifies the share user is not able to delete an NTP server.

        Test Steps:
        1. Verify the Delete NTP server button is locked and not clickable
        """
        assert COM.assert_element_is_restricted(xpaths.system_general.delete_ntp_server('0-debian-pool-ntp-org')) is True

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Modify Email Options")
    def test_share_admin_not_able_to_modify_email_options(self):
        """
        Summary: This test verifies the share user is not able to modify email options.

        Test Steps:
        1. Click the Email settings button
        2. Verify the Email options Send Test Email button is locked and not clickable
        2. Verify the Email options save button is locked and not clickable
        3. Close right panel
        """
        COM.click_button('email-settings')
        assert COM.assert_right_panel_header('Email Options') is True
        assert COM.assert_button_is_restricted('send-test-mail') is True
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()
