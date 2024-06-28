import allure
import pytest

import xpaths
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'System Settings', 'Advanced Page', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_System_Settings_Advanced:

    @pytest.fixture(autouse=True, scope='class')
    def setup_system_settings_advanced(self):
        """
        Summary: This setup fixture System Settings Advanced page for all test cases.
        """
        NAV.navigate_to_system_settings_advanced()

    @allure.tag("Read")
    @allure.issue('NAS-129329', 'NAS-129329')
    @allure.story("Read Only Admin Can See the System Settings Advanced Page")
    def test_read_only_admin_can_see_the_system_settings_advanced(self):
        """
        Summary: This test verifies the read-only admin is able to access and see all details in the System Settings > Advanced view.

        Test Steps:
        1. Verify the read-only admin is able to see Advanced view page (title, Save Debug button)
        2. Verify the read-only admin is able to see various Card details (Console, Syslog, Audit, Kernel)
        """
        assert COM.assert_page_header('Advanced')
        assert COM.is_button_visible('save-debug') is True

        # Console Card
        assert COM.is_card_visible('Console') is True
        assert COM.is_button_visible('console-configure') is True
        assert COM.is_text_visible('Enable Serial Console:') is True

        # Syslog Card
        assert COM.is_card_visible('Syslog') is True
        assert COM.is_button_visible('syslog-configure') is True
        assert COM.is_text_visible('Syslog Level:') is True

        # Audit Card
        assert COM.is_card_visible('Audit') is True
        assert COM.is_button_visible('audit-configure') is True
        assert COM.is_text_visible('Reservation:') is True

        # Kernel Card
        assert COM.is_card_visible('Kernel') is True
        assert COM.is_button_visible('kernel-configure') is True
        assert COM.is_text_visible('Enable Debug Kernel:') is True

        # Cron Jobs Card
        assert COM.is_card_visible('Cron Jobs') is True
        assert COM.is_button_visible('cron-add') is True
        assert COM.is_text_visible('Next Run') is True
        # Cron Jobs page
        COM.click_link('cron-jobs-open-in-new')
        assert COM.assert_page_header('Cron Jobs') is True
        assert COM.is_input_visible('search') is True
        assert COM.is_button_visible('columns') is True
        assert COM.is_button_visible('add-cronjob') is True
        assert COM.is_select_visible('page-size') is True
        NAV.navigate_to_system_settings_advanced()

        # Init/Shutdown Scripts Card
        assert COM.is_card_visible('Init/Shutdown Scripts') is True
        assert COM.is_button_visible('init-shutdown-add') is True
        assert COM.is_text_visible('Timeout') is True
        # Init/Shutdown Scripts page
        COM.click_link('init-shutdown-open-in-new')
        assert COM.assert_page_header('Init/Shutdown Scripts') is True
        assert COM.is_button_visible('add-init-shutdown-script') is True
        assert COM.is_select_visible('page-size') is True
        NAV.navigate_to_system_settings_advanced()

        # Sysctl Card
        assert COM.is_card_visible('Sysctl') is True
        assert COM.is_button_visible('sysctl-add') is True
        assert COM.is_text_visible('Var') is True
        # Sysctl page
        COM.click_link('sysctl-open-in-new')
        assert COM.assert_page_header('Sysctl') is True
        assert COM.is_input_visible('search') is True
        assert COM.is_button_visible('add-tunable') is True
        assert COM.is_select_visible('page-size') is True
        NAV.navigate_to_system_settings_advanced()

        # Storage Card
        assert COM.is_card_visible('Storage') is True
        assert COM.is_button_visible('storage-configure') is True
        assert COM.is_text_visible('System Dataset Pool:') is True

        # Replication Card
        assert COM.is_card_visible('Replication') is True
        assert COM.is_button_visible('replication-configure') is True
        assert COM.is_text_visible('Replication Tasks Limit:') is True

        # Access Card
        assert COM.is_card_visible('Access') is True
        assert COM.is_button_visible('sessions-terminate') is True
        assert COM.is_button_visible('sessions-configure') is True
        assert COM.is_text_visible('Token Lifetime:') is True
        assert COM.is_visible(xpaths.system.advanced_access_terminate_session()) is True

        # Allowed IP Addresses Card
        assert COM.is_card_visible('Allowed IP Addresses') is True
        assert COM.is_button_visible('configure-ip-address') is True

        # TODO: Uncomment when NAS-129329 fixed
        # # Self-Encrypting Drive Card
        # assert COM.is_card_visible('Self-Encrypting Drive') is True
        # assert COM.is_button_visible('self-encrypted-drive-configure') is True
        # assert COM.is_text_visible('ATA Security User:') is True

        # Isolated GPU Device(s) Card
        assert COM.is_card_visible('Isolated GPU Device(s)') is True
        assert COM.is_button_visible('isolated-gpus-devices-configure') is True
        assert COM.is_text_visible('No Isolated GPU Device(s) configured') is True

        # Global Two-Factor Authentication Card
        assert COM.is_card_visible('Global Two Factor Authentication') is True
        assert COM.is_button_visible('two-factor-auth-configure') is True
        assert COM.is_text_visible('Global 2FA:') is True

    @allure.tag("Update")
    @allure.issue('NAS-129333', 'NAS-129333')
    @allure.story("Read Only Admin Is Not Able to Modify Any Advanced Settings")
    def test_read_only_admin_not_able_to_modify_any_advanced_settings(self):
        """
        Summary: This test verifies the read-only user is not able to modify any advanced settings.

        Test Steps:
        1. Verify the Save Debug button is clickable
        2. Verify configure buttons are locked and not clickable
        """
        assert COM.is_clickable(xpaths.common_xpaths.button_field('save-debug')) is True
        assert COM.assert_button_is_restricted('console-configure') is True
        assert COM.assert_button_is_restricted('syslog-configure') is True
        assert COM.assert_button_is_restricted('audit-configure') is True
        # TODO: fix this when NAS-129333 is fixed
        assert COM.assert_button_is_restricted('kernel-configure') is True
        assert COM.assert_button_is_restricted('cron-add') is True
        COM.click_link('cron-jobs-open-in-new')
        assert COM.assert_button_is_restricted('add-cronjob') is True
        NAV.navigate_to_system_settings_advanced()
        assert COM.assert_button_is_restricted('init-shutdown-add') is True
        COM.click_link('init-shutdown-open-in-new')
        assert COM.assert_button_is_restricted('add-init-shutdown-script') is True
        NAV.navigate_to_system_settings_advanced()
        assert COM.assert_button_is_restricted('sysctl-add') is True
        COM.click_link('sysctl-open-in-new')
        assert COM.assert_button_is_restricted('add-tunable') is True
        NAV.navigate_to_system_settings_advanced()
        assert COM.assert_button_is_restricted('storage-configure') is True
        assert COM.assert_button_is_restricted('replication-configure') is True
        assert COM.assert_button_is_restricted('sessions-terminate') is True
        assert COM.assert_button_is_restricted('sessions-configure') is True
        assert COM.assert_button_is_restricted('configure-ip-address') is True
        # TODO: Uncomment when NAS-129329 fixed
        # assert COM.assert_button_is_restricted('self-encrypted-drive-configure') is True
        assert COM.assert_button_is_restricted('isolated-gpus-devices-configure') is True
        # TODO: fix this when NAS-129333 is fixed
        assert COM.assert_button_is_restricted('two-factor-auth-configure') is True
