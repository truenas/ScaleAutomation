import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class iSCSI:

    @classmethod
    def assert_edit_iscsi_target_panel_header(cls) -> bool:
        """
        This method asserts the header of the Edit iSCSI Target panel.

        :return: True if the header of the Edit iSCSI Target panel is displayed, otherwise it returns False.

        Example:
            - iSCSI.assert_edit_iscsi_target_panel_header()
        """
        return COM.assert_right_panel_header('Edit ISCSI Target')

    @classmethod
    def assert_edit_panel_header_is_visible_opened_from_iscsi_tab(cls, tab_name: str) -> bool:
        """
        This method asserts that the Edit panel header is visible from the given tab.

        :param tab_name: The name of the tab.
        :return: True if the Edit panel header is visible from the given tab, otherwise it returns False.

        Example:
            - iSCSI.assert_edit_panel_header_is_visible_from_iscsi_tab('Targets')
        """
        match tab_name:
            case 'Authorized Access':
                title = f'Edit {tab_name}'
            case 'Initiators Groups':
                title = 'Add Initiator'
            case 'Targets':
                title = f'Edit ISCSI {tab_name.rstrip("s")}'
            case _:
                title = f'Edit {tab_name.rstrip("s")}'
        return COM.assert_right_panel_header(title)

    @classmethod
    def assert_sharing_iscsi_page_header(cls) -> bool:
        """
        This method asserts the header of the sharing iSCSI page.

        :return: True if the header of the sharing iSCSI page is displayed, otherwise it returns False.

        Example:
            - iSCSI.assert_sharing_iscsi_page_header()
        """
        return COM.assert_page_header('iSCSI')

    @classmethod
    def assert_iscsi_tab_header_is_visible(cls, tab_name: str) -> bool:
        """
        This method asserts that the iSCSI target tab is visible.

        :param tab_name: The name of the tab.
        :return: True if the iSCSI target tab is visible, otherwise it returns False.

        Example:
            - iSCSI.assert_iscsi_target_tab_is_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(tab_name, 3))

    @classmethod
    def assert_global_configuration_tab_is_visible(cls) -> bool:
        """
        This method asserts that the global configuration tab is visible.

        :return: True if the global configuration tab is visible, otherwise it returns False.

        Example:
            - iSCSI.assert_global_configuration_tab_is_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Global Configuration'))

    @classmethod
    def assert_iscsi_target_name_exists(cls, target_name: str) -> bool:
        """
        This method verifies that the given iSCSI target name exists.

        :param target_name: The name of the iSCSI target. Example: target1 is target-1
        :return: True if the given iSCSI target name exists, otherwise it returns False.

        Example:
            - iSCSI.assert_iscsi_target_name_exists('target-1')
        """
        return WebUI.wait_until_visible(xpaths.iscsi.iscsi_target_name(target_name))

    @classmethod
    def verify_iscsi_sharing_configuration_page_opens(cls) -> None:
        """
        This method verifies the sharing configuration page opens.

        Example:
            - iSCSI.verify_iscsi_sharing_configuration_page_opens()
        """
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('iSCSI') is True

    @classmethod
    def assert_iscsi_wizard_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method verifies that the iSCSI wizard button is locked and not clickable on the iSCSI sharing page.

        :return: True if the iSCSI wizard button is locked and not clickable otherwise it returns False.

        Example:
            - iSCSI.assert_iscsi_wizard_button_is_locked_and_not_clickable()
        """
        return COM.assert_button_is_locked_and_not_clickable('wizard')

    @classmethod
    def assert_tab_add_button_is_locked_and_not_clickable(cls, tab_name: str) -> bool:
        """
        This method asserts that the Add button in the given tab is locked and not clickable.

        :param tab_name: The name of the tab.
        :return: True if the Add button in the given tab is locked and not clickable, otherwise it returns False.

        Example:
            - iSCSI.assert_tab_add_button_is_locked_and_not_clickable('Targets')
        """
        match tab_name.lower():
            case 'associated targets' | 'authorized access':
                tab = 'target-extent'
            case 'initiators groups':
                tab = 'initiator'
            case 'portals':
                tab = 'portal'
            case 'targets' | 'extents':
                tab = 'target'
            case _:
                tab = tab_name.lower()
        return COM.assert_button_is_locked_and_not_clickable(f'add-{tab}')

    @classmethod
    def assert_tab_row_item_delete_button_is_locked_and_not_clickable(cls, tab_name: str, row_item: str) -> bool:
        """
        This method asserts that the Delete button in the given tab is locked and not clickable.

        :param tab_name: The name of the tab.
        :param row_item: The name of the item. Example: target1 is target-1
        :return: True if the Delete button in the given tab is locked and not clickable, otherwise it returns False.

        Example:
            - iSCSI.assert_tab_delete_button_is_locked_and_not_clickable('Targets', 'target-1')
        """
        match tab_name.lower():
            case 'authorized access':
                tab = tab_name.replace(' ', '-').lower()
            case 'initiators groups':
                tab = 'initiator'
            case _:
                tab = tab_name.replace(' ', '-').lower().rstrip('s')
        return COM.assert_button_is_locked_and_not_clickable(f'iscsi-{tab}-{row_item}-delete-row-action')

    @classmethod
    def click_on_the_tab_row_item_edit_button(cls, tab_name: str, row_item: str) -> None:
        """
        This method clicks on the Edit button of the given item in the given tab.

        :param tab_name: The name of the tab.
        :param item_name: The name of the item. Example: target1 is target-1

        Example:
            - iSCSI.click_on_the_item_edit_button('Targets', 'target-1')
        """
        match tab_name.lower():
            case 'authorized access':
                tab = tab_name.replace(' ', '-').lower()
            case 'initiators groups':
                tab = 'initiator'
            case _:
                tab = tab_name.replace(' ', '-').lower().rstrip('s')
        COM.click_button(f'iscsi-{tab}-{row_item}-edit-row-action')

    @classmethod
    def click_on_iscsi_tab(cls, tab_name: str) -> None:
        """
        This method clicks the given tab.

        :param tab_name: The name of the tab.

        Example:
            - iSCSI.click_on_tab('Targets')
        """
        tab = COM.convert_to_tag_format(tab_name)
        COM.click_link(tab)

    @classmethod
    def set_target_alias_input(cls, text: str) -> None:
        """
        This method sets the alias for the given iSCSI target.

        :param text: text of the given iSCSI target.

        Example:
            - iSCSI.set_target_alias_input('alias')
        """
        COM.set_input_field('alias', text)

    @classmethod
    def verify_iscsi_configuration_tabs(cls) -> None:
        """
        This method verifies the various configuration tabs are present on the sharing configuration page.

        Example:
            - iSCSI.verify_iscsi_configuration_tabs()
        """
        assert COM.is_visible(xpaths.common_xpaths.link_field('target-global-configuration')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('portals')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('initiators-groups')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('authorized-access')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('targets')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('extents')) is True
        assert COM.is_visible(xpaths.common_xpaths.link_field('associated-targets')) is True

    @classmethod
    def verify_iscsi_configuration_wizard_create_choose_block_device_ui(cls) -> None:
        """
        This method verifies the fields present on the iSCSI Configuration Wizard.

        Example:
            - iSCSI.verify_iscsi_configuration_wizard_create_choose_block_device_ui()
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('name')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('type')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('disk')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('usefor')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('target')) is True

    @classmethod
    def verify_iscsi_global_configuration_ui(cls) -> None:
        """
        This method verifies the fields if present on the Global Configuration section
        of the Target Global Configuration tab.

        Example:
            - iSCSI.verify_iscsi_global_configuration_ui()
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('basename')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('isns-servers')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('pool-avail-threshold')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('listen-port')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True
