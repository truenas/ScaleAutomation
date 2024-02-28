import xpaths
from keywords.webui.common import Common


class Active_Directory:
    @classmethod
    def assert_active_directory_right_panel(cls) -> bool:
        """
        This method checks if the Active Directory right panel is visible.
        :return: True if the Active Directory right panel is visible, otherwise it returns False.

        Example:
            - Active_Directory.assert_active_directory_right_panel()
        """
        return Common.assert_right_panel_header('Active Directory')

    @classmethod
    def assert_nameserver_failed_to_resolve_srv_record_message(cls, nameserver2) -> bool:
        """
        This method verify the nameserver failed to resolve SRV record message.
        :param nameserver2: The nameserver IP of that failed to resolve SRV record.
        :return: This method return True if the nameserver failed to resolve SRV record message is visible
        otherwise it returns False.

        Example:
            - Active_Directory.assert_nameserver_failed_to_resolve_srv_record_message('237.84.2.178')
        """
        message = f'Nameserver {nameserver2} failed to resolve SRV record for domain'
        return Common.assert_text_is_visible(message)

    @classmethod
    def click_advanced_options_button(cls) -> None:
        """
        This method clicks the Advanced Options button on the Active Directory Setup/Edit panel.

        Example:
            - Common.click_advanced_options_button()
        """
        Common.click_button('toggle-advanced')

    @classmethod
    def click_leave_domain_button(cls):
        """
        This method clicks the Leave Domain button.

        Example:
            - Active_Directory.click_leave_domain_button()
        """
        Common.click_button('leave-domain')

    @classmethod
    def click_rebuild_directory_service_cache_button(cls):
        """
        This method clicks the Rebuild Directory Service Cache button.

        Example:
            - Active_Directory.click_rebuild_directory_service_cache_button()
        """
        Common.click_button('rebuild-cache')

    @classmethod
    def click_save_button_and_wait_for_ad_to_finish_saving(cls):
        """
        This method clicks the save button and waits for the Active Directory dialog to disappear

        Example:
            - Active_Directory.click_save_button_and_wait_for_ad_to_finish_saving()
        """
        Common.click_save_button_and_wait_for_progress_bar()
        assert Common.assert_dialog_not_visible('Active Directory')

    @classmethod
    def click_the_dialog_leave_domain_button(cls):
        """
        This method clicks the Leave Domain button in the dialog.

        Example:
            - Active_Directory.click_the_dialog_leave_domain_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('leave-domain', 1))

        assert Common.assert_please_wait_not_visible()

    @classmethod
    def is_edit_active_directory_visible(cls) -> bool:
        """
        This method checks if the Edit Active Directory dialog is visible.
        :return: True if the Edit Active Directory dialog is visible, otherwise it returns False.

        Example:
            - Active_Directory.is_edit_active_directory_visible()
        """
        return Common.assert_right_panel_header('Active Directory')

    @classmethod
    def is_leave_domain_dialog_visible(cls) -> bool:
        """
        This method checks if the Leave Domain dialog is visible.
        :return: True if the Leave Domain dialog is visible, otherwise it returns False.

        Example:
            - Active_Directory.is_leave_domain_dialog_visible()
        """
        return Common.assert_dialog_visible('Leave Domain')

    @classmethod
    def select_kerberos_principal_option(cls, option: str) -> None:
        """
        This method click on Kerberos Principal and select an option.
        :param option: Is an option from Kerberos Principal that was previously added.

        Example:
            - Active_Directory.select_kerberos_principal_option('test-principal')
        """
        Common.select_option('kerberos-principal', f'kerberos-principal-{option}')

    @classmethod
    def select_kerberos_realm_option(cls, option: str) -> None:
        """
        This method click on Kerberos Realm and select an option.
        :param option: Is an option from Kerberos Realm that was previously added.

        Example:
            - Active_Directory.select_kerberos_realm_option('test-realm')
        """
        Common.select_option('kerberos-realm', f'kerberos-realm-{option}')

    @classmethod
    def select_winbind_nss_info_option(cls, option: str) -> None:
        """
        This method click on NSS Info and select an option
        :param option: Is on one of these values [sfu, sfu-20, rfc-2307]

        Example:
            - Active_Directory.select_winbind_nss_info_option('sfu')
        """
        Common.select_option('nss-info', f'nss-info-{option}')

    @classmethod
    def set_ad_timeout(cls, timeout: int) -> None:
        """
        This method sets the Active Directory timeout.
        :param timeout: The timeout in seconds.

        Example:
            - Active_Directory.set_ad_timeout(60)
        """
        Common.set_input_field('timeout', str(timeout))

    @classmethod
    def set_allow_dns_updates_checkbox(cls) -> None:
        """
        This method sets the Allows DNS Updates checkbox.

        Example:
            - Active_Directory.set_allow_dns_updates_checkbox()
        """
        Common.set_checkbox('allow-dns-updates')

    @classmethod
    def set_allow_trusted_domains_checkbox(cls) -> None:
        """
        This method sets the Allows Trusted Domains checkbox.

        Example:
            - Active_Directory.set_allow_trusted_domains_checkbox()
        """
        Common.set_checkbox('allow-trusted-doms')

    @classmethod
    def set_computer_account_ou(cls, ou: str) -> None:
        """
        This method sets the computer account OU input.
        :param ou: The name of the computer account OU.

        Example:
            - Active_Directory.set_computer_account_ou('TrueNAS_Server')
        """
        Common.set_input_field('createcomputer', ou)

    @classmethod
    def set_disable_ad_user_group_cache_checkbox(cls) -> None:
        """
        This method sets the Disable AD User Group Cache checkbox.

        Example:
            - Active_Directory.set_disable_ad_user_group_cache_checkbox()
        """
        Common.set_checkbox('disable-freenas-cache')

    @classmethod
    def set_domain_account_name(cls, username: str) -> None:
        """
        This method sets the domain account name input.
        :param username: The name of the domain account.

        Example:
            - Active_Directory.set_domain_account_name('admin')
        """
        Common.set_input_field('bindname', username)

    @classmethod
    def set_domain_account_password(cls, password: str) -> None:
        """
        This method sets the domain account password input.
        :param password: The password of the domain account.

        Example:
            - Active_Directory.set_domain_account_password('password')
        """
        Common.set_input_field('bindpw', password)

    @classmethod
    def set_domain_name(cls, domain: str) -> None:
        """
        This method sets the domain name input.
        :param domain: The name of the domain.

        Example:
            - Active_Directory.set_domain_name('example.com')
        """
        Common.set_input_field('domainname', domain)

    @classmethod
    def set_dns_timeout(cls, timeout: int) -> None:
        """
        This method sets the DNS timeout.
        :param timeout: The timeout in seconds.

        Example:
            - Active_Directory.set_dns_timeout(60)
        """
        Common.set_input_field('dns-timeout', str(timeout))

    @classmethod
    def set_enable_requires_password_or_kerberos_principal_checkbox(cls) -> None:
        """
        This method sets the Enable Requires Password or Kerberos Principal checkbox.

        Example:
            - Active_Directory.set_enable_requires_password_or_kerberos_principal_checkbox()
        """
        Common.set_checkbox('enable')

    @classmethod
    def set_leave_domain_password(cls, password: str) -> None:
        """
        This method sets the leave domain password input.
        :param password: The password of the domain account.

        Example:
            - Active_Directory.set_leave_domain_password('password')
        """
        Common.set_input_field('password', password)

    @classmethod
    def set_leave_domain_username(cls, username: str) -> None:
        """
        This method sets the leave domain username input.
        :param username: The name of the domain account.

        Example:
            - Active_Directory.set_leave_domain_username('admin')
        """
        Common.set_input_field('username', username)

    @classmethod
    def set_netbios_alias(cls, netbios_alias: str) -> None:
        """
        This method sets the netbios alias input.
        :param netbios_alias: The netbios alias.

        Example:
            - Active_Directory.set_netbios_alias('alias')
        """
        Common.set_input_field('netbiosalias', netbios_alias)

    @classmethod
    def set_netbios_name(cls, netbios_name: str) -> None:
        """
        This method sets the netbios name input.
        :param netbios_name: The netbios name.

        Example:
            - Active_Directory.set_netbios_name('name')
        """
        Common.set_input_field('netbiosname', netbios_name)

    @classmethod
    def set_restricted_pam_checkbox(cls) -> None:
        """
        This method sets the Restricted PAM checkbox.

        Example:
            - Active_Directory.set_restricted_pam_checkbox()
        """
        Common.set_checkbox('restrict-pam')

    @classmethod
    def set_site_name(cls, site) -> None:
        """
        This method sets the site name input.
        :param site: The name of the site.

        Example:
            - Active_Directory.set_site_name('site')
        """
        Common.set_input_field('site', site)

    @classmethod
    def set_use_default_domain_checkbox(cls) -> None:
        """
        This method sets the Use Default Domain checkbox.

        Example:
            - Active_Directory.set_use_default_domain_checkbox()
        """
        Common.set_checkbox('use-default-domain')

    @classmethod
    def set_verbose_logging_checkbox(cls):
        """
        This method sets the Verbose Logging checkbox.

        Example:
            - Active_Directory.set_verbose_logging_checkbox()
        """
        Common.set_checkbox('verbose-logging')

    @classmethod
    def unset_allow_dns_updates_checkbox(cls) -> None:
        """
        This method unsets the Allows DNS Updates checkbox.

        Example:
            - Active_Directory.unset_allow_dns_updates_checkbox()
        """
        Common.unset_checkbox('allow-dns-updates')

    @classmethod
    def unset_allow_trusted_domains_checkbox(cls) -> None:
        """
        This method unsets the Allows Trusted Domains checkbox.

        Example:
            - Active_Directory.unset_allow_trusted_domains_checkbox()
        """
        Common.unset_checkbox('allow-trusted-doms')

    @classmethod
    def unset_disable_ad_user_group_cache_checkbox(cls) -> None:
        """
        This method unsets the Disable AD User Group Cache checkbox.

        Example:
            - Active_Directory.unset_disable_ad_user_group_cache_checkbox()
        """
        Common.unset_checkbox('disable-freenas-cache')

    @classmethod
    def unset_enable_requires_password_or_kerberos_principal_checkbox(cls) -> None:
        """
        This method unsets the Enable Requires Password or Kerberos Principal checkbox.

        Example:
            - Active_Directory.unset_enable_requires_password_or_kerberos_principal_checkbox()
        """
        Common.unset_checkbox('enable')

    @classmethod
    def unset_restrict_pam_checkbox(cls) -> None:
        """
        This method unsets the Restricted PAM checkbox.

        Example:
            - Active_Directory.unset_restrict_pam_checkbox()
        """
        Common.unset_checkbox('restrict-pam')

    @classmethod
    def unset_use_default_domain_checkbox(cls) -> None:
        """
        This method unsets the Use Default Domain checkbox.

        Example:
            - Active_Directory.unset_use_default_domain_checkbox()
        """
        Common.unset_checkbox('use-default-domain')

    @classmethod
    def unset_verbose_logging_checkbox(cls) -> None:
        """
        This method unsets the Verbose Logging checkbox.

        Example:
            - Active_Directory.unset_verbose_logging_checkbox()
        """
        Common.unset_checkbox('verbose-logging')
