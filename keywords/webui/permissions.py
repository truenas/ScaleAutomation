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
        translated_level = ''
        if level == 'user' or level == 'owner':
            translated_level = 'person'
        elif level == 'group' or level == 'owner group':
            translated_level = 'people'
        elif level == 'other':
            translated_level = 'groups'
        return COM.get_element_property(f"//*[@name='{user_category}']/ancestor::ix-permissions-item/descendant::*[@class='{translated_level}']", "textContent")

    @classmethod
    def set_apply_group_checkbox(cls):
        """
        This method sets the Apply Group Checkbox.
        """
        COM.set_checkbox('apply-group')

    @classmethod
    def set_apply_user_checkbox(cls):
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
    def unset_apply_group_checkbox(cls):
        """
        This method unsets the Apply Group Checkbox.
        """
        COM.unset_checkbox('apply-group')

    @classmethod
    def unset_apply_user_checkbox(cls):
        """
        This method unsets the Apply User Checkbox.
        """
        COM.unset_checkbox('apply-user')

    @classmethod
    def verify_dataset_group(cls, name: str) -> bool:
        """
        This method returns true if the textContent of the group element matches the given name.

        :param name: The name of the group.
        :return: returns true if the textContent of the element matches the given name.
        """
        return COM.get_element_property(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Group:')]/..//*[contains(text(),'{name}')]"), 'textContent')

    @classmethod
    def verify_dataset_group_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the group permissions visible matches the given permissions.

        :param permissions: the expected permissions of the group.
        :return: returns true if the group permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('people', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_group_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the name of the group visible matches the given name.

        :param name: the name of the group.
        :return: returns true if the name of the group visible matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('people', 'name')
        return val == name

    @classmethod
    def verify_dataset_other_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the other permissions visible matches the given permissions.

        :param permissions: the expected permissions of other.
        :return: returns true if the other permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('groups', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_other_permissions_name(cls) -> bool:
        """
        This method returns true if the name other is visible for the other permissions.

        :return: returns true if the name other is visible for the other permissions.
        """
        val = cls.get_dataset_permissions_by_level('groups', 'name')
        return val == 'Other'

    @classmethod
    def verify_dataset_owner(cls, name: str) -> bool:
        """
        This method returns true if the textContent of the owner element matches the given name.

        :param name: The name of the owner.
        :return: returns true if the textContent of the element matches the given name.
        """
        return COM.get_element_property(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Owner:')]/..//*[contains(text(),'{name}')]"), 'textContent')

    @classmethod
    def verify_dataset_owner_permissions(cls, permissions: str) -> bool:
        """
        This method returns true if the owner permissions visible matches the given permissions.

        :param permissions: the expected permissions of the owner.
        :return: returns true if the owner permissions visible match the given permissions.
        """
        val = cls.get_dataset_permissions_by_level('person', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_owner_permissions_name(cls, name: str) -> bool:
        """
        This method returns true if the name of the owner visible matches the given name.

        :param name: the name of the owner.
        :return: returns true if the name of the owner visible matches the given name.
        """
        val = cls.get_dataset_permissions_by_level('person', 'name')
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

