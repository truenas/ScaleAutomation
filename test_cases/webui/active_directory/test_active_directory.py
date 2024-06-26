import allure
import pytest

import xpaths
from helper.data_config import get_data_list
from helper.global_config import shared_config, private_config
from helper.webui import WebUI
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
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.smb import SMB


@allure.tag('Active Directory', 'Directory Services')
@allure.epic('Directory Services')
@allure.feature('Active Directory')
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

    @allure.tag("Create", 'Percy')
    @allure.story("Setup Active Directory")
    def test_setup_active_directory(self, ad_data, setup_dns_for_active_directory):
        """
        This test case test setup active directory.
        1. Navigate to directory services page.
        2. Click on the active directory settings button
        3. Set up the active directory and save
        4. Verify the Active Directory card is visible and the service status is HEALTHY
        5. Take a snapshot of active directory setup
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

        WebUI.take_percy_snapshot("Active Directory Setup")

    @allure.tag("defect_verification", "NAS-129528", "NAS-129686")
    @allure.issue("NAS-129686", "NAS-129686")
    def test_setup_active_directory_with_group_cache_disabled(self, ad_data, tear_down_class):
        """
        This test case test setup active directory with the group cache disabled.
        """
        # Setup SSH usage and dataset
        Navigation.navigate_to_dashboard()
        API_POST.start_service('ssh')
        API_POST.start_service('cifs')
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_POST.create_dataset("tank/group_cache_disabled_smb", "SMB")
        API_POST.create_dataset("tank/group_cache_disabled_unix")
        API_POST.create_dataset("tank/group_cache_disabled_nfsv4", "SMB")
        API_POST.create_dataset("tank/group_cache_disabled_POSIX")
        API_POST.create_share('smb', "group_cache_disabled_smb", "/mnt/tank/group_cache_disabled_smb")

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
        assert Common.is_checked("disable-freenas-cache") is True
        Common.close_right_panel()

        # Create SMB share with ACL
        Navigation.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('smb') is True
        SMB.click_edit_share_acl("group_cache_disabled_smb")
        SMB.add_additional_acl_who_entry("group", r"AD03\domain guests")
        Common.click_save_button_and_wait_for_right_panel()

        # Verify share functionality
        SMB.click_edit_share_acl("group_cache_disabled_smb")
        # Expected failure below: https://ixsystems.atlassian.net/browse/NAS-129686
        assert Common.assert_text_is_visible(r"AD03\domain guests") is True
        Common.close_right_panel()
        assert SMB.assert_user_can_access('group_cache_disabled_smb', ad_data['username'], ad_data['password']) is True

        # Navigate to datasets page and edit unix dataset group with manually typed AD group
        Navigation.navigate_to_datasets()
        Datasets.select_dataset("group_cache_disabled_unix")
        Datasets.click_edit_permissions_button()
        Permissions.set_apply_group_checkbox()
        Common.set_input_field('gid', r"AD03\domain guests", True)
        Common.click_save_button()

        # Verify unix dataset group has saved in UI and CLI
        assert Permissions.assert_dataset_group(r"AD03\domain guests") is True
        assert Perm_SSH.verify_getfacl_contains_permissions("/mnt/tank/group_cache_disabled_unix",
                                                            r"# group: AD03\\domain\040guests") is True

        # Edit POSIX dataset group with manually typed AD group
        Datasets.select_dataset("group_cache_disabled_POSIX")
        Datasets.click_edit_permissions_button()
        Permissions.click_set_acl_button()
        Common.assert_dialog_visible('Select a preset ACL')
        Common.click_radio_button("use-preset-create-a-custom-acl")
        Common.click_button('continue')
        Common.assert_page_header('Edit ACL')
        Permissions.click_add_item_button()
        Permissions.select_ace_who("group")
        Common.set_input_field("group", r"AD03\domain guests")
        Common.set_checkbox('permissions-read')
        Permissions.click_add_item_button()
        Permissions.select_ace_who("mask")
        Common.set_checkbox('permissions-read')
        Permissions.click_save_acl_button()

        # Verify POSIX dataset group has saved in UI and CLI
        assert Common.is_visible(xpaths.datasets.dataset_permissions_item(r'Group – AD03\domain guests', "Read")) is True
        assert Perm_SSH.verify_getfacl_contains_permissions("/mnt/tank/group_cache_disabled_POSIX",
                                                            r"group:AD03\\domain\040guests:r--") is True

        # Edit nfsv4 dataset group with manually typed AD group
        Datasets.select_dataset("group_cache_disabled_nfsv4")
        Datasets.click_edit_permissions_button()
        Permissions.click_add_item_button()
        Permissions.select_ace_who("group")
        Common.set_input_field("group", r"AD03\domain guests")
        Permissions.click_save_acl_button()

        # Verify nfsv4 dataset group has saved in UI and CLI
        assert Datasets.is_permissions_advanced_item_visible("Group", r"AD03\domain guests") is True
        assert Perm_SSH.verify_getfacl_contains_permissions("/mnt/tank/group_cache_disabled_nfsv4",
                                                            r"group:AD03\domain guests:rwxpDdaARWc--s:fd-----:allow",
                                                            "NFSv4") is True

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
        API_DELETE.delete_dataset("tank/group_cache_disabled_unix")
        API_DELETE.delete_dataset("tank/group_cache_disabled_nfsv4")
        API_DELETE.delete_dataset("tank/group_cache_disabled_POSIX")
        API_DELETE.delete_dataset("tank/group_cache_disabled_smb")
        API_DELETE.delete_share("smb", "group_cache_disabled_smb")
