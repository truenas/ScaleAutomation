import xpaths
from keywords.webui.common import Common as COM


class FTP:
    @classmethod
    def verify_ftp_service_basic_edit_ui(cls) -> None:
        """
        This method verifies the basic edit UI of the FTP service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('port')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('clients')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('ipconnections')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('loginattempt')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('timeout-notransfer')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('timeout')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_ftp_service_advanced_edit_ui(cls) -> None:
        """
        This method verifies the advanced edit UI of the FTP service.
        """
        cls.verify_ftp_service_basic_edit_ui()
        assert COM.is_visible(xpaths.common_xpaths.input_field('port')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('defaultroot')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('rootlogin')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('onlyanonymous')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('onlylocal')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('ident')) is True
        cls.verify_ftp_service_permission_tables_ui()
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('tls')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('passiveportsmin')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('passiveportsmax')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('fxp')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('resume')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('reversedns')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('masqaddress')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('banner')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('options')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('localuserbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('localuserdlbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('anonuserbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('anonuserdlbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_ftp_service_permission_tables_ui(cls) -> None:
        """
        This method verifies the file and directory permissions tables on the advanced FTP Edit UI.
        """
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'execute')) is True
