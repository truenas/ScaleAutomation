import xpaths
from helper.global_config import private_config, shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH
from keywords.webui.datasets import Datasets as DAT
from keywords.webui.navigation import Navigation as NAV


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
    def click_add_item_button(cls) -> None:
        """
        This method clicks the add item button on the Edit ACL page.

        Example:
            - Permissions.click_add_item_button()
        """
        COM.click_button('add-acl-item')

    @classmethod
    def click_save_acl_button(cls) -> None:
        """
        This method clicks the save access control list button.

        Example:
            - Permissions.click_save_acl_button()
        """
        COM.click_button('save-acl')
        assert COM.assert_dialog_visible('Updating ACL', shared_config['WAIT']) is True
        assert COM.assert_dialog_not_visible('Updating ACL', shared_config['LONG_WAIT']) is True
        assert COM.assert_page_header('Datasets') is True
        assert COM.assert_progress_bar_not_visible() is True

    @classmethod
    def click_set_acl_button(cls) -> None:
        """
        This method clicks the Set ACL button.

        Example:
            - Permissions.click_set_acl_button()
        """
        COM.click_button('set-acl')

    @classmethod
    def click_use_preset_button(cls) -> None:
        """
        This method clicks the Use Preset button on the Edit ACL page.

        Example:
            - Permissions.click_use_preset_button()
        """
        COM.click_button('use-preset')

    @classmethod
    def delete_custom_preset(cls, dataset: str, name: str) -> None:
        """
        This method navigates to the given dataset and uses it to delete the given custom preset.
.
        :param dataset: The name of the dataset to use.
        :param name: The name of the preset to delete.

        Example:
            - Permissions.delete_custom_preset('test-dataset', 'test-preset')
        """
        NAV.navigate_to_datasets()
        DAT.click_dataset_location(dataset)
        DAT.click_edit_permissions_button()
        COM.click_button('save-as-preset')
        if COM.is_visible(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)):
            WebUI.execute_script("arguments[0].click();", WebUI.wait_until_clickable(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)))
            # I am not sure why but this element is very flakey. Selenium's click will not work even though it's fine manually.
            # Javascript click DOES work.
            # https://ixsystems.atlassian.net/browse/NAS-128105 created on 2024-03-29
            # COM.click_on_element(xpaths.datasets.dataset_permission_custom_preset_delete_button(name))
            assert WebUI.wait_until_not_visible(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)) is True
        COM.click_cancel_button()
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.button_field('cancel')) is True

    @classmethod
    def get_dataset_permissions_item_name_by_level(cls, user_category: str, name: str) -> str:
        """
        This method returns the name text for the given user category using the given name.

        :param user_category: the user type. EX: User/Owner, Group, Other, User Obj, Group Obj, Mask.
        :param name: name of the user or group.
        :return: the name text for the given user category using the given name.
        """
        translated_category = ''
        match user_category:
            case 'user' | 'owner':
                translated_category = 'person'
            case 'group' | 'owner group':
                translated_category = 'people'
            case 'other' | 'everyone':
                translated_category = 'groups'
        return COM.get_element_property(f"//*[@name='{translated_category}']/ancestor::ix-permissions-item/descendant::*[@class='name' and contains(text(), '{name}')]", "textContent")

    @classmethod
    def get_dataset_permissions_item_permissions_by_level(cls, user_category: str, name: str) -> str:
        """
        This method returns the permissions text for the given user category for the given name.

        :param user_category: the user type. EX: User/Owner, Group, Other, User Obj, Group Obj, Mask.
        :param name: name of the user or group.
        :return: the permissions text for the given user category for the given name.
        """
        translated_category = ''
        match user_category.lower():
            case 'user' | 'owner':
                translated_category = 'person'
            case 'group' | 'owner group':
                translated_category = 'people'
            case 'other' | 'everyone':
                translated_category = 'groups'
        return COM.get_element_property(
            f"//*[@name='{translated_category}']/ancestor::ix-permissions-item/descendant::*[@class='name' and contains(text(), '{name}')]/following-sibling::*[@class='permissions']",
            "textContent")

    @classmethod
    def select_ace_who(cls, who: str) -> None:
        """
        This method sets the Apply Group Checkbox.

        :param who: the type to set dataset Access Control Entry who.

        Example:
        - Permissions.select_ace_who('user')
        """
        COM.select_option('tag', f'tag-{COM.convert_to_tag_format(who)}')
        WebUI.delay(0.5)

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
    def set_custom_preset_name(cls, name: str) -> None:
        """
        This method deletes the custom preset of the given name if it exists and sets the custom preset name input.
        """
        if COM.is_visible(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)):
            WebUI.execute_script("arguments[0].click();", WebUI.wait_until_clickable(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)))
            # I am not sure why but this element is very flakey. Selenium's click will not work even thought it's fine manually.
            # https://ixsystems.atlassian.net/browse/NAS-128105 created on 2024-03-29
            # COM.click_on_element(xpaths.datasets.dataset_permission_custom_preset_delete_button(name))
            assert WebUI.wait_until_not_visible(xpaths.datasets.dataset_permission_custom_preset_delete_button(name)) is True
        COM.set_input_field('preset-name', name)

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
        if permissions == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_permissions_by_level('group', 'Group – builtin_administrators')
            return val == permissions

    @classmethod
    def verify_dataset_builtin_admin_group_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible builtin_administrators default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :return: true if the visible builtin_administrators default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('group', 'Group – default – builtin_administrators')
        return val == permissions

    @classmethod
    def verify_dataset_builtin_admin_group_permissions_name(cls, name: str = 'Group – builtin_administrators') -> bool:
        """
        This method returns true if the visible name of the builtin_administrators matches
        Group – builtin_administrators, otherwise False.

        :return: true if the visible name of the builtin_administrators matches Group – builtin_administrators.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_name_by_level('group', 'Group – builtin_administrators')
            return val == 'Group – builtin_administrators'

    @classmethod
    def verify_dataset_builtin_admin_group_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the builtin_administrators default matches
        Group – default – builtin_administrators, otherwise False.

        :return: true if the visible name of the builtin_administrators default matches Group – default – builtin_administrators.
        """
        val = cls.get_dataset_permissions_item_name_by_level('group', 'Group – default – builtin_administrators')
        return val == 'Group – default – builtin_administrators'

    @classmethod
    def verify_dataset_everyone_permissions(cls, permissions: str, name: str) -> bool:
        """
        This method returns true if the visible everyone permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the owner.
        :param name: the name of everyone group.
        :return: true if the visible everyone permissions matches the given permissions.
        """
        if permissions == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_permissions_by_level('everyone', name)
            return val == permissions

    @classmethod
    def verify_dataset_everyone_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible everyone permissions name matches the given name, otherwise False.

        :param name: the name of everyone group.
        :return: true if the visible everyone permissions matches the given permissions.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_name_by_level('everyone', name)
            return val == name

    @classmethod
    def verify_dataset_group_permissions(cls, permissions: str, name: str) -> bool:
        """
        This method returns true if the visible group permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :param name: the name of the group.
        :return: true if the visible group permissions matches the given permissions.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_permissions_by_level('group', name)
            return val == permissions

    @classmethod
    def verify_dataset_group_default_permissions(cls, permissions: str, name: str) -> bool:
        """
        This method returns true if the visible group default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the group.
        :param name: the name of the group.
        :return: true if the visible group default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('group', name)
        return val == permissions

    @classmethod
    def verify_dataset_group_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the group matches the given name, otherwise False.

        :param name: the name of the group.
        :return: true if the visible name of the group matches the given name.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_name_by_level('group', name)
            return val == name

    @classmethod
    def verify_dataset_group_default_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the group default matches the given name, otherwise False.

        :param name: the name of the group.
        :return: true if the visible name of the group default matches the given name.
        """
        val = cls.get_dataset_permissions_item_name_by_level('group', name)
        return val == name

    @classmethod
    def verify_dataset_mask_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible Mask permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Mask'.
        :return: true if the visible mask default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('group', 'Mask')
        return val == permissions

    @classmethod
    def verify_dataset_mask_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible Mask default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Mask – default'.
        :return: true if the visible mask default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('group', 'Mask – default')
        return val == permissions

    @classmethod
    def verify_dataset_mask_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the Mask matches the Mask, otherwise False.

        :return: true if the visible name of the Mask matches the Mask.
        """
        val = cls.get_dataset_permissions_item_name_by_level('group', 'Mask')
        return val == 'Mask'

    @classmethod
    def verify_dataset_mask_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the Mask matches the Mask – default, otherwise False.

        :return: true if the visible name of the Mask matches the Mask – default.
        """
        val = cls.get_dataset_permissions_item_name_by_level('group', 'Mask – default')
        return val == 'Mask – default'

    @classmethod
    def verify_dataset_other_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible other permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Other'.
        :return: true if the visible other permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('other', 'Other')
        return val == permissions

    @classmethod
    def verify_dataset_other_default_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the visible other default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of 'Other'.
        :return: true if the visible other default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('other', 'Other – default')
        return val == permissions

    @classmethod
    def verify_dataset_other_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the other matches the Other, otherwise False.

        :return: true if the visible name of the other matches the Other.
        """
        val = cls.get_dataset_permissions_item_name_by_level('other', 'Other')
        return val == 'Other'

    @classmethod
    def verify_dataset_other_default_permissions_name(cls) -> bool:
        """
        This method returns true if the visible name of the other default matches the Other – default, otherwise False.

        :return: true if the visible name of the other default matches the Other – default.
        """
        val = cls.get_dataset_permissions_item_name_by_level('other', 'Other – default')
        return val == 'Other – default'

    @classmethod
    def verify_dataset_owner_permissions(cls, permissions: str, name: str) -> bool:
        """
        This method returns true if the visible owner permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the owner.
        :param name: the name of the owner.
        :return: true if the visible owner permissions matches the given permissions.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_permissions_by_level('owner', name)
            return val == permissions

    @classmethod
    def verify_dataset_owner_default_permissions(cls, permissions: str, name: str) -> bool:
        """
        This method returns true if the visible owner default permissions matches the given permissions, otherwise False.

        :param permissions: the expected permissions of the owner.
        :param name: the name of the owner.
        :return: true if the visible owner default permissions matches the given permissions.
        """
        val = cls.get_dataset_permissions_item_permissions_by_level('owner', name)
        return val == permissions

    @classmethod
    def verify_dataset_owner_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the owner matches the given name, otherwise False.

        :param name: the name of the owner.
        :return: true if the visible name of the owner matches the given name.
        """
        if name == 'None':
            return True
        else:
            val = cls.get_dataset_permissions_item_name_by_level('owner', name)
            return val == name

    @classmethod
    def verify_dataset_owner_default_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the visible name of the owner default matches the given name, otherwise False.

        :param name: the name of the owner.
        :return: true if the visible name of the owner default matches the given name.
        """
        val = cls.get_dataset_permissions_item_name_by_level('owner', name)
        return val == name

    @classmethod
    def verify_dataset_permissions_edit_button(cls) -> bool:
        """
        This method returns true if the edit permissions button is visible, otherwise False.

        :return: returns true if the edit permissions button is visible.
        """
        return COM.is_visible(xpaths.common_xpaths.button_field('edit-permissions'))

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


