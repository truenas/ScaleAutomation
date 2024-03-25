import xpaths
from helper.global_config import private_config, shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH


class Permissions:
    @classmethod
    def assert_edit_acl_page_header(cls) -> bool:
        """
        This method returns true if the Edit ACL page header is visible.

        :return: returns true if the Edit ACL page header is visible.
        """
        return COM.assert_page_header('Edit ACL')

    @classmethod
    def assert_edit_permissions_page_header(cls) -> bool:
        """
        This method returns true if the Edit Permissions page header is visible.

        :return: returns true if the Edit Permissions page header is visible.
        """
        return COM.assert_page_header('Edit Permissions')

    @classmethod
    def assert_dataset_group(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the name of the group. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name is visible under Owner.
        """
        WebUI.wait_until_visible(xpaths.datasets.selected_dataset_group())
        val = COM.get_element_property(xpaths.datasets.selected_dataset_group(), 'textContent')
        return val.lower().__contains__(name.lower())

    @classmethod
    def assert_dataset_owner(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the name of the Owner. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name is visible under Owner.
        """
        WebUI.wait_until_visible(xpaths.datasets.selected_dataset_owner())
        val = COM.get_element_property(xpaths.datasets.selected_dataset_owner(), 'textContent')
        return val.lower().__contains__(name.lower())

    @classmethod
    def assert_owner_input(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the value of the Owner input. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name matches the value of the Owner input.
        """
        WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('owner'), 'value')
        val = COM.get_element_property(xpaths.common_xpaths.input_field('owner'), 'value')
        return val.lower().__contains__(name.lower())

    @classmethod
    def assert_owner_group_input(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the value of the Owner Group input. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name matches the value of the Owner Group input.
        """
        WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('owner-group'), 'value')
        val = COM.get_element_property(xpaths.common_xpaths.input_field('owner-group'), 'value')
        return val.lower().__contains__(name.lower())

    @classmethod
    def assert_save_acl_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method returns true if the save access control list button is locked and not clickable.

        :return: returns true if the save access control list button is locked and not clickable.
        """
        return COM.assert_button_is_locked_and_not_clickable('save-acl')

    @classmethod
    def assert_save_as_preset_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method returns true if the save as preset button is locked and not clickable.

        :return: returns true if the save as preset button is locked and not clickable.
        """
        return COM.assert_button_is_locked_and_not_clickable('save-as-preset')

    @classmethod
    def assert_set_acl_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method returns true if the set access control list button is locked and not clickable.

        :return: returns true if the set access control list button is locked and not clickable.
        """
        return COM.assert_button_is_locked_and_not_clickable('set-acl')

    @classmethod
    def assert_strip_acl_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method returns true if the strip access control list button is locked and not clickable.

        :return: returns true if the strip access control list button is locked and not clickable.
        """
        return COM.assert_button_is_locked_and_not_clickable('strip-acl')

    @classmethod
    def click_save_acl_button(cls):
        """
        This method clicks the save access control list button.

        Example:
            - Permissions.click_save_acl_button()
        """
        COM.click_button('save-acl')
        assert COM.assert_dialog_visible('Updating ACL', shared_config['WAIT']) is True
        assert COM.assert_dialog_not_visible('Updating ACL', shared_config['LONG_WAIT']) is True

    @classmethod
    def click_set_acl_button(cls):
        """
        This method clicks the Set ACL button.

        Example:
            - Permissions.click_set_acl_button()
        """
        COM.click_button('set-acl')

    @classmethod
    def get_dataset_permissions_by_level(cls, user_category: str, level: str, index: int) -> str:
        """
        This method returns the permissions text for the given user category for the given level.

        :param user_category: the user type. EX: user/owner, group/owner group, other.
        :param level: the permissions level. EX: read, write, execute.
        :param index: the index of the element.
        :return: returns the permissions text for the given user category for the given level.
        """
        translated_category = ''
        match user_category:
            case 'user' | 'owner':
                translated_category = 'person'
            case 'group' | 'owner group':
                translated_category = 'people'
            case 'other':
                translated_category = 'groups'
        return COM.get_element_property(f"(//*[@name='{translated_category}']/ancestor::ix-permissions-item/descendant::*[@class='{level}'])[{index}]", "textContent")

    @classmethod
    def select_ace_who(cls, who: str) -> None:
        """
        This method sets the Apply Group Checkbox.

        :param who: the type to set dataset Access Control Entry who.

        Example:
        - Permissions.select_ace_who('user')
        """
        COM.select_option('tag', f'tag-{COM.convert_to_tag_format(who)}')

    @classmethod
    def select_ace_user(cls, user: str) -> None:
        """
        This method sets the access control entry user

        :param user: the name of the user.

        Example:
        - Permissions.select_ace_user('user')
        """
        COM.set_input_field('user', user, True)

    @classmethod
    def set_ace_permissions(cls, perm: str) -> None:
        """
        This method sets the Access Control Entry permissions.

        :param perm: the type to set dataset Access Control Entry permissions. [READ/MODIFY/TRAVERSE/FULL CONTROL]

        Example:
        - Permissions.set_ace_permissions('MODIFY')
        """
        COM.select_option('basic-permission', f'basic-permission-{COM.convert_to_tag_format(perm)}')

    @classmethod
    def set_apply_group_checkbox(cls) -> None:
        """
        This method sets the Apply Group Checkbox.
        """
        COM.set_checkbox('apply-group')

    @classmethod
    def set_apply_owner_checkbox(cls) -> None:
        """
        This method sets the Apply Owner Checkbox.
        """
        COM.set_checkbox('apply-owner')

    @classmethod
    def set_apply_user_checkbox(cls) -> None:
        """
        This method sets the Apply User Checkbox.
        """
        COM.set_checkbox('apply-user')

    @classmethod
    def set_dataset_group(cls, group: str) -> None:
        """
        This method sets the Unix Permissions group for the share on the Edit Permissions page

        :param group: the name of the group.
        """
        COM.is_visible(xpaths.common_xpaths.input_field('group'))
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('group'), 'value') is True
        COM.set_input_field('group', group, True)

    @classmethod
    def set_dataset_owner(cls, owner: str) -> None:
        """
        This method sets the ACL Owner for the share on the Edit ACL page

        :param owner: the name of the owner.
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner'))
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('owner'), 'value') is True
        COM.set_input_field('owner', owner, True)

    @classmethod
    def set_dataset_owner_group(cls, group: str) -> None:
        """
        This method sets the ACL group for the share on the Edit ACL page

        :param owner group: the name of the owner group.
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner-group'))
        COM.set_input_field('owner-group', group, True)

    @classmethod
    def set_dataset_user(cls, user: str) -> None:
        """
        This method sets the Unix Permissions user for the share on the Edit Permissions page

        :param user: the name of the user.
        """
        COM.is_visible(xpaths.common_xpaths.input_field('user'))
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('user'), 'value') is True
        COM.set_input_field('user', user, True)

    @classmethod
    def set_permissions_checkbox(cls, user_category: str, level: str) -> None:
        """
        This method sets the given level permission checkbox for the given user category.

        :param user_category: the user type to set the permission for. EX: user, group, other.
        :param level: the level of permission to set. EX: read, write, execute.
        """
        COM.set_checkbox(f'{user_category}-{level}')

    @classmethod
    def set_permissions_checkbox_by_level(cls, user_category: str, level: str) -> None:
        """
        This method sets the permissions for the given user category if the given level specifies it. Otherwise, it unsets that level.

        :param user_category: the user type to set the permission for. EX: user, group, other.
        :param level: the level of permission to set. EX: Read | Write | Execute or any combination.
        """
        if level.lower().__contains__("read"):
            cls.set_permissions_checkbox(user_category, "read")
        else:
            cls.unset_permissions_checkbox(user_category, "read")
        if level.lower().__contains__("write"):
            cls.set_permissions_checkbox(user_category, "write")
        else:
            cls.unset_permissions_checkbox(user_category, "write")
        if level.lower().__contains__("execute"):
            cls.set_permissions_checkbox(user_category, "execute")
        else:
            cls.unset_permissions_checkbox(user_category, "execute")

    @classmethod
    def set_group_access(cls, level: str) -> None:
        """
        This method sets the group access to the given level.

        :param level: the level of permission to set. EX: Read | Write | Execute or any combination.
        """
        cls.set_permissions_checkbox_by_level('group', level)

    @classmethod
    def set_other_access(cls, level: str) -> None:
        """
        This method sets the other access to the given level.

        :param level: the level of permission to set. EX: Read | Write | Execute or any combination.
        """
        cls.set_permissions_checkbox_by_level('other', level)

    @classmethod
    def set_user_access(cls, level: str) -> None:
        """
        This method sets the user access to the given level.

        :param level: the level of permission to set. EX: Read | Write | Execute or any combination.
        """
        cls.set_permissions_checkbox_by_level('user', level)

    @classmethod
    def unset_apply_group_checkbox(cls) -> None:
        """
        This method unsets the Apply Group Checkbox.
        """
        COM.unset_checkbox('apply-group')

    @classmethod
    def unset_apply_owner_checkbox(cls) -> None:
        """
        This method sets the Apply Owner Checkbox.
        """
        COM.unset_checkbox('apply-owner')

    @classmethod
    def unset_apply_user_checkbox(cls) -> None:
        """
        This method unsets the Apply User Checkbox.
        """
        COM.unset_checkbox('apply-user')

    @classmethod
    def unset_permissions_checkbox(cls, user_category: str, level: str) -> None:
        """
        This method unsets the given level permission checkbox for the given user category.

        :param user_category: the user type to unset the permission for. EX: user, group, other.
        :param level: the level of permission to unset. EX: read, write, execute.
        """
        COM.unset_checkbox(f'{user_category}-{level}')

    @classmethod
    def verify_dataset_builtin_admin_group_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible builtin_administrators permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :return: true if the visible builtin_administrators permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions', 1)
        return val == permissions

    @classmethod
    def verify_dataset_builtin_admin_group_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible builtin_administrators default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :return: true if the visible builtin_administrators default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions', 5)
        return val == permissions

    @classmethod
    def verify_dataset_builtin_admin_group_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the builtin_administrators matches
        Group – builtin_administrators, otherwise False.

        :return: true if the visible name of the builtin_administrators matches Group – builtin_administrators.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name', 2)
        return val == 'Group – builtin_administrators'

    @classmethod
    def verify_dataset_builtin_admin_group_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the builtin_administrators default matches
        Group – default – builtin_administrators, otherwise False.

        :return: true if the visible name of the builtin_administrators default matches Group – default – builtin_administrators.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name', 5)
        return val == 'Group – default – builtin_administrators'

    @classmethod
    def verify_dataset_group_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible group permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :return: true if the visible group permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions', 1)
        return val == permissions

    @classmethod
    def verify_dataset_group_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible group default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :return: true if the visible group default permissions matches the given permissions.
        """
        index = 2
        if COM.assert_text_is_visible('Mask'):
            index = 4
        val = cls.get_dataset_permissions_by_level('group', 'permissions', index)
        return val == permissions

    @classmethod
    def verify_dataset_group_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the group matches the given name, otherwise False.

        :param name: the name of the group.
        :return: true if the visible name of the group matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name', 1)
        return val == name

    @classmethod
    def verify_dataset_group_default_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the group default matches the given name, otherwise False.

        :param name: the name of the group.
        :return: true if the visible name of the group default matches the given name.
        """
        index = 2
        if COM.assert_text_is_visible('Mask'):
            index = 4
        val = cls.get_dataset_permissions_by_level('group', 'name', index)
        return val == name

    @classmethod
    def verify_dataset_mask_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible Mask permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Mask'.
        :return: true if the visible mask default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions', 3)
        return val == permissions

    @classmethod
    def verify_dataset_mask_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible Mask default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Mask – default'.
        :return: true if the visible mask default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions', 6)
        return val == permissions

    @classmethod
    def verify_dataset_mask_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the Mask matches the Mask, otherwise False.

        :return: true if the visible name of the Mask matches the Mask.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name', 3)
        return val == 'Mask'

    @classmethod
    def verify_dataset_mask_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the Mask matches the Mask – default, otherwise False.

        :return: true if the visible name of the Mask matches the Mask – default.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name', 6)
        return val == 'Mask – default'

    @classmethod
    def verify_dataset_other_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible other permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Other'.
        :return: true if the visible other permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('other', 'permissions', 1)
        return val == permissions

    @classmethod
    def verify_dataset_other_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible other default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Other'.
        :return: true if the visible other default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('other', 'permissions', 2)
        return val == permissions

    @classmethod
    def verify_dataset_other_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the other matches the Other, otherwise False.

        :return: true if the visible name of the other matches the Other.
        """
        val = cls.get_dataset_permissions_by_level('other', 'name', 1)
        return val == 'Other'

    @classmethod
    def verify_dataset_other_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the other default matches the Other – default, otherwise False.

        :return: true if the visible name of the other default matches the Other – default.
        """
        val = cls.get_dataset_permissions_by_level('other', 'name', 2)
        return val == 'Other – default'

    @classmethod
    def verify_dataset_owner_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible owner permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the owner.
        :return: true if the visible owner permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'permissions', 1)
        return val == permissions

    @classmethod
    def verify_dataset_owner_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible owner default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the owner.
        :return: true if the visible owner default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'permissions', 2)
        return val == permissions

    @classmethod
    def verify_dataset_owner_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the owner matches the given name, otherwise False.

        :param name: the name of the owner.
        :return: true if the visible name of the owner matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'name', 1)
        return val == name

    @classmethod
    def verify_dataset_owner_default_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the owner default matches the given name, otherwise False.

        :param name: the name of the owner.
        :return: true if the visible name of the owner default matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'name', 2)
        return val == name

    @classmethod
    def verify_dataset_permissions_edit_button(cls) -> bool:
        """
        This method returns true if the edit permissions button is visible, otherwise False.

        :return: returns true if the edit permissions button is visible.
        """
        return COM.is_visible(xpaths.common_xpaths.link_field('edit-permissions'))

    @classmethod
    def verify_dataset_permissions_type(cls, permissions_type: str) -> bool:
        """
        This method returns true if the permissions type is visible, otherwise False.

        :param permissions_type: the type of permission level for the dataset.
        :return: returns true if the permissions type is visible.
        """
        return COM.assert_text_is_visible(permissions_type)

    @classmethod
    def verify_dataset_access(cls, pool: str, dataset: str, username: str, password: str, level: str) -> None:
        """
        This method verifies the dataset access for the given username at the specified access level.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :param level: The access level to be verified (EX: "read", "write", "execute").
        """
        if level.lower().__contains__("read"):
            assert PERM_SSH.assert_dataset_read_access(pool, dataset, username, password) is True
        else:
            assert PERM_SSH.assert_dataset_read_access(pool, dataset, username, password) is False
        if level.lower().__contains__("write"):
            assert PERM_SSH.assert_dataset_write_access(pool, dataset, username, password) is True
        else:
            assert PERM_SSH.assert_dataset_write_access(pool, dataset, username, password) is False
        if level.lower().__contains__("execute"):
            assert PERM_SSH.assert_dataset_execute_access(pool, dataset, username, password) is True
        else:
            assert PERM_SSH.assert_dataset_execute_access(pool, dataset, username, password) is False
