import allure
import pytest

from helper.global_config import shared_config
from keywords.api.boot import API_Boot
from keywords.webui.boot import Boot
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'Boot Environment', "Users", 'Permissions')
@allure.epic('Permission')
@allure.feature('Share Admin')
class Test_Share_Admin_Boot_Environments:

    @pytest.fixture(scope='function', autouse=True)
    def navigate_boot_environment_page(self):
        """
        This fixture navigates to boot environment page.
        """
        NAV.navigate_to_system_settings_boot()

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self):
        """
        This fixture sets a second boot environment and navigates to boot page.
        """
        shared_config['DEFAULT_BE'] = API_Boot.get_default_bootenv_id()
        shared_config['BOOT_DISK'] = API_Boot.get_boot_device()
        API_Boot.create_bootenv('test-bootenv', shared_config['DEFAULT_BE'])

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self):
        """
        This fixture deletes the created boot environment.
        """
        yield
        API_Boot.delete_bootenv('test-bootenv')

    @allure.story("Share Admin Can View the List of Boot Environments")
    def test_share_admin_can_view_the_list_of_boot_environments(self):
        """
        This test verifies the share admin can view the list of boot environments.
        1. Navigate to Boot Environment page.
        2. Verify default and created boot environments is visible.
        """
        assert Boot.assert_boot_environment_row_exist(shared_config['DEFAULT_BE']) is True
        assert Boot.assert_boot_environment_row_exist('test-bootenv') is True

    @allure.story("Share Admin Can Not Change the Keep Status, Activate, Clone, Delete and Rename Boot Environments")
    def test_share_admin_cannot_to_change_the_keep_status_active_clone_delete_and_rename_boot_environments(self):
        """
        This test verifies the share admin can not change the keep status, clone, delete or rename boot environments.
        1. Navigate to Boot Environment page.
        2. Verify default boot environment keep status, clone rename is restricted.
        3. Verify other boot environment keep status, activate, clone, delete and rename is restricted.
        """
        assert Boot.assert_clone_boot_environment_is_restricted(shared_config['DEFAULT_BE']) is True
        assert Boot.assert_rename_boot_environment_is_restricted(shared_config['DEFAULT_BE']) is True
        assert Boot.assert_keep_boot_environment_is_restricted(shared_config['DEFAULT_BE']) is True

        assert Boot.assert_activate_boot_environment_is_restricted('test-bootenv') is True
        assert Boot.assert_clone_boot_environment_is_restricted('test-bootenv') is True
        assert Boot.assert_delete_boot_environment_is_restricted('test-bootenv') is True
        assert Boot.assert_rename_boot_environment_is_restricted('test-bootenv') is True
        assert Boot.assert_keep_boot_environment_is_restricted('test-bootenv') is True

    @allure.story("Share Admin Can Not Scrub the Boot Pool")
    def test_share_admin_cannot_to_scrub_the_boot_pool(self):
        """
        This test verifies the share admin can not scrub the boot pool.
        1. Navigate to Boot Environment page.
        2. Verify scrub button is restricted.
        """
        assert Boot.asser_scrub_boot_environment_button_is_restricted() is True

    @allure.story("Share Admin Can Not View the Stats Settings for the Boot Pool")
    def test_share_admin_cannot_view_the_stats_settings_for_the_boot_pool(self):
        """
        This test verifies the share admin can not view the stats settings for the boot pool.
        1. Navigate to Boot Environment page.
        2. Verify stats settings button is restricted.
        """
        assert Boot.asser_stats_settings_button_is_not_restricted() is True

    @allure.story("Share Admin Can View the Boot Pool Status")
    def test_share_admin_can_view_the_boot_pool_status(self):
        """
        This test verifies the share admin can view the boot pool status.
        1. Navigate to Boot Environment page.
        2. Click on Boot Pool Status button.
        3. Verify boot pool status is visible and is ONLINE.
        """
        Boot.click_boot_pool_status_button()
        assert COM.assert_page_header('Boot Pool Status') is True
        assert Boot.assert_boot_pool_status('ONLINE') is True

    @allure.story("Share Admin Can Not Replace or Attach Disks in the Boot Pool")
    def test_share_admin_cannot_replace_or_attach_disks_in_the_boot_pool(self):
        """
        This test verifies the share admin can not replace or attach disks in the boot pool.
        1. Navigate to Boot Environment page.
        2. Click on Boot Pool Status button.
        3. Verify replace disk and attach disk buttons are restricted.
        """
        Boot.click_boot_pool_status_button()
        assert COM.assert_page_header('Boot Pool Status') is True
        assert Boot.assert_replace_disk_is_restricted(shared_config['BOOT_DISK']) is True
        assert Boot.assert_attach_disk_is_restricted(shared_config['BOOT_DISK']) is True
