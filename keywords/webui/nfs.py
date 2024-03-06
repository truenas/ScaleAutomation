import xpaths
from helper.webui import WebUI
from selenium.webdriver.common.keys import Keys
from keywords.webui.common import Common as COM


class NFS:

    @classmethod
    def assert_error_nfs_share_authorized_hosts_required(cls) -> bool:
        """
        This method returns True if 'Authorized Hosts and IP addresses is required' error message is visible,
         otherwise it returns False.

        :return: True if 'Authorized Hosts and IP addresses is required' error message is visible,
         otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_authorized_hosts_required()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Authorized Hosts and IP addresses is required'))

    @classmethod
    def assert_error_nfs_share_network_invalid_ip(cls) -> bool:
        """
        This method returns True if 'Invalid IP address' error message is visible, otherwise it returns False.

        :return: True if 'Invalid IP address' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_network_invalid_ip()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Invalid IP address'))

    @classmethod
    def assert_error_nfs_share_network_is_required(cls) -> bool:
        """
        This method returns True if 'Network is required' error message is visible, otherwise it returns False.

        :return: True if 'Network is required' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_network_is_required()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Network is required'))

    @classmethod
    def assert_error_nfs_share_mapall_user_override(cls) -> bool:
        """
        This method returns True if 'maproot_user disqualifies mapall_user' error message is visible,
        otherwise it returns False.

        :return: True if 'maproot_user disqualifies mapall_user' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_mapall_user_override()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('maproot_user disqualifies mapall_user'))

    @classmethod
    def assert_error_nfs_share_maproot_user_required(cls) -> bool:
        """
        This method returns True if 'This field is required when map group is specified' error message is visible,
        otherwise it returns False.

        :return: True if 'This field is required when map group is specified' error message is visible,
        otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_maproot_user_required()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This field is required when map group is specified'))

    @classmethod
    def assert_error_nfs_share_path_duplicate(cls, sharepath: str) -> bool:
        """
        This method returns True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.

        :param sharepath: The path of the share
        :return: True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_path_duplicate()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text(
            f'ERROR - Export conflict. Another share with the same path exports {sharepath} for'))

    @classmethod
    def assert_error_nfs_share_path_nonexistent(cls) -> bool:
        """
        This method returns True if 'This path does not exist.' error message is visible, otherwise it returns False.

        :return: True if 'This path does not exist.' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_path_nonexistent()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This path does not exist.'))

    @classmethod
    def assert_error_nfs_share_path_required(cls) -> bool:
        """
        This method returns True if 'Path is required' error message is visible, otherwise it returns False.

        :return: True if 'Path is required' error message is visible, otherwise it returns False.

        Example:
            - NFS.assert_error_nfs_share_path_required()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Path is required'))

    @classmethod
    def click_add_hosts_button(cls):
        """
        This method clicks the Add Hosts button on the NFS share edit panel.

        Example:
            - NFS.click_add_hosts_button()
        """
        COM.click_button('add-item-hosts')

    @classmethod
    def click_add_networks_button(cls):
        """
        This method clicks the Add Networks button on the NFS share edit panel.

        Example:
            - NFS.click_add_networks_button()
        """
        COM.click_button('add-item-networks')

    @classmethod
    def click_remove_from_list_button(cls):
        """
        This method clicks the Remove From List button on the Network section of the NFS share edit panel.

        Example:
            - NFS.click_remove_from_list_button()
        """
        COM.click_button('remove-from-list')

    @classmethod
    def set_host_and_ip(cls, text: str):
        """
        This method sets the Authorized Hosts and IP addresses field on the Hosts section of the NFS share edit panel.

        :param text: The text to enter.

        Example:
            - NFS.set_host_and_ip('0.0.0.0')
        """
        cls.set_nfs_network_and_host_inputs('Hosts', text)

    @classmethod
    def set_mapall_group(cls, name: str):
        """
        This method sets the Mapall Group field on the NFS share edit panel.

        :param name: The name of the group.

        Example:
            - NFS.set_mapall_group('group1')
        """
        COM.set_input_field('mapall-group', name, True)
        WebUI.delay(0.2)

    @classmethod
    def set_mapall_user(cls, name: str):
        """
        This method sets the Mapall User field on the NFS share edit panel.

        :param name: The name of the user.

        Example:
            - NFS.set_mapall_user('user1')
        """
        COM.set_input_field('mapall-user', name, True)
        WebUI.delay(0.2)

    @classmethod
    def set_maproot_group(cls, name: str):
        """
        This method sets the Maproot Group field on the NFS share edit panel.

        :param name: The name of the group.

        Example:
            - NFS.set_maproot_group('group1')
        """
        COM.set_input_field('maproot-group', name, True)
        WebUI.delay(0.2)

    @classmethod
    def set_maproot_user(cls, name: str):
        """
        This method sets the Maproot User field on the NFS share edit panel.

        :param name: The name of the user.

        Example:
            - NFS.set_maproot_user('user1')
        """
        COM.set_input_field('maproot-user', name, True)
        WebUI.delay(0.2)

    @classmethod
    def set_network(cls, network: str):
        """
        This method sets the Network input on the Network section of the NFS share edit panel.

        :param network: The ip of the network.

        Example:
            - NFS.set_network('0.0.0.0')
        """
        cls.set_nfs_network_and_host_inputs('Network', network)

    @classmethod
    def set_network_mask(cls, netmask: str):
        """
        This method selects the specified netmask on the Network section of the NFS share edit panel.

        :param netmask: The netmask.

        Example:
            - NFS.set_network_mask('24)
        """
        COM.select_option('netmasks', f'netmask-{netmask}')

    @classmethod
    def set_nfs_network_and_host_inputs(cls, field: str, text: str):
        """
        This method selects the specified netmask on the Network section of the NFS share edit panel.

        :param field: The field to select (Network or Hosts)
        :param text: The text to enter.

        Example:
            - NFS.set_nfs_network_and_host_inputs('Hosts', '0.0.0.0')
        """
        path = xpaths.common_xpaths.any_xpath(
            f'//*[contains(text(), "{field}")]/ancestor::ix-list//*[@data-test="input"]')
        assert WebUI.wait_until_visible(path) is True
        WebUI.xpath(path).clear()
        WebUI.xpath(path).send_keys(text)
        WebUI.xpath(path).send_keys(Keys.TAB)

    @classmethod
    def set_security_type(cls, security_type: str):
        """
        This method selects the security type of the share on the NFS share edit panel.

        :param security_type: The security type to select.

        Example:
            - NFS.set_security_type('sys')
        """
        COM.select_option('security', f'security-{security_type}')

    @classmethod
    def unset_mapall_group(cls):
        """
        This method unsets the Mapall Group field on the NFS share edit panel.

        Example:
            - NFS.unset_mapall_group()
        """
        COM.clear_input_field('mapall-group', True)
        WebUI.delay(0.2)

    @classmethod
    def unset_mapall_user(cls):
        """
        This method unsets the Mapall User field on the NFS share edit panel.

        Example:
            - NFS.unset_mapall_user()
        """
        COM.clear_input_field('mapall-user', True)
        WebUI.delay(0.2)

    @classmethod
    def unset_maproot_group(cls):
        """
        This method unsets the Maproot Group field on the NFS share edit panel.

        Example:
            - NFS.unset_maproot_group()
        """
        COM.clear_input_field('maproot-group', True)
        WebUI.delay(0.2)

    @classmethod
    def unset_maproot_user(cls):
        """
        This method unsets the Maproot User field on the NFS share edit panel.

        Example:
            - NFS.unset_maproot_user()
        """
        COM.clear_input_field('maproot-user', True)
        WebUI.delay(0.2)

    @classmethod
    def verify_nfs_service_edit_ui(cls) -> None:
        """
        This method verifies the edit UI of the NFS service.

        Example:
            - NFS.verify_nfs_service_edit_ui()
        """
        assert COM.is_visible(xpaths.common_xpaths.select_field('bindip')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('servers-auto')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('v-4-v-3-owner')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('v-4-krb')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('mountd-port')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('rpcstatd-port')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('rpclockd-port')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('allow-nonroot')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('userd-manage-gids')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_nfs_sessions_page_opens(cls) -> None:
        """
        This method verifies the NFS Sessions page is opens.

        Example:
            - NFS.verify_nfs_sessions_page_opens()
        """
        if COM.assert_page_header('Services'):
            COM.click_link('nfs-sessions')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('NFS'))
            COM.click_button('nfs-actions-menu-sessions')
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('NFS Sessions') is True
