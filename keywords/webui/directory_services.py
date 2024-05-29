import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Directory_Services:

    @classmethod
    def assert_active_directory_card_not_visible(cls) -> bool:
        """
        This method checks if the Active Directory card is visible.
        :return: True if the Active Directory card is visible, otherwise it returns False.

        Example:
            - Directory_Services.assert_active_directory_card_visible()
        """
        return COM.is_card_not_visible('Active Directory')

    @classmethod
    def assert_active_directory_card_visible(cls) -> bool:
        """
        This method checks if the Active Directory card is visible.
        :return: True if the Active Directory card is visible, otherwise it returns False.

        Example:
            - Directory_Services.assert_active_directory_card_visible()
        """
        return COM.is_card_visible('Active Directory')

    @classmethod
    def assert_active_directory_domain_account_name(cls, username: str) -> bool:
        """
        This method verifies the given domain account name is visible.
        :param username: The name of the domain account.
        :return: Ture if the given domain account name is visible otherwise it returns False.

        Example:
            - Directory_Services.assert_active_directory_domain_account_name('admin')
        """
        return COM.assert_label_and_value_exist('Domain Account Name:', username)

    @classmethod
    def assert_active_directory_domain_name(cls, domain: str) -> bool:
        """
        This method verifies the given domain name is visible.
        :param domain: The name of the domain.
        :return: Ture if the given domain name is visible otherwise it returns False.

        Example:
            - Directory_Services.assert_active_directory_domain_name('admin')
        """
        return COM.assert_label_and_value_exist('Domain Name:', domain.upper())

    @classmethod
    def assert_add_kerberos_keytab_button_is_restricted(cls) -> bool:
        """
        This method returns True if the Add kerberos keytab button is restricted, otherwise False.
        :return: True if the add kerberos keytab button is restricted, otherwise False.

        Example:
            - Directory_Services.assert_add_kerberos_keytab_button_is_restricted()
        """
        return COM.assert_button_is_restricted('add-kerberos-keytabs')

    @classmethod
    def assert_add_kerberos_realms_button_is_restricted(cls) -> bool:
        """
        This method returns True if the Add kerberos realms button is restricted, otherwise False.
        :return: True if the add kerberos realms button is restricted, otherwise False.

        Example:
            - Directory_Services.assert_add_kerberos_realms_button_is_restricted()
        """
        return COM.assert_element_is_restricted(xpaths.common_xpaths.button_field_by_row('add-idmap', 2))

    @classmethod
    def assert_add_idmap_button_is_restricted(cls) -> bool:
        """
        This method returns True if the Add idmap button is restricted, otherwise False.
        :return: True if the add idmap button is restricted, otherwise False.

        Example:
            - Directory_Services.assert_add_idmap_button_is_restricted()
        """
        return COM.assert_element_is_restricted(xpaths.common_xpaths.button_field_by_row('add-idmap', 1))

    @classmethod
    def assert_configure_active_directory_button_is_restricted(cls) -> bool:
        """
        This method returns True if the configure active directory button is restricted, otherwise False.
        :return: True if the configure active directory button is restricted, otherwise False.

        Example:
            - Directory_Services.assert_configure_active_directory_button_is_restricted()
        """
        return COM.assert_button_is_restricted('configure-active-directory')

    @classmethod
    def assert_configure_ldap_button_is_restricted(cls) -> bool:
        """
        This method returns True if the configure ldap button is restricted, otherwise False.
        :return: True if the configure ldap button is restricted, otherwise False.

        Example:
            - Directory_Services.assert_configure_ldap_button_is_restricted()
        """
        return COM.assert_button_is_restricted('configure-ldap')

    @classmethod
    def assert_directory_services_page_header(cls) -> bool:
        """
        This method returns True if the Directory Services page is displayed, otherwise False.
        :return: is the name of the service to start.

        Example:
            - Directory_Services.assert_directory_services_page_header()
        """
        return COM.assert_page_header('Directory Services')

    @classmethod
    def assert_idmap_active_directory_primary_domain(cls):
        """
        This method returns True if the idmap active directory primary domain is displayed, otherwise False.
        :return: True if the idmap active directory primary domain is displayed, otherwise False.

        Example:
            - Directory_Services.assert_idmap_active_directory_primary_domain()
        """
        return WebUI.wait_until_visible(xpaths.directory_services.idmap_active_directory_primary_domain)

    @classmethod
    def assert_idmap_smb_primary_domain(cls):
        """
        This method returns True if the idmap smb primary domain is displayed, otherwise False.
        :return: True if the idmap smb primary domain is displayed, otherwise False.

        Example:
            - Directory_Services.assert_idmap_smb_primary_domain()
        """
        return WebUI.wait_until_visible(xpaths.directory_services.idmap_smb_primary_domain)

    @classmethod
    def assert_kerberos_keytab_ad_machine_account(cls):
        """
        This method returns True if the kerberos keytab ad machine account is displayed, otherwise False.
        :return: True if the kerberos keytab ad machine account is displayed, otherwise False.

        Example:
            - Directory_Services.assert_kerberos_keytab_ad_machine_account()
        """
        return WebUI.wait_until_visible(xpaths.directory_services.kerberos_keytab_ad_machine_account)

    @classmethod
    def assert_kerberos_realm(cls, realm_xpath: str) -> bool:
        """
        This method returns True if the kerberos realm is displayed, otherwise False.
        :param realm_xpath: The xpath of the kerberos realm
        :return: True if the kerberos realm is displayed, otherwise False.

        Example:
            - Directory_Services.assert_kerberos_realm('realm')
        """
        return WebUI.wait_until_visible(xpaths.directory_services.kerberos_realm(realm_xpath))

    @classmethod
    def assert_kerberos_setting_appdefaults_auxiliary_parameters_value(cls, value: str) -> bool:
        """
        This method returns True if the kerberos setting Appdefaults Auxiliary Parameters value is displayed, otherwise False.
        :param value: The value of the Appdefaults Auxiliary Parameters kerberos setting
        :return: True if the kerberos setting Appdefaults Auxiliary Parameters value is displayed, otherwise False.

        Example:
            - Directory_Services.assert_kerberos_setting_appdefaults_auxiliary_parameters_value('value')
        """
        return COM.assert_label_and_value_exist('Appdefaults Auxiliary Parameters:', value)

    @classmethod
    def assert_kerberos_setting_libdefaults_auxiliary_parameters_value(cls, value: str) -> bool:
        """
        This method returns True if the kerberos setting Libdefaults Auxiliary Parameters value is displayed, otherwise False.
        :param value: The value of the Libdefaults Auxiliary Parameters kerberos setting
        :return: True if the kerberos setting Libdefaults Auxiliary Parameters value is displayed, otherwise False.

        Example:
            - Directory_Services.assert_kerberos_setting_libdefaults_auxiliary_parameters_value('value')
        """
        return COM.assert_label_and_value_exist('Libdefaults Auxiliary Parameters:', value)

    @classmethod
    def assert_ldap_card(cls) -> bool:
        """
        This method returns True if the LDAP card is displayed, otherwise False.

        :return: True if the LDAP card is displayed, otherwise False.

        Example:
            - Directory_Services.assert_ldap_card()
        """
        return COM.is_card_visible('LDAP')

    @classmethod
    def assert_ldap_edit_panel(cls) -> bool:
        """
        This method returns True if the LDAP edit panel is displayed, otherwise False.

        :return: True if the LDAP edit panel is displayed, otherwise False.

        Example:
            - Directory_Services.assert_ldap_edit_panel()
        """
        return COM.assert_right_panel_header('LDAP')

    @classmethod
    def assert_service_status(cls, status: str) -> bool:
        """
        This method verifies the given service status is visible.
        :param status: The name of the service.
        :return: True if the given service status is visible otherwise it returns False.
        """
        return COM.assert_label_and_value_exist('Status:', status.upper())

    @classmethod
    def click_active_directory_settings_button(cls) -> None:
        """
        This method clicks the active directory settings button.

        Example:
            - Directory_Services.click_active_directory_settings_button()
        """
        COM.click_button('active-directory-settings')

    @classmethod
    def click_configure_active_directory_button(cls) -> None:
        """
        This method clicks the configure active directory button.

        Example:
            - Directory_Services.click_configure_active_directory_button()
        """
        COM.click_button('configure-active-directory')

    @classmethod
    def click_configure_ldap_button(cls) -> None:
        """
        This method clicks the configure ldap button.

        Example:
            - Directory_Services.click_configure_ldap_button()
        """
        if cls.assert_ldap_card() is True:
            cls.remove_ldap()
        COM.click_button('configure-ldap')

    @classmethod
    def click_idmap_active_directory_primary_domain_edit_button(cls) -> None:
        """
        This method clicks the edit button of the idmap active directory primary domain.

        Example:
            - Directory_Services.click_idmap_active_directory_primary_domain_edit_button()
        """
        COM.click_button('idmap-ds-type-activedirectory-edit-row-action')

    @classmethod
    def click_idmap_smb_primary_domain_edit_button(cls) -> None:
        """
        This method clicks the edit button of the idmap smb primary domain.

        Example:
            - Directory_Services.click_idmap_smb_primary_domain_edit_button()
        """
        COM.click_button('idmap-ds-type-default-domain-edit-row-action')

    @classmethod
    def click_kerberos_keytab_ad_machine_account_edit_button(cls) -> None:
        """
        This method clicks the edit button of the kerberos keytab ad machine account.

        Example:
            - Directory_Services.click_kerberos_keytab_ad_machine_account_edit_button()
        """
        COM.click_button('kerberos-keytab-ad-machine-account-edit-row-action')

    @classmethod
    def click_kerberos_realm_edit_button(cls, realm_xpath: str) -> None:
        """
        This method clicks the edit button of the kerberos realm.
        :param realm_xpath: The xpath of the kerberos realm.

        Example:
            - Directory_Services.click_kerberos_realm_edit_button('realm-xpath')
        """
        COM.click_button(f'kerberos-realm-{realm_xpath}-edit-row-action')

    @classmethod
    def click_kerberos_settings_button(cls) -> None:
        """
        This method clicks the kerberos settings button.

        Example:
            - Directory_Services.click_kerberos_settings_button()
        """
        COM.click_button('kerberos-settings-settings')

    @classmethod
    def click_ldap_settings_button(cls) -> None:
        """
        This method clicks the configure ldap button.

        Example:
            - Directory_Services.click_ldap_settings_button()
        """
        COM.click_button('ldap-settings')

    @classmethod
    def click_show_advanced_settings_button(cls) -> None:
        """
        This method clicks the show advanced settings button and confirms the dialog.

        Example:
            - Directory_Services.click_show_advanced_settings_button()
        """
        COM.click_button('show-advanced-settings')
        assert COM.assert_dialog_visible('Warning')
        COM.click_button('dialog-confirm')

    @classmethod
    def is_idmap_card_header_visible(cls) -> bool:
        """
        This method verifies if the idmap card header is visible.
        :return: True if the idmap card header is visible, otherwise False.

        Example:
            - Directory_Services.is_idmap_card_header_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Idmap', 3))

    @classmethod
    def is_kerberos_keytab_card_header_visible(cls) -> bool:
        """
        This method verifies if the kerberos keytab card is visible.
        :return: True if the kerberos keytab card is visible, otherwise False.

        Example:
            - Directory_Services.is_kerberos_keytab_card_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Kerberos Keytab', 3))

    @classmethod
    def is_kerberos_realms_card_header_visible(cls) -> bool:
        """
        This method verifies if the kerberos realm card is visible.
        :return: True if the kerberos realm card is visible, otherwise False.

        Example:
            - Directory_Services.is_kerberos_realm_card_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Kerberos Realms', 3))

    @classmethod
    def is_kerberos_settings_card_header_visible(cls) -> bool:
        """
        This method verifies if the kerberos settings card is visible.
        :return: True if the kerberos settings card is visible, otherwise False.

        Example:
            - Directory_Services.is_kerberos_settings_card_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Kerberos Settings', 3))

    @classmethod
    def is_ldap_configure_button_visible(cls) -> bool:
        """
        This method returns True if the configure ldap button is visible, otherwise False.

        :return: True if the configure ldap button is visible, otherwise False.

        Example:
            - Directory_Services.is_ldap_configure_button_visible()
        """
        return COM.is_visible('//*[@data-test="button-configure-ldap"]')

    @classmethod
    def remove_ldap(cls) -> None:
        """
        This method removes the existing ldap configuration.

        Example:
            - Directory_Services.remove_ldap()
        """
        if COM.is_visible(xpaths.common_xpaths.any_text('Active Directory and LDAP are disabled.')) is False:
            if not COM.is_visible(xpaths.common_xpaths.any_text('To enable disable Active Directory first.')):
                if COM.is_visible(xpaths.common_xpaths.button_field('configure-ldap')):
                    cls.click_configure_ldap_button()
                if COM.is_visible(xpaths.common_xpaths.button_field('ldap-settings')):
                    cls.click_ldap_settings_button()
                while COM.is_visible('//mat-chip-row//*[@name="cancel"]'):
                    COM.delete_pill('//mat-chip-row')
                while COM.is_visible('//*[@name="mdi-close-circle"]'):
                    COM.click_on_element('//*[@name="mdi-close-circle"]')
                COM.clear_input_field('bindpw')
                COM.unset_checkbox('enable')
                COM.click_save_button()
                if COM.is_visible(xpaths.common_xpaths.any_text('Error: has_samba_schema')):
                    print("Error: has_samba_schem encountered. NAS-128958")
                    COM.click_error_dialog_close_button()
                    COM.close_right_panel()
        assert COM.is_card_not_visible('LDAP') is True
        assert cls.is_ldap_configure_button_visible() is True
