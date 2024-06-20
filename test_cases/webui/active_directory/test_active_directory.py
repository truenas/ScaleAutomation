import allure
import pytest

import xpaths
from helper.data_config import get_data_list
from helper.global_config import shared_config, private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.ssh.permissions import Permissions_SSH as Perm_SSH
from keywords.webui.active_directory import Active_Directory
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.directory_services import Directory_Services
from keywords.webui.navigation import Navigation
from keywords.webui.permissions import Permissions


@pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
class Test_Active_Directory:
    """
    This test class covers the leave active directory, and join active directory.
    """

    @pytest.fixture(scope='class')
    def setup_active_directory_with_api(self, ad_data):
        """
        This setup fixture sets up the active directory for test that need it.
        """
        API_PUT.set_nameservers(ad_data['nameserver'])
        API_PUT.join_active_directory(ad_data['username'], ad_data['password'], ad_data['domain'])

    @pytest.fixture(scope='class')
    def setup_dns_for_active_directory(self, ad_data):
        """
        This setup fixture sets up the active directory for test that need it.
        """
        API_PUT.set_nameservers(ad_data['nameserver'])

    @pytest.fixture(scope='class')
    def setup_dns_for_ad_with_a_second_nameserver(self, ad_data):
        """
        This setup fixture sets up the active directory for test that need it.
        """
        API_PUT.set_nameservers(ad_data['nameserver'], ad_data['nameserver2'])

    def test_leaving_active_directory(self, ad_data, setup_active_directory_with_api, tear_down_class):
        """
        This test case test leaving active directory.
        """
        # Navigate to directory services page.
        Navigation.navigate_to_directory_services()

        # Click on the active directory settings button and leave the active directory.
        Directory_Services.click_active_directory_settings_button()
        assert Active_Directory.is_edit_active_directory_visible() is True
        Active_Directory.click_leave_domain_button()
        assert Active_Directory.is_leave_domain_dialog_visible()
        Active_Directory.set_leave_domain_username(ad_data['username'])
        Active_Directory.set_leave_domain_password(ad_data['password'])
        Active_Directory.click_the_dialog_leave_domain_button()

        # Verify that the active directory card is not visible after leaving the active directory
        assert Directory_Services.assert_active_directory_card_not_visible() is True

    def test_setup_active_directory(self, ad_data, setup_dns_for_active_directory):
        """
        This test case test setup active directory.
        """
        # Navigate to directory services page.
        Navigation.navigate_to_directory_services()

        # Click on the active directory settings button and set up the active directory.
        Directory_Services.click_configure_active_directory_button()
        assert Active_Directory.is_edit_active_directory_visible()
        Active_Directory.set_domain_name(ad_data['domain'])
        Active_Directory.set_domain_account_name(ad_data['username'])
        Active_Directory.set_domain_account_password(ad_data['password'])
        Active_Directory.set_enable_requires_password_or_kerberos_principal_checkbox()
        Active_Directory.click_advanced_options_button()
        Active_Directory.set_computer_account_ou(ad_data['ca_ou'])
        Active_Directory.set_netbios_name(shared_config['HOSTNAME'])
        Active_Directory.click_save_button_and_wait_for_ad_to_finish_saving()

        # Verify the Active Directory card is visible and the service status is HEALTHY
        assert Directory_Services.assert_active_directory_card_visible()
        assert Directory_Services.assert_service_status('HEALTHY')

        # Verify the domain name and domain account name is visible.
        assert Directory_Services.assert_active_directory_domain_name(ad_data['domain'])
        assert Directory_Services.assert_active_directory_domain_account_name(ad_data['username'])

    @allure.tag("defect_verification", "NAS-129528")
    def test_setup_active_directory_with_group_cache_disabled(self, ad_data, tear_down_class):
        """
        This test case test setup active directory with the group cache disabled.
        """
        # Setup SSH usage and dataset
        Navigation.navigate_to_dashboard()
        API_POST.start_service('ssh')
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_POST.create_dataset("tank/group_cache_disabled")

        # Click on the active directory settings button and edit the active directory configuration.
        Navigation.navigate_to_directory_services()
        Directory_Services.click_active_directory_settings_button()
        assert Active_Directory.is_edit_active_directory_visible() is True
        Active_Directory.click_advanced_options_button()
        Common.set_checkbox("disable-freenas-cache")
        Common.click_button("rebuild-cache")
        assert Common.assert_progress_bar_not_visible() is True
        Active_Directory.click_save_button_and_wait_for_ad_to_finish_saving()

        # Verify the group cache is disabled after saving
        Directory_Services.click_active_directory_settings_button()
        assert Active_Directory.is_edit_active_directory_visible() is True
        Active_Directory.click_advanced_options_button()
        assert Common.get_element_property(xpaths.common_xpaths.checkbox_field_attribute
                                           ("disable-freenas-cache"), 'checked') is True
        Common.close_right_panel()

        # Navigate to datasets page and edit dataset group with manually typed AD group
        Navigation.navigate_to_datasets()
        Datasets.select_dataset("group_cache_disabled")
        Datasets.click_edit_permissions_button()
        Permissions.set_apply_group_checkbox()
        Permissions.set_dataset_group("AD03\domain guests")
        Common.click_save_button()

        # Verify dataset group has saved in UI and CLI
        assert Permissions.assert_dataset_group("AD03\domain guests") is True
        assert Perm_SSH.verify_getfacl_contains_permissions("/mnt/tank/group_cache_disabled",
                                                            r"# group: AD03\\domain\040guests") is True

        # Delete dataset
        API_DELETE.delete_dataset("tank/group_cache_disabled")

    def test_setup_active_directory_with_misconfigured_dns(self, ad_data, setup_dns_for_ad_with_a_second_nameserver):
        """
        This test case test setup active directory with misconfigured dns.
        """
        # Navigate to directory services page.
        Navigation.navigate_to_directory_services()

        # Click on the active directory settings button and set up the active directory.
        Directory_Services.click_configure_active_directory_button()
        assert Active_Directory.is_edit_active_directory_visible() is True
        Active_Directory.set_domain_name(ad_data['domain'])
        Active_Directory.set_domain_account_name(ad_data['username'])
        Active_Directory.set_domain_account_password(ad_data['password'])
        Active_Directory.set_enable_requires_password_or_kerberos_principal_checkbox()
        Active_Directory.click_advanced_options_button()
        Active_Directory.set_computer_account_ou(ad_data['ca_ou'])
        Active_Directory.set_netbios_name(shared_config['HOSTNAME'])
        Common.unset_checkbox("disable-freenas-cache")
        Active_Directory.click_save_button_and_wait_for_ad_to_finish_saving()

        # Verify the message of the nameserver failed to resolve SRV record message.
        assert Active_Directory.assert_nameserver_failed_to_resolve_srv_record_message(ad_data['nameserver2']) is True
        Common.click_error_dialog_close_button()
        Common.close_right_panel()

    @pytest.fixture(scope='function')
    def tear_down_class(self, request, ad_data):
        """
        This fixture tears down the active directory for all tests.
        """
        yield
        if 'setup_active_directory' in request.node.name:
            API_POST.leave_active_directory(ad_data['username'], ad_data['password'])
            API_PUT.set_nameservers(ad_data['nameserver1'], ad_data['nameserver2'])
        elif request.node.report.failed and 'leave_active_directory' in request.node.name:
            API_POST.leave_active_directory(ad_data['username'], ad_data['password'])
            API_PUT.set_nameservers(ad_data['nameserver1'], ad_data['nameserver2'])
