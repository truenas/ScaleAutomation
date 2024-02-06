import xpaths
from helper.webui import WebUI
from selenium.webdriver.common.keys import Keys
from keywords.webui.common import Common as COM


class NFS:

    @classmethod
    def assert_error_nfs_share_authorized_hosts_required(cls) -> bool:
        """
        This method returns True if 'Authorized Hosts and IP addresses is required' error message is visible, otherwise it returns False.

        :return: True if 'Authorized Hosts and IP addresses is required' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Authorized Hosts and IP addresses is required'))

    @classmethod
    def assert_error_nfs_share_network_invalid_ip(cls) -> bool:
        """
        This method returns True if 'Invalid IP address' error message is visible, otherwise it returns False.

        :return: True if 'Invalid IP address' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Invalid IP address'))

    @classmethod
    def assert_error_nfs_share_network_is_required(cls) -> bool:
        """
        This method returns True if 'Network is required' error message is visible, otherwise it returns False.

        :return: True if 'Network is required' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Network is required'))


    @classmethod
    def assert_error_nfs_share_mapall_user_override(cls) -> bool:
        """
        This method returns True if 'maproot_user disqualifies mapall_user' error message is visible, otherwise it returns False.

        :return: True if 'maproot_user disqualifies mapall_user' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('maproot_user disqualifies mapall_user'))

    @classmethod
    def assert_error_nfs_share_maproot_user_required(cls) -> bool:
        """
        This method returns True if 'This field is required when map group is specified' error message is visible, otherwise it returns False.

        :return: True if 'This field is required when map group is specified' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This field is required when map group is specified'))

    @classmethod
    def assert_error_nfs_share_path_duplicate(cls, sharepath: str) -> bool:
        """
        This method returns True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.

        :param sharepath: The path of the share
        :return: True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.
        """
        # TODO - Update with proper message when it is implemented.
        #   NAS-127220 - The Error Message For A Duplicate NFS Share Needs Clarification
        return COM.is_visible(xpaths.common_xpaths.any_text(f'ERROR - Export conflict. This share is exported to everybody and another share exports {sharepath} for'))

    @classmethod
    def assert_error_nfs_share_path_nonexistant(cls) -> bool:
        """
        This method returns True if 'This path does not exist.' error message is visible, otherwise it returns False.

        :return: True if 'This path does not exist.' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This path does not exist.'))

    @classmethod
    def assert_error_nfs_share_path_required(cls) -> bool:
        """
        This method returns True if 'Path is required' error message is visible, otherwise it returns False.

        :return: True if 'Path is required' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Path is required'))

    @classmethod
    def click_add_hosts_button(cls):
        """
        This method clicks the Add Hosts button on the NFS share edit panel.
        """
        COM.click_button('add-item-hosts')


    @classmethod
    def click_add_networks_button(cls):
        """
        This method clicks the Add Networks button on the NFS share edit panel.
        """
        COM.click_button('add-item-networks')

    @classmethod
    def click_remove_from_list_button(cls):
        """
        This method clicks the Remove From List button on the Network section of the NFS share edit panel.
        """
        COM.click_button('remove-from-list')

    @classmethod
    def set_host_and_ip(cls, text: str):
        """
        This method sets the Authorized Hosts and IP addresses field on the Hosts section of the NFS share edit panel.

        :param text: The text to enter.
        """
        cls.set_nfs_network_and_host_inputs(text, '2')

    @classmethod
    def set_mapall_group(cls, name: str):
        """
        This method sets the Mapall Group field on the NFS share edit panel.

        :param name: The name of the group.
        """
        COM.set_input_field('mapall-group', name, True)

    @classmethod
    def set_mapall_user(cls, name: str):
        """
        This method sets the Mapall User field on the NFS share edit panel.

        :param name: The name of the user.
        """
        COM.set_input_field('mapall-user', name, True)

    @classmethod
    def set_maproot_group(cls, name: str):
        """
        This method sets the Maproot Group field on the NFS share edit panel.

        :param name: The name of the group.
        """
        COM.set_input_field('maproot-group', name, True)

    @classmethod
    def set_maproot_user(cls, name: str):
        """
        This method sets the Maproot User field on the NFS share edit panel.

        :param name: The name of the user.
        """
        COM.set_input_field('maproot-user', name, True)

    @classmethod
    def set_network(cls, network: str):
        """
        This method sets the Network input on the Network section of the NFS share edit panel.

        :param network: The ip of the network.
        """
        cls.set_nfs_network_and_host_inputs(network, '1')

    @classmethod
    def set_network_mask(cls, netmask: str):
        """
        This method selects the specified netmask on the Network section of the NFS share edit panel.

        :param netmask: The netmask.
        """
        COM.select_option('netmasks', f'netmask-{netmask}')

    @classmethod
    def set_nfs_network_and_host_inputs(cls, text: str, index: str):
        """
        This method selects the specified netmask on the Network section of the NFS share edit panel.

        :param text: The text to enter
        :param index: The index of the input elements to select
        """
        path = xpaths.common_xpaths.any_xpath(f'(//*[@data-test="input"])[{index}]')
        WebUI.wait_until_visible(path)
        WebUI.xpath(path).clear()
        WebUI.xpath(path).send_keys(text)
        WebUI.xpath(path).send_keys(Keys.TAB)

    @classmethod
    def set_security_type(cls, securitytype: str):
        """
        This method selects the security type of the share on the NFS share edit panel.

        :param securitytype: The security type to select.
        """
        COM.select_option('security', f'security-{securitytype}')

    @classmethod
    def unset_mapall_group(cls):
        """
        This method unsets the Mapall Group field on the NFS share edit panel.
        """
        COM.clear_input_field('mapall-group', True)

    @classmethod
    def unset_mapall_user(cls):
        """
        This method unsets the Mapall User field on the NFS share edit panel.
        """
        COM.clear_input_field('mapall-user', True)

    @classmethod
    def unset_maproot_group(cls):
        """
        This method unsets the Maproot Group field on the NFS share edit panel.
        """
        COM.clear_input_field('maproot-group', True)

    @classmethod
    def unset_maproot_user(cls):
        """
        This method unsets the Maproot User field on the NFS share edit panel.
        """
        COM.clear_input_field('maproot-user', True)

