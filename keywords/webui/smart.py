import xpaths
from keywords.webui.common import Common as COM


class SMART:
    @classmethod
    def verify_smart_service_edit_ui(cls) -> None:
        """
        This method verifies the edit UI of the S.M.A.R.T. service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('interval')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('powermode')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('difference')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('informational')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('critical')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True
