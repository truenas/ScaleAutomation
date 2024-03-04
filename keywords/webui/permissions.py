import xpaths
from keywords.webui.common import Common as COM


class Permissions:
    @classmethod
    def get_dataset_permissions_by_level(cls, user_category: str, level: str) -> str:
        """

        :param user_category:
        :param level:
        :return:
        """
        return COM.get_element_property(f"//*[@name='{user_category}']/ancestor::ix-permissions-item/descendant::*[@class='{level}']", "textContent")

    @classmethod
    def set_dataset_owner(cls, owner: str) -> None:
        """
        This method sets the ACL Owner for the share on the Edit ACL page
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner'))
        COM.set_input_field('owner', owner, True)

    @classmethod
    def set_dataset_owner_group(cls, group: str) -> None:
        """
        This method sets the ACL group for the share on the Edit ACL page
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner-group'))
        COM.set_input_field('owner-group', group, True)

    @classmethod
    def verify_dataset_group(cls, name: str) -> bool:
        """

        :param name:
        :return:
        """
        return COM.get_element_property(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Group:')]/..//*[contains(text(),'{name}')]"), 'textContent')

    @classmethod
    def verify_dataset_group_permissions(cls, permissions: str) -> bool:
        """

        :param permissions:
        :return:
        """
        val = cls.get_dataset_permissions_by_level('people', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_group_permissions_name(cls, name: str) -> bool:
        """

        :param name:
        :return:
        """
        val = cls.get_dataset_permissions_by_level('people', 'name')
        return val == name

    @classmethod
    def verify_dataset_other_permissions(cls, permissions: str) -> bool:
        """

        :param permissions:
        :return:
        """
        val = cls.get_dataset_permissions_by_level('groups', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_other_permissions_name(cls) -> bool:
        """

        :return:
        """
        val = cls.get_dataset_permissions_by_level('groups', 'name')
        return val == 'Other'

    @classmethod
    def verify_dataset_owner(cls, name: str) -> bool:
        """

        :param name:
        :return:
        """
        return COM.get_element_property(xpaths.common_xpaths.any_xpath(f"//*[contains(text(),'Owner:')]/..//*[contains(text(),'{name}')]"), 'textContent')

    @classmethod
    def verify_dataset_owner_permissions(cls, permissions: str) -> bool:
        """

        :param permissions:
        :return:
        """
        val = cls.get_dataset_permissions_by_level('person', 'permissions')
        return val == permissions

    @classmethod
    def verify_dataset_owner_permissions_name(cls, name: str) -> bool:
        """

        :param name:
        :return:
        """
        val = cls.get_dataset_permissions_by_level('person', 'name')
        return val == name

    @classmethod
    def verify_dataset_permissions_edit_button(cls) -> bool:
        """

        :return:
        """
        return COM.is_visible(xpaths.common_xpaths.link_field('edit-permissions'))

    @classmethod
    def verify_dataset_permissions_type(cls, permtype: str) -> bool:
        """

        :param permtype:
        :return:
        """
        return COM.assert_text_is_visible(permtype)



