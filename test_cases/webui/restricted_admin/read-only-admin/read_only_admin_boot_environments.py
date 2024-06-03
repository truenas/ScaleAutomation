import allure
import pytest

from helper.global_config import shared_config
from keywords.api.boot import API_Boot
from keywords.webui.boot import Boot
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'Boot Environment', "Users", 'Permissions')
@allure.epic('Permission')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Boot_Environments:

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

    @allure.story("Read Only Admin Can View the List of Boot Environments")
    def test_read_only_admin_can_view_the_list_of_boot_environments(self):
        """
        This test verifies the read-only admin can view the list of boot environments.
        1. Navigate to Boot Environment page.
        2. Verify default and created boot environments is visible.
        """
        assert Boot.assert_boot_environment_row_exist(shared_config['DEFAULT_BE']) is True
        assert Boot.assert_boot_environment_row_exist('test-bootenv') is True

    @allure.story("Read Only Admin Can Not Modify Boot Environments")
    def test_read_only_admin_cannot_modify_boot_environments(self):
        """
        This test verifies the read-only admin cannot modify boot environments.
        1. Navigate to Boot Environment page.
        2. Verify default boot environment is restricted. (keep status, clone rename)
        3. Verify other boot environment is restricted. (keep status, activate, clone, delete, rename)
        """
        assert Boot.assert_boot_environment_element_restricted(shared_config['DEFAULT_BE'], 'clone') is True
        assert Boot.assert_boot_environment_element_restricted(shared_config['DEFAULT_BE'], 'rename') is True
        assert Boot.assert_boot_environment_element_restricted(shared_config['DEFAULT_BE'], 'toggle-keep') is True

        assert Boot.assert_boot_environment_element_restricted('test-bootenv', 'activate') is True
        assert Boot.assert_boot_environment_element_restricted('test-bootenv', 'clone') is True
        assert Boot.assert_boot_environment_element_restricted('test-bootenv', 'delete') is True
        assert Boot.assert_boot_environment_element_restricted('test-bootenv', 'rename') is True
        assert Boot.assert_boot_environment_element_restricted('test-bootenv', 'toggle-keep') is True

    @allure.story("Read Only Admin Can Not Scrub the Boot Pool")
    def test_read_only_admin_cannot_scrub_the_boot_pool(self):
        """
        This test verifies the read-only admin can not scrub the boot pool.
        1. Navigate to Boot Environment page.
        2. Verify scrub button is restricted.
        """
        assert COM.assert_button_is_restricted('bootenv-scrub') is True

    @allure.story("Read Only Admin Can Not View the Stats Settings for the Boot Pool")
    def test_read_only_admin_cannot_view_the_stats_settings_for_the_boot_pool(self):
        """
        This test verifies the read-only admin cannot view the stats settings for the boot pool.
        1. Navigate to Boot Environment page.
        2. Verify stats settings button is restricted.
        """
        assert COM.assert_button_is_restricted('bootenv-stats') is True

    @allure.story("Read Only Admin Can View the Boot Pool Status")
    def test_read_only_admin_can_view_the_boot_pool_status(self):
        """
        This test verifies the read-only admin can view the boot pool status.
        1. Navigate to Boot Environment page.
        2. Click on Boot Pool Status button.
        3. Verify boot pool status is visible and is ONLINE.
        """
        COM.click_button('bootenv-status')
        assert COM.assert_page_header('Boot Pool Status') is True
        assert Boot.assert_boot_pool_status('ONLINE') is True

    @allure.story("Read Only Admin Can Not Replace or Attach Disks in the Boot Pool")
    def test_read_only_admin_cannot_replace_or_attach_disks_in_the_boot_pool(self):
        """
        This test verifies the read-only admin can not replace or attach disks in the boot pool.
        1. Navigate to Boot Environment page.
        2. Click on Boot Pool Status button.
        3. Verify replace disk and attach disk buttons are restricted.
        """
        COM.click_button('bootenv-status')
        assert COM.assert_page_header('Boot Pool Status') is True
        assert Boot.assert_boot_disk_actions_is_restricted(shared_config['BOOT_DISK'], 'attach') is True
        assert Boot.assert_boot_disk_actions_is_restricted(shared_config['BOOT_DISK'], 'replace') is True
