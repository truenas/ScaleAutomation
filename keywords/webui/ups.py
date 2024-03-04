import xpaths
from keywords.webui.common import Common as COM


class UPS:
    @classmethod
    def verify_ups_service_edit_ui(cls) -> None:
        """
        This method verifies the edit UI of the UPS service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('identifier')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('mode')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('driver')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('port')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('monuser')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('monpwd')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('extrausers')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('rmonitor')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('shutdown')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('shutdowntimer')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('shutdowncmd')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('powerdown')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('nocommwarntime')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('hostsync')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('description')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('options')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('optionsupsd')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True