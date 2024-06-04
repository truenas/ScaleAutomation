import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.ldap import API_LDAP
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common
from keywords.webui.active_directory import Active_Directory
from keywords.webui.directory_services import Directory_Services
from keywords.webui.navigation import Navigation


@allure.tag('Read Only Admin', 'Directory Services', 'Permissions', 'Users')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Directory_Services:

    @pytest.fixture(scope='function')
    def setup_ad(self, ad_data):
        """
        This setup fixture sets up the active directory for test that need it.
        """
        API_PUT.set_nameservers(ad_data['nameserver'])
        API_PUT.join_active_directory(ad_data['username'], ad_data['password'], ad_data['domain'])

        Navigation.navigate_to_directory_services()
        assert Directory_Services.assert_directory_services_page_header() is True

    @pytest.fixture(scope='function')
    def setup_ldap(self, ldap_data):
        """
        This setup fixture sets up the LDAP for test that need it.
        """
        API_LDAP.configure_ldap(ldap_data['basedn'], ldap_data['binddn'], ldap_data['bindpassword'], ldap_data['domain'])

        Navigation.navigate_to_directory_services()
        assert Directory_Services.assert_directory_services_page_header() is True

    @pytest.fixture(scope='function')
    def teardown_ad(self, ad_data):
        """
        This teardown fixture tears down the active directory for test that need it.
        """
        yield
        API_POST.leave_active_directory(ad_data['username'], ad_data['password'])
        API_PUT.set_nameservers(ad_data['nameserver1'], ad_data['nameserver2'])

    @pytest.fixture(scope='function')
    def teardown_ldap(self, ldap_data):
        """
        This teardown fixture tears down the LDAP for test that need it.
        """
        yield
        API_LDAP.disable_ldap()

    @pytest.fixture(scope='function')
    def navigate_to_directory_services(self):
        """
        This fixture navigates to Directory services page.
        """
        Navigation.navigate_to_directory_services()
        assert Directory_Services.assert_directory_services_page_header() is True

    @allure.tag('Update', 'Active Directory')
    @allure.story('Read Only Admin Is Not Able to Configure Active Directory')
    def test_read_only_admin_is_not_able_to_configure_active_directory(self, navigate_to_directory_services):
        """
        This test verifies the read-only admin is not able to configure active directory.
        1. Navigate to Directory services page
        2. Verify that the configure active directory button is restricted
        """
        assert Directory_Services.assert_configure_active_directory_button_is_restricted() is True

    @allure.tag('Update', 'LDAP')
    @allure.story('Read Only Admin Is Not Able to Configure LDAP')
    def test_read_only_admin_is_not_able_to_configure_ldap(self, navigate_to_directory_services):
        """
        This test verifies the read-only admin is not able to configure LDAP.
        1. Navigate to Directory services page
        2. Verify that the configure ldap button is restricted
        """
        assert Directory_Services.assert_configure_ldap_button_is_restricted() is True

    @allure.tag('Create', 'Kerberos', 'Advanced Settings')
    @allure.story('Read Only Admin Is Not Able to Add Kerberos and Idmap in Advanced Settings')
    def test_read_only_admin_is_not_to_add_kerberos_and_idmap_in_advanced_settings(self, navigate_to_directory_services):
        """
        This test verifies the read-only admin is not able to add kerberos and idmap in advanced settings.
        1. Navigate to Directory services page
        2. Verify that the Add idmap button is restricted
        3. Verify that the Add kerberos keytab button is restricted
        4. Verify that the Add kerberos realms button is restricted
        """
        Directory_Services.click_show_advanced_settings_button()
        assert Directory_Services.assert_add_idmap_button_is_restricted() is True
        assert Directory_Services.assert_add_kerberos_keytab_button_is_restricted() is True
        assert Directory_Services.assert_add_kerberos_realms_button_is_restricted() is True

    @allure.tag('Read', 'Active Directory')
    @allure.story('Read Only Admin Is Able to View Pre-Configured Active Directory')
    @pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
    def test_read_only_admin_is_able_to_view_pre_configured_active_directory(self, ad_data, setup_ad, teardown_ad):
        """
        This test verifies the read-only admin is able to view pre-configured active directory.
        1. Configure active directory as admin
        2. Navigate to Directory services page as read-only admin
        3. Verify that the Active Directory card information is visible
        """
        assert Directory_Services.assert_active_directory_card_visible() is True
        assert Directory_Services.assert_any_service_status() is True
        assert Directory_Services.assert_active_directory_domain_name(ad_data['domain']) is True
        assert Directory_Services.assert_active_directory_domain_account_name(ad_data['username']) is True

    @allure.tag('Read', 'LDAP')
    @allure.story('Read Only Admin Is Able to View Pre-Configured LDAP')
    @pytest.mark.parametrize('ldap_data', get_data_list('ldap_credentials'), scope='class')
    def test_read_only_admin_is_able_to_view_pre_configured_ldap(self, ldap_data, setup_ldap, teardown_ldap):
        """
        This test verifies the read-only admin is able to view pre-configured LDAP.
        1. Configure LDAP as admin
        2. Navigate to Directory services page as read-only admin
        3. Verify that the LDAP card information is visible
        """
        assert Directory_Services.assert_ldap_card() is True
        assert Directory_Services.assert_any_service_status() is True
        assert Common.get_label_value('Hostname:') == ldap_data['domain']
        assert Common.get_label_value('Base DN:') == ldap_data['basedn']
        assert Common.get_label_value('Bind DN:') == ldap_data['binddn']

    @allure.tag('Read', 'Advanced Settings')
    @allure.story('Read Only Admin Is Able to View Directory Services Advanced Settings')
    @pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
    def test_read_only_admin_is_able_to_view_directory_services_advanced_settings(self, ad_data, setup_ad, teardown_ad):
        """
        This test verifies the read-only admin is able to view Directory services advanced settings.
        1. Configure active directory as admin
        2. Navigate to Directory services page as read-only admin
        3. Click on Show advanced settings button
        4. Verify that the idmap card header is visible
        5. Verify that the idmap active directory primary domain is visible
        6. Verify that the idmap smb primary domain is visible
        7. Verify that the kerberos card header is visible
        8. Verify that the kerberos realm is visible
        9. Verify that the kerberos settings card header is visible
        10. Verify that the kerberos setting Appdefaults Auxiliary Parameters value is visible
        11. Verify that the kerberos setting Libdefaults Auxiliary Parameters value is visible
        12. Verify that the kerberos keytab card header is visible
        13. Verify that the kerberos keytab ad machine account is visible
        """
        Directory_Services.click_show_advanced_settings_button()
        assert Directory_Services.is_idmap_card_header_visible() is True
        assert Directory_Services.assert_idmap_active_directory_primary_domain() is True
        assert Directory_Services.assert_idmap_smb_primary_domain() is True

        assert Directory_Services.is_kerberos_realms_card_header_visible() is True
        assert Directory_Services.assert_kerberos_realm(ad_data['realm_xpath']) is True

        assert Directory_Services.is_kerberos_settings_card_header_visible() is True
        assert Directory_Services.assert_kerberos_setting_appdefaults_auxiliary_parameters_value('None') is True
        assert Directory_Services.assert_kerberos_setting_libdefaults_auxiliary_parameters_value('None') is True

        assert Directory_Services.is_kerberos_keytab_card_header_visible() is True
        assert Directory_Services.assert_kerberos_keytab_ad_machine_account() is True

    @allure.tag('Update', 'Active Directory')
    @allure.story('Read Only Admin Is Not Able to Modify Pre-Configured Active Directory')
    @pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
    def test_read_only_admin_is_not_able_to_modify_pre_configured_active_directory(self, ad_data, setup_ad, teardown_ad):
        """
        This test verifies the read-only admin is not able to modify pre-configured active directory.
        1. Configure Active Directory as admin
        2. Navigate to Directory services page as read-only admin
        3. Click on Active Directory settings button
        4. Verify that the Active Directory save button is restricted
        """
        assert Directory_Services.assert_active_directory_card_visible() is True
        Directory_Services.click_active_directory_settings_button()
        assert Active_Directory.is_edit_active_directory_visible() is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

    @allure.tag('Update', 'LDAP')
    @allure.story('Read Only Admin Is Not Able to Modify Pre-Configured LDAP')
    @pytest.mark.parametrize('ldap_data', get_data_list('ldap_credentials'), scope='class')
    def test_read_only_admin_is_not_able_to_modify_pre_configured_ldap(self, ldap_data, setup_ldap, teardown_ldap):
        """
        This test verifies the read-only admin is not able to modify pre-configured LDAP.
        1. Configure LDAP as admin
        2. Navigate to Directory services page as read-only admin
        3. Click on LDAP settings button
        4. Verify that the LDAP save button is restricted
        """
        assert Directory_Services.assert_ldap_card() is True
        Directory_Services.click_ldap_settings_button()
        assert Common.assert_right_panel_header('LDAP') is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True

        Common.close_right_panel()

    @allure.tag('Update', 'Advanced Settings')
    @allure.story('Read Only Admin Is Not Able to Modify Directory Services Advanced Settings')
    @pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
    def test_read_only_admin_is_not_able_to_modify_directory_services_advanced_settings(self, ad_data, setup_ad, teardown_ad):
        """
        This test verifies the read-only admin is not able to modify any directory service advanced settings.
        1. Configure Active Directory as admin
        2. Navigate to Directory services page as read-only admin
        3. Click on Show advanced settings button
        4. Click on idmap active directory primary domain edit button
        5. Verify that the idmap save button is restricted
        6. Click on kerberos realm edit button
        7. Verify that the kerberos save button is restricted
        8. Click on kerberos keytab ad machine account edit button
        9. Verify that the kerberos keytab save button is restricted
        10. Click on kerberos settings button
        11. Verify that the kerberos settings save button is restricted
        """
        Directory_Services.click_show_advanced_settings_button()
        assert Directory_Services.is_idmap_card_header_visible() is True
        Directory_Services.click_idmap_active_directory_primary_domain_edit_button()
        assert Common.assert_right_panel_header('Edit Idmap') is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

        assert Directory_Services.is_kerberos_realms_card_header_visible() is True
        Directory_Services.click_kerberos_realm_edit_button(ad_data['realm_xpath'])
        assert Common.assert_right_panel_header('Edit Kerberos Realm') is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

        assert Directory_Services.is_kerberos_keytab_card_header_visible() is True
        Directory_Services.click_kerberos_keytab_ad_machine_account_edit_button()
        assert Common.assert_right_panel_header('Edit Kerberos Keytab') is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

        Directory_Services.click_kerberos_settings_button()
        assert Common.assert_right_panel_header('Kerberos Settings') is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()
