import xpaths
from keywords.webui.common import Common as COM


class iSCSI:
    @classmethod
    def verify_iscsi_sharing_configuration_page_opens(cls) -> None:
        """
        This method verifies the sharing configuration page opens.
        """
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('iSCSI') is True

    @classmethod
    def verify_iscsi_configuration_tabs(cls) -> None:
        """
        This method verifies the various configuration tabs are present on the sharing configuration page.
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
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('name')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('type')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('disk')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('usefor')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('target')) is True

    @classmethod
    def verify_iscsi_global_configuration_ui(cls) -> None:
        """
        This method verifies the fields present on the Global Configuration section of the Target Global Configuration tab.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('basename')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('isns-servers')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('pool-avail-threshold')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('listen-port')) is True
