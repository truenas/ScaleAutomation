import xpaths
from keywords.webui.common import Common as COM


class SNMP:
    @classmethod
    def verify_snmp_service_edit_ui(cls) -> None:
        """
        This method verifies the edit UI of the SNMP service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('location')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('contact')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('community')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('v-3')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('options')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('zilstat')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('loglevel')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True
