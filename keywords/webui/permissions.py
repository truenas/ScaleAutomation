import xpaths
from keywords.webui.common import Common as COM


class Permissions:
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
    def set_apply_group_checkbox(cls) -> None:
        """
        This method sets the Apply Group Checkbox.
        """
        COM.set_checkbox('apply-group')

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
        COM.set_input_field('group', group, True)

    @classmethod
    def set_dataset_owner(cls, owner: str) -> None:
        """
        This method sets the ACL Owner for the share on the Edit ACL page

        :param owner: the name of the owner.
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner'))
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
        COM.set_input_field('user', user, True)

    @classmethod
    def unset_apply_group_checkbox(cls) -> None:
        """
        This method unsets the Apply Group Checkbox.
        """
        COM.unset_checkbox('apply-group')

    @classmethod
    def unset_apply_user_checkbox(cls) -> None:
        """
        This method unsets the Apply User Checkbox.
        """
        COM.unset_checkbox('apply-user')

    @classmethod
    def verify_dataset_group(cls, name: str) -> bool:
        """
        This method returns true if the given name is visible under Group.

        :param name: The name of the group.
        :return: returns true if the given name is visible under Group.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Group:')]/..//*[contains(text(),'{name}')]"))

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

        :param permissions: the expected permissions of other.
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
    def verify_dataset_owner(cls, name: str) -> bool:
        """
        This method returns true if the given name is visible under Owner.

        :param name: The name of the owner.
        :return: returns true if the given name is visible under Owner.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Owner:')]/..//*[contains(text(),'{name}')]"))

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

