import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class Local_Groups:

    @classmethod
    def add_group_allowed_sudo_command(cls, command: str) -> None:
        COM.set_input_field('sudo-commands', command, True, True)
        assert COM.is_visible(xpaths.common_xpaths.any_pill("sudo-commands", command))

    @classmethod
    def add_group_allowed_sudo_command_no_password(cls, command: str) -> None:
        COM.set_input_field('sudo-commands-nopasswd', command, True, True)
        assert COM.is_visible(xpaths.common_xpaths.any_pill("sudo-commands-nopasswd", command))

    @classmethod
    def assert_add_local_group_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add local group button is locked and not clickable

        :return: True if the add local group button is locked and not clickable, otherwise it returns False.

        Example:
            - Local_Groups.assert_add_local_group_button_is_restricted()
        """
        return COM.assert_button_is_restricted('add-group')

    @classmethod
    def assert_delete_local_group_button_is_restricted(cls, name: str) -> bool:
        """
        This method returns True if the add local group button is locked and not clickable.

        :param name: is the name of the group to be deleted
        :return: True if the add local group button is locked and not clickable, otherwise it returns False.

        Example:
            - Local_Groups.assert_delete_local_group_button_is_restricted()
        """
        name = COM.convert_to_tag_format(name)
        return COM.assert_button_is_restricted(f'{name}-delete')

    @classmethod
    def assert_gid_field_is_disabled(cls) -> bool:
        """
        This method returns True if the gid text field is disabled, otherwise False

        :return: returns True if the gid text field is disabled, otherwise False

        Example
         - Local_Groups.assert_gid_field_is_disabled()
        """
        return COM.get_input_property('gid', 'disabled')

    @classmethod
    def assert_group_allow_all_sudo_commands(cls) -> bool:
        """
        This method returns True if the allow all sudo commands checkbox is set, otherwise False

        :return: returns True if the allow all sudo commands checkbox is set, otherwise False

        Example
         - Local_Groups.assert_group_allow_all_sudo_commands()
        """
        return COM.is_checked('sudo-commands-all')

    @classmethod
    def assert_group_allow_all_sudo_commands_no_password(cls) -> bool:
        """
        This method returns True if the allow all sudo commands no password checkbox is set, otherwise False

        :return: returns True if the allow all sudo commands no password checkbox is set, otherwise False

        Example
         - Local_Groups.assert_group_allow_all_sudo_commands_no_password()
        """
        return COM.is_checked('sudo-commands-nopasswd-all')

    @classmethod
    def assert_group_allowed_sudo_commands(cls, command: str) -> bool:
        """
        This method returns True if the given command is set for the group, otherwise False

        :param command: is the command of the group
        :return: returns True if the given command is set for the group, otherwise False

        Example
         - Local_Groups.assert_group_allowed_sudo_commands('/usr/sbin/zfs')
        """
        return WebUI.xpath(f'//*[@formcontrolname="sudo_commands"]//*[contains(text(),"{command}")]').text == command

    @classmethod
    def assert_group_allowed_sudo_commands_is_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands text field is disabled, otherwise False

        :return: returns True if the allow sudo commands text field is disabled, otherwise False

        Example
         - Local_Groups.assert_group_allowed_sudo_commands_is_disabled()
        """
        return COM.get_input_property('sudo-commands', 'disabled')

    @classmethod
    def assert_group_allowed_sudo_commands_no_password(cls, command: str) -> bool:
        """
        This method returns True if the given command is set for the group, otherwise False

        :param command: is the command of the group
        :return: returns True if the given command is set for the group, otherwise False

        Example
         - Local_Groups.assert_group_allowed_sudo_commands_no_password('/usr/bin')
        """
        return WebUI.xpath(f'//*[@formcontrolname="sudo_commands_nopasswd"]//*[contains(text(),"{command}")]').text == command

    @classmethod
    def assert_group_allowed_sudo_commands_no_password_is_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands no password text field is disabled, otherwise False

        :return: returns True if the allow sudo commands no password text field is disabled, otherwise False

        Example
         - Local_Groups.assert_group_allowed_sudo_commands_no_password_is_disabled()
        """
        return COM.get_input_property('sudo-commands-nopasswd', 'disabled')

    @classmethod
    def assert_group_gid(cls, group_name: str, gid: str) -> bool:
        """
        This method returns True if the given gid is set for the given group, otherwise False

        :param group_name: is the name of the group
        :param gid: is the gid of the group
        :return: returns True if the given gid is set for the given group, otherwise False

        Example
         - Local_Groups.assert_group_gid('group-name', '3000')
        """
        group_name = COM.convert_to_tag_format(group_name)
        return WebUI.get_attribute(xpaths.local_groups.gid(group_name), 'innerText') == gid

    @classmethod
    def assert_sudo_commands_is_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands checkbox is disabled, otherwise False

        :return: returns True if the allow sudo commands checkbox is disabled, otherwise False

        Example
         - Local_Groups.assert_sudo_commands_is_disabled()
        """
        return COM.get_input_property('sudo-commands', 'disabled') is True

    @classmethod
    def assert_sudo_commands_no_password_is_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands no password checkbox is disabled, otherwise False

        :return: returns True if the allow sudo commands no password checkbox is disabled, otherwise False

        Example
         - Local_Groups.assert_sudo_commands_no_password_is_disabled()
        """
        return COM.get_input_property('sudo-commands-nopasswd', 'disabled') is True

    @classmethod
    def click_add_group_button(cls) -> None:
        """
        This method clicks the add group button

        Example
         - Local_Groups.click_add_group_button()
        """
        COM.click_button('add-group')

    @classmethod
    def click_add_to_list_button(cls) -> None:
        """
        This method clicks the Add To List button.

        Example
         - Local_Groups.click_add_to_list_button()
        """
        COM.click_button('add-to-list')

    @classmethod
    def click_group_action_button(cls, group_name: str, action: str) -> None:
        """
        This method clicks the given group action button of the given group

        :param group_name: is the name of the group
        :param action: is the action of the button ['members'/'edit'/'delete']

        Example
         - Local_Groups.click_group_action_button('group-name', 'delete')
         - Local_Groups.click_group_action_button('group-name', 'edit')
         - Local_Groups.click_group_action_button('group-name', 'members')
        """
        group_name = COM.convert_to_tag_format(group_name + '-' + action)
        assert COM.is_visible(xpaths.common_xpaths.button_field(group_name))
        COM.click_button(group_name)

    @classmethod
    def click_group_delete_button_by_name(cls, group_name: str) -> None:
        """
        This method clicks the given group name edit button

        :param group_name: is the name of the group

        Example
         - Local_Groups.click_group_edit_button_by_name('group-name')
        """
        cls.click_group_action_button(group_name, 'delete')

    @classmethod
    def click_group_edit_button_by_name(cls, group_name: str) -> None:
        """
        This method clicks the given group name edit button

        :param group_name: is the name of the group

        Example
         - Local_Groups.click_group_edit_button_by_name('group-name')
        """
        cls.click_group_action_button(group_name, 'edit')

    @classmethod
    def click_group_members_button(cls, group_name: str) -> None:
        """
        This method clicks the given group name members button

        :param group_name: is the name of the group

        Example
         - Local_Groups.click_group_members_button('group-name')
        """
        cls.click_group_action_button(group_name, 'members')

    @classmethod
    def click_group_members_by_name(cls, username: str) -> None:
        """
        This method clicks the given username

        :param username: is the name of the user

        Example
         - Local_Groups.click_user_account_by_name('username')
        """
        COM.click_on_element(xpaths.local_groups.members_group_member(username))

    @classmethod
    def click_remove_from_list_button(cls) -> None:
        """
        This method clicks the Remove From List button.

        Example
         - Local_Groups.click_remove_from_list_button()
        """
        COM.click_button('remove-from-list')

    @classmethod
    def click_user_account_by_name(cls, username: str) -> None:
        """
        This method clicks the given username

        :param username: is the name of the user

        Example
         - Local_Groups.click_user_account_by_name('username')
        """
        COM.click_on_element(xpaths.local_groups.members_user(username))

    @classmethod
    def create_group_by_api(cls, group_name: str, smb_access: bool = False) -> None:
        """
        This method creates the given group by API call

        :param group_name: is the name of the group to delete
        :param smb_access: allow smb access for the group.

        Example
         - Local_Users.create_group_by_api('group name')
         - Local_Users.create_group_by_api('group name', True)
        """
        API_POST.create_group(group_name, smb_access)

    @classmethod
    def delete_all_group_allowed_sudo_commands(cls):
        """
        This method deletes all sudo command commands.

        Example
         - Local_Groups.delete_all_group_allowed_sudo_commands()
        """
        while COM.is_visible(xpaths.common_xpaths.any_pill_delete("sudo-commands", '/')):
            command = COM.get_element_property(xpaths.common_xpaths.any_pill("sudo-commands", '/'), 'innerText')
            cls.delete_group_allowed_sudo_command(command)

    @classmethod
    def delete_all_group_allowed_sudo_commands_no_password(cls):
        """
        This method deletes all sudo command no password commands.

        Example
         - Local_Groups.delete_all_group_allowed_sudo_commands_no_password()
        """
        while COM.is_visible(xpaths.common_xpaths.any_pill_delete("sudo-commands-nopasswd", '/')):
            command = COM.get_element_property(xpaths.common_xpaths.any_pill("sudo-commands-nopasswd", '/'), 'innerText')
            cls.delete_group_allowed_sudo_command_no_password(command)

    @classmethod
    def delete_group_allowed_sudo_command(cls, command: str) -> None:
        """
        This method deletes the given group allow sudo command command

        :param command: The command of the pill to delete.

        Example
         - Local_Users.delete_group_allowed_sudo_command('/usr/sbin/zfs')
        """
        if COM.is_visible(xpaths.common_xpaths.any_pill_delete('sudo-commands', command)):
            COM.click_on_element(xpaths.common_xpaths.any_pill_delete('sudo-commands', command))
        assert not COM.is_visible(xpaths.common_xpaths.any_pill('sudo-commands', command))

    @classmethod
    def delete_group_allowed_sudo_command_no_password(cls, command: str) -> None:
        """
        This method deletes the given group allow sudo command no password command

        :param command: The command of the pill to delete.

        Example
         - Local_Users.delete_group_allowed_sudo_command_no_password('/usr/sbin/zfs')
        """
        if COM.is_visible(xpaths.common_xpaths.any_pill_delete('sudo-commands-nopasswd', command)):
            COM.click_on_element(xpaths.common_xpaths.any_pill_delete('sudo-commands-nopasswd', command))
        assert not COM.is_visible(xpaths.common_xpaths.any_pill('sudo-commands-nopasswd', command))

    @classmethod
    def delete_group_by_api(cls, name: str, privilege: str = None) -> None:
        """
        This method deletes the given group by API call

        :param name: is the name of the group to delete
        :param privilege: is privilege of the group.

        Example
         - Local_Users.delete_group_by_api('group name')
         - Local_Users.delete_group_by_api('group name', 'Read-Only Administrator')
        """
        API_DELETE.delete_group(name, privilege)

    @classmethod
    def delete_group_by_name(cls, group_name: str, state: bool = False) -> None:
        """
        This method deletes the given group

        :param group_name: is the name of the group to be deleted
        :param state: whether to delete primary group as well [True/False]

        Example
         - Local_Groups.delete_group_by_name('Group Name')
         - Local_Groups.delete_group_by_name('Group Name', True)
        """
        cls.expand_group_by_name(group_name)
        cls.click_group_delete_button_by_name(COM.convert_to_tag_format(group_name))
        if state:
            COM.set_checkbox('delete-primary-group')
        COM.click_button('delete')
        COM.assert_page_header('delete group', shared_config['SHORT_WAIT'])

    @classmethod
    def expand_group_by_name(cls, group_name: str) -> None:
        """
        This method expands the gid group

        :param group_name: is the name of the group

        Example
         - Local_Groups.expand_group_by_name('group_name')
        """
        group_name = COM.convert_to_tag_format(group_name)
        if COM.is_visible(xpaths.common_xpaths.button_field(f"{group_name}-edit")) is False:
            COM.click_on_element(f'//*[@data-test="row-group-{group_name}"]')

    @classmethod
    def get_group_list_allow_sudo_commands(cls, group) -> str:
        """
        This method returns the group allow sudo commands from the given group

        :param group: is the name of the group
        :return: returns the group allow sudo commands from the given group

        Example
         - Local_Groups.get_group_list_builtin('group name')
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        index = True if group == "_ssh" else False
        return cls.get_group_list_attribute(xpaths.local_groups.allow_sudo_commands(COM.convert_to_tag_format(group)), index)

    @classmethod
    def get_group_list_attribute(cls, path: str, index: bool = False) -> str:
        """
        This method returns the group list attribute from the given path

        :param path: is the path of the group attribute
        :param index: True if group name is '_ssh'
        :return: returns the group list attribute from the given path

        Example
         - Local_Groups.get_group_list_attribute('xpath')
         - Local_Groups.get_group_list_attribute('xpath', True)
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        if index:
            path = f'({path})[2]'
        return COM.get_element_property(path, 'textContent').strip()

    @classmethod
    def get_group_list_builtin(cls, group) -> str:
        """
        This method returns the group builtin from the given group

        :param group: is the name of the group
        :return: returns the group builtin from the given group

        Example
         - Local_Groups.get_group_list_builtin('group name')
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        index = True if group == "_ssh" else False
        return cls.get_group_list_attribute(xpaths.local_groups.builtin(COM.convert_to_tag_format(group)), index)

    @classmethod
    def get_group_list_gid(cls, group) -> str:
        """
        This method returns the group gid from the given group

        :param group: is the name of the group
        :return: returns the group gid from the given group

        Example
         - Local_Groups.get_group_list_gid('group name')
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        index = True if group == "_ssh" else False
        return cls.get_group_list_attribute(xpaths.local_groups.gid(COM.convert_to_tag_format(group)), index)

    @classmethod
    def get_group_list_roles(cls, group) -> str:
        """
        This method returns the group roles from the given group

        :param group: is the name of the group
        :return: returns the group roles from the given group

        Example
         - Local_Groups.get_group_list_roles('group name')
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        index = True if group == "_ssh" else False
        return cls.get_group_list_attribute(xpaths.local_groups.roles(COM.convert_to_tag_format(group)), index)

    @classmethod
    def get_group_list_samba_auth(cls, group) -> str:
        """
        This method returns the group samba authentication from the given group

        :param group: is the name of the group
        :return: returns the group samba authentication from the given group

        Example
         - Local_Groups.get_group_list_samba_auth('group name')
        """
        # TODO: Fix/Remove this if '_ssh' group is removed or changed
        index = True if group == "_ssh" else False
        return cls.get_group_list_attribute(xpaths.local_groups.samba_auth(COM.convert_to_tag_format(group)), index)

    @classmethod
    def is_group_visible(cls, group_name: str) -> bool:
        """
        This method returns True if the given group displays, otherwise False

        :param group_name: is the name of the group
        :return: returns True if the given group displays, otherwise False

        Example
         - Local_Groups.is_group_visible('group-name')
        """
        name = COM.convert_to_tag_format(group_name)
        if not COM.is_visible(xpaths.local_groups.group(name)):
            NAV.navigate_to_dashboard()
            NAV.navigate_to_local_groups()
        if not COM.assert_page_header('Groups'):
            NAV.navigate_to_local_groups()
        return WebUI.wait_until_visible(xpaths.local_groups.group(name))

    @classmethod
    def is_user_in_group_list(cls, username: str) -> bool:
        """
        This method returns True if the given username is in the group member list, otherwise False

        :param username: is the name of the user
        :return: returns True if the given username is in the group member list, otherwise False

        Example
         - Local_Groups.is_user_in_group_list('username')
        """
        return COM.is_visible(xpaths.local_groups.members_group_member(username))

    @classmethod
    def is_user_in_users_list(cls, username: str) -> bool:
        """
        This method returns True if the given username is in the users list, otherwise False

        :param username: is the name of the user
        :return: returns True if the given username is in the users list, otherwise False

        Example
         - Local_Groups.is_user_in_users_list('username')
        """
        return COM.is_visible(xpaths.local_groups.members_user(username))

    @classmethod
    def select_group_privileges(cls, privilege: str) -> None:
        """
        This method selects the given privilege.

        :param privilege: The name of the privilege to select.

        Example:
            - Local_Groups.select_group_privileges('Read-Only Administrator')
        """
        COM.click_on_element(f'//*[@data-test="input-privileges"]')
        COM.click_on_element(f'//mat-option[contains(.,"{privilege}")]')

    @classmethod
    def set_allow_duplicate_gids(cls) -> None:
        """
        This method sets the allow duplicat gids checkbox

        Example
         - Local_Groups.set_allow_duplicate_gids()
        """
        COM.set_checkbox('allow-duplicate-gid')

    @classmethod
    def set_group_allow_all_sudo_commands_checkbox(cls) -> None:
        """
        This method sets the allow all sudo commands checkbox

        Example
         - Local_Groups.set_group_allow_all_sudo_commands_checkbox()
        """
        COM.set_checkbox('sudo-commands-all')

    @classmethod
    def set_group_allow_all_sudo_commands_no_password_checkbox(cls) -> None:
        """
        This method sets the allow all sudo commands no password checkbox

        Example
         - Local_Groups.set_group_allow_all_sudo_commands_no_password_checkbox()
        """
        COM.set_checkbox('sudo-commands-nopasswd-all')

    @classmethod
    def set_group_allowed_sudo_commands(cls, command: str) -> None:
        """
        This method adds the given sudo command for the group

        :param command: is the sudo command to be added

        Example
         - Local_Groups.set_group_allowed_sudo_commands('/usr/sbin/zfs')
        """
        COM.set_input_field('sudo-commands', command)

    @classmethod
    def set_group_allowed_sudo_commands_no_password(cls, command: str) -> None:
        """
        This method adds the given sudo command no password for the group

        :param command: is the sudo command no password to be added

        Example
         - Local_Groups.set_group_allowed_sudo_commands_no_password('/usr/bin')
        """
        COM.set_input_field('sudo-commands-nopasswd', command)

    @classmethod
    def set_group_gid(cls, gid: str) -> None:
        """
        This method sets the given group id(gid) for the group

        :param gid: is the group id to be added

        Example
         - Local_Groups.set_group_gid('3005')
        """
        COM.set_input_field('gid', gid, True)
        assert WebUI.get_attribute(xpaths.common_xpaths.input_field('gid'), 'value') == gid

    @classmethod
    def set_group_name(cls, group_name: str) -> None:
        """
        This method sets the given group name for the group

        :param group_name: is the group id to be added

        Example
         - Local_Groups.set_group_name('Group Name')
        """
        COM.set_input_field('name', group_name, True)
        assert WebUI.get_attribute(xpaths.common_xpaths.input_field('name'), 'value') == group_name

    @classmethod
    def set_samba_authentication(cls) -> None:
        """
        This method sets the samba authentication checkbox

        Example
         - Local_Groups.set_samba_authentication()
        """
        COM.set_checkbox('smb')

    @classmethod
    def set_show_builtin_groups_toggle(cls) -> None:
        """
        This method sets the show built-in groups toggle

        Example
         - Local_Groups.set_show_builtin_groups_toggle()
        """
        COM.set_toggle('show-built-in-groups')

    @classmethod
    def unset_group_allow_all_sudo_commands_checkbox(cls) -> None:
        """
        This method unsets the group allow all sudo commands checkbox

        Example
         - Local_Groups.unset_group_allow_all_sudo_commands_checkbox()
        """
        COM.unset_checkbox('sudo-commands-all')

    @classmethod
    def unset_group_allow_all_sudo_commands_no_password_checkbox(cls) -> None:
        """
        This method unsets the group allow all sudo commands no password checkbox

        Example
         - Local_Groups.unset_group_allow_all_sudo_commands_no_password_checkbox()
        """
        COM.unset_checkbox('sudo-commands-nopasswd-all')

    @classmethod
    def unset_samba_authentication(cls) -> None:
        """
        This method unsets the samba authentication checkbox

        Example
         - Local_Groups.unset_samba_authentication()
        """
        COM.unset_checkbox('smb')

    @classmethod
    def unset_show_builtin_groups_toggle(cls) -> None:
        """
        This method unsets the show built-in groups toggle

        Example
         - Local_Groups.unset_show_builtin_groups_toggle()
        """
        COM.unset_toggle('show-built-in-groups')
