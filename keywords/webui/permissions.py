import xpaths
from helper.global_config import private_config, shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.ssh.common import Common_SSH as SSH


class Permissions:

    @classmethod
    def assert_dataset_execute_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform execute actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with execute access, False otherwise.
        """
        file = f"{username}exec_file.sh"
        cr_dir = f"{username}exec_dir"
        command = f'cd /mnt/{pool}/test ; chmod 777 . ; touch {file} ;  echo -n "mkdir /mnt/{pool}/{dataset}/{cr_dir}" | cat > {file} ; chmod 777 {file}'
        SSH.get_output_from_ssh(command, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        command2 = f"cd /mnt/{pool}/test ; ./{file}"
        SSH.get_output_from_ssh(command2, private_config['IP'], username, password)
        command3 = f"cd /mnt/{pool} ; sudo ls -al {dataset}"
        value = SSH.get_output_from_ssh(command3, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        return cr_dir in value.stdout.lower()

    @classmethod
    def assert_dataset_read_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform read actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with read access, False otherwise.
        """
        command = f"cd /mnt/{pool}/{dataset} ; ls -al"
        value = SSH.get_output_from_ssh(command, private_config['IP'], username, password)
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        return True

    @classmethod
    def assert_dataset_write_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform write actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with write access, False otherwise.
        """
        file = f"{username}file.txt"
        command = f"cd /mnt/{pool} ; touch {dataset}/{file}"
        SSH.get_output_from_ssh(command, private_config['IP'], username, password)
        command2 = f"cd /mnt/{pool} ; sudo ls -al {dataset}"
        value = SSH.get_output_from_ssh(command2, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        return file in value.stdout.lower()

    @classmethod
    def assert_edit_acl_page_header(cls) -> bool:
        """
        This method returns true if the ACLs page header is visible.

        :return: returns true if the ACLs page header is visible.
        """
        return COM.assert_page_header('Edit ACL')

    @classmethod
    def assert_edit_permissions_page_header(cls) -> bool:
        """
        This method returns true if the Permissions page header is visible.

        :return: returns true if the Permissions page header is visible.
        """
        return COM.assert_page_header('Edit Permissions')

    @classmethod
    def assert_dataset_group(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the name of the group. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name is visible under Owner.
        """
        val = COM.get_element_property(xpaths.datasets.selected_dataset_group(), 'textContent')
        return val.lower().__contains__(name.lower())

    @classmethod
    def assert_dataset_owner(cls, name: str) -> bool:
        """
        This method returns true if the given name matches the name of the Owner. Otherwise, it returns false.

        :param name: The name of the owner.
        :return: returns true if the given name is visible under Owner.
        """
        val = COM.get_element_property(xpaths.datasets.selected_dataset_owner(), 'textContent')
        return val.lower().__contains__(name.lower())

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
    def get_dataset_permissions_by_level(cls, user_category: str, level: str) -> str:
        """
        This method returns the permissions text for the given user category for the given level.

        :param user_category: the user type. EX: user/owner, group/owner group, other.
        :param level: the permissions level. EX: read, write, execute.
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
        return COM.get_element_property(f"//*[@name='{translated_category}']/ancestor::ix-permissions-item/descendant::*[@class='{level}']", "textContent")

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
    def verify_dataset_group_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the group permissions visible matches the given permissions.

        :param permissions: the expected permissions of the group.
        :return: returns true if the group permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('group', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_group_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the name of the group visible matches the given name.

        :param name: the name of the group.
        :return: returns true if the name of the group visible matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('group', 'name')
        return val == name

    @classmethod
    def verify_dataset_other_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the other permissions visible matches the given permissions.

        :param permissions: the expected permissions of 'other'.
        :return: returns true if the other permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('other', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_other_permissions_name(cls) -> bool:
        """
        This method returns true if the name other is visible for the other permissions.

        :return: returns true if the name other is visible for the other permissions.
        """
        val = cls.get_dataset_permissions_by_level('other', 'name')
        return val == 'Other'

    @classmethod
    def verify_dataset_owner_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the owner permissions visible matches the given permissions.

        :param permissions: the expected permissions of the owner.
        :return: returns true if the owner permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_owner_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the name of the owner visible matches the given name.

        :param name: the name of the owner.
        :return: returns true if the name of the owner visible matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('owner', 'name')
        return val == name

    @classmethod
    def verify_dataset_permissions_edit_button(cls) -> bool:
        """
        This method returns true if the edit permissions button is visible.

        :return: returns true if the edit permissions button is visible.
        """
        return COM.is_visible(xpaths.common_xpaths.link_field('edit-permissions'))

    @classmethod
    def verify_dataset_permissions_type(cls, permissions_type: str) -> bool:
        """
        This method returns true if the permissions type is visible.

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
            assert cls.assert_dataset_read_access(pool, dataset, username, password) is True
        else:
            assert cls.assert_dataset_read_access(pool, dataset, username, password) is False
        if level.lower().__contains__("write"):
            assert cls.assert_dataset_write_access(pool, dataset, username, password) is True
        else:
            assert cls.assert_dataset_write_access(pool, dataset, username, password) is False
        if level.lower().__contains__("execute"):
            assert cls.assert_dataset_execute_access(pool, dataset, username, password) is True
        else:
            assert cls.assert_dataset_execute_access(pool, dataset, username, password) is False
