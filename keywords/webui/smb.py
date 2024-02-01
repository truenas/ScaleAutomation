import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.post import API_POST


class SMB:
    @classmethod
    def add_smb_acl_entry_by_api(cls, who: str, userid: int, permission: str, perm_type: str):
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param who: is the type of user to have acl permissions: [USER/GROUP/BOTH]
        :param userid: is the id of the user/group used in the 'who' parameter as an integer
        :param permission: is the permission to be assigned: [FULL/CHANGE/READ]
        :param perm_type: is the permission type to be assigned: [ALLOWED/DENIED]
        """
        API_POST.add_smb_acl_entry(who, userid, permission, perm_type)

    @classmethod
    def assert_share_ignore_list(cls, name: str) -> bool:
        """
        This returns True if the share ignore list contains the given name otherwise it returns False.

        :param name: name to verify in the ignore list
        :return: True if the share ignore list contains the given name otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="ignore_list"]//*[contains(text(),"{name}")]'))

    @classmethod
    def assert_share_watch_list(cls, name: str) -> bool:
        """
        This returns True if the share watch list contains the given name otherwise it returns False.

        :param name: name to verify in the watch list
        :return: True if the share watch list contains the given name otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="watch_list"]//*[contains(text(),"{name}")]'))

    @classmethod
    def click_add_share_button(cls) -> None:
        """
        This method clicks the add share button on the Shares page
        """
        WebUI.xpath(xpaths.common_xpaths.button_field('smb-share-add')).click()
        assert COM.assert_right_panel_header('Add SMB')

    def click_edit_share_filesystem_acl(cls, name: str) -> None:
        """
        This method clicks the edit share filesystem acl button of the given share by the share type.

        :param name: name of the given share
        """
        WebUI.xpath(xpaths.common_xpaths.button_field(f'card-smb-share-{name.lower()}-security-row-action')).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit ACL', 1))

    @classmethod
    def delete_share_by_name(cls, sharetype: str, name: str, action: str) -> None:
        """
        This method deletes the given share on the Shares page
        """
        WebUI.xpath(xpaths.common_xpaths.button_share_action_by_name(sharetype, name, action)).click()
        COM.assert_confirm_dialog()

    @classmethod
    def set_afp(cls) -> None:
        """
        This method sets the afp checkbox.
        """
        COM.set_checkbox('afp')

    @classmethod
    def set_audit_logging_enable(cls) -> None:
        """
        This method sets the audit logging enable checkbox.
        """
        COM.set_checkbox('enable')

    @classmethod
    def set_guest_ok(cls) -> None:
        """
        This method sets the guest ok checkbox.
        """
        COM.set_checkbox('guestok')

    @classmethod
    def set_ignore_list(cls, name: str) -> None:
        """
        This method adds the given name to the ignore list.

        :param name: name of the account to ignore
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('ignore-list'))
        WebUI.xpath(xpaths.common_xpaths.input_field('ignore-list')).click()
        name = COM.convert_to_tag_format('ignore-list-'+name)
        WebUI.xpath(xpaths.common_xpaths.option_field(name)).click()

    @classmethod
    def set_share_purpose(cls, purpose: str) -> None:
        """
        This method sets the purpose for the share on the Edit Share right panel
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.select_field('purpose'))
        WebUI.xpath(xpaths.common_xpaths.select_field('purpose')).click()
        purpose = purpose.replace(' ', '-').lower()
        WebUI.xpath(xpaths.common_xpaths.option_field('purpose-' + purpose)).click()

    @classmethod
    def set_smb_acl_by_api(cls, name: str):
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param name: is the name of the smb share to have acl permissions set
        """
        API_POST.set_smb_acl(name)

    @classmethod
    def set_watch_list(cls, name: str) -> None:
        """
        This method adds the given name to the watch list.

        :param name: name of the account to watch
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('watch-list'))
        WebUI.xpath(xpaths.common_xpaths.input_field('watch-list')).click()
        name = COM.convert_to_tag_format('watch-list-'+name)
        WebUI.xpath(xpaths.common_xpaths.option_field(name)).click()

