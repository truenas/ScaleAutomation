import xpaths
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
    def verify_iscsi_sharing_configuration_page_opens(cls) -> None:
        """
        This method verifies the sharing configuration page opens.

        Example:
            - iSCSI.verify_iscsi_sharing_configuration_page_opens()
        """
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('iSCSI') is True

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
