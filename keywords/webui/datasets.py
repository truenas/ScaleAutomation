import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from helper.api import Response


class Datasets:
    @classmethod
    def assert_add_zvol_button(cls) -> bool:
        """
        This method return True or False if the add zvol button is visible.
        :return: True if the add zvol button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_add_zvol_button()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.button_field('add-zvol'))

    @classmethod
    def assert_children_size(cls, size: str) -> bool:
        """
        This method return True if the given size is set otherwise it returns False.

        :param size: is the size of the children
        :return: True if the given size is set otherwise it returns False.

        Example:
            - Dataset.assert_Children_Size('1 GiB')
        """
        return COM.assert_label_and_value_exist('Children', size)

    @classmethod
    def assert_dataset_group(cls, name: str) -> bool:
        """
        This method return True if the given dataset group is set otherwise it returns False.

        :param name: name of the given dataset group
        :return: True if the given dataset group is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_group('root')
        """
        return COM.assert_label_and_value_exist('Group:', name)

    @classmethod
    def assert_dataset_owner(cls, name: str) -> bool:
        """
        This method return True if the given dataset owner is set otherwise it returns False.

        :param name: name of the given dataset owner
        :return: True if the given dataset owner is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_owner('root')
        """
        return COM.assert_label_and_value_exist('Owner:', name)

    @classmethod
    def assert_dataset_roles_share_icon(cls, name: str, sharetype: str) -> bool:
        """
        This method return True if the given dataset is selected otherwise it returns False.

        :param sharetype: the type of share connected to the dataset
        :param name: name of the given dataset
        :return: True if the given dataset displays the specified share connected icon otherwise it returns False.

        Example:
            - Dataset.assert_dataset_roles_share_icon('dataset_name', 'smb')
        """
        child = f'//ix-tree-node//*[contains(text(),"{name}")]'
        parent = 'ix-dataset-node'
        target = f'ix-icon[@name="ix:{sharetype}_share"]'
        return COM.is_visible(xpaths.common_xpaths.any_child_parent_target(child, parent, target))

    @classmethod
    def assert_dataset_selected(cls, name: str) -> bool:
        """
        This method return True if the given dataset is selected otherwise it returns False.

        :param name: name of the given dataset.
        :return: True if the given dataset is selected otherwise it returns False.

        Example:
            - Dataset.assert_dataset_selected('root')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.selected_dataset(name))

    @classmethod
    def assert_dataset_share_attached(cls, name: str, sharetype: str) -> bool:
        """
        This method return True if the given share is attached to the dataset otherwise it returns False.

        :param sharetype: the type of attached share
        :param name: name of the given share.
        :return: True if the given share is attached to the dataset otherwise it returns False.

        Example:
            - Dataset.assert_dataset_share_attached('root')
        """
        print("returned xpath: "+xpaths.common_xpaths.share_attached(name, sharetype))
        return COM.is_visible(xpaths.common_xpaths.share_attached(name, sharetype))

    @classmethod
    def assert_dataset_tree(cls) -> bool:
        """
        This method return True or False if the dataset tree is visible.
        :return: True if the dataset tree is visible, otherwise it returns False.

        Example:
            - Dataset.assert_dataset_tree()
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath('//ix-tree-node'))

    @classmethod
    def assert_group_quotas(cls, text: str) -> bool:
        """
        This method returns True or False if the group quotas is visible.

        :param text: The group quotas.
        :return: True if the group quotas is visible, otherwise it returns False.

        Example:
            - Dataset.assert_group_quotas('Quotas set for')
        """
        return COM.assert_label_and_value_exist('Group Quotas:', text)

    @classmethod
    def assert_data_written_size(cls, size: str) -> bool:
        """
        This method returns True or False if the data written size is visible.

        :param size: The data written size.
        :return: True if the data written size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_data_written_size('96 KiB')
        """
        return COM.assert_label_and_value_exist('Data Written:', size)

    @classmethod
    def assert_search_field(cls) -> bool:
        """
        This method returns True or False if the search field is visible.

        :return: True if the search field is visible, otherwise it returns False.

        Example:
            - Dataset.assert_search_field()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.input_field('search'))

    @classmethod
    def assert_space_available_to_dataset_size(cls, size: str) -> bool:
        """
        This method returns True or False if the space available to dataset size is visible.

        :param size: The space available to dataset size.
        :return: True if the space available to dataset size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_space_available_to_dataset_size('96 KiB')
        """
        return COM.assert_label_and_value_exist('Space Available to Dataset:', size)

    @classmethod
    def assert_total_allocation_size(cls, size: str) -> bool:
        """
        This method returns True or False if the total allocation size is visible.

        :param size: The total allocation size.
        :return: True if the total allocation size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_total_allocation_size('96 KiB')
        """
        return COM.assert_label_and_value_exist('Total Allocation:', size)

    @classmethod
    def assert_user_quotas(cls, text: str) -> bool:
        """
        This method returns True or False if the user quotas is visible.

        :param text: The user quotas.
        :return: True if the user quotas is visible, otherwise it returns False.

        Example:
            - Dataset.assert_user_quotas('Quotas set for')
        """
        return COM.assert_label_and_value_exist('User Quotas:', text)

    @classmethod
    def click_add_dataset_button(cls):
        """
        This method clicks on the add dataset button.

        Example:
            - Dataset.click_add_dataset_button()
        """
        COM.click_button('add-dataset')

    @classmethod
    def click_add_zvol_button(cls):
        """
        This method clicks on the add zvol button.

        Example:
            - Dataset.click_add_zvol_button()
        """
        COM.click_button('add-zvol')

    @classmethod
    def click_advanced_basic_options_button(cls):
        """
        This method clicks on the advanced basic options button.

        Example:
            - Dataset.click_advanced_basic_options_button()
        """
        COM.click_button('custom-button-advanced-options')

    @classmethod
    def click_create_snapshot_button(cls):
        """
        This method clicks on the Create Snapshot button.

        Example:
            - Dataset.click_Create_Snapshot_button()
        """
        COM.click_button('create-snapshot')

    @classmethod
    def click_delete_dataset_button(cls):
        """
        This method clicks on the Delete Dataset button.

        Example:
            - Dataset.click_delete_dataset_button()
        """
        COM.click_button('delete-dataset')

    @classmethod
    def click_dataset_permission_item(cls, name: str, permissions: str):
        """
        This method clicks on the Dataset Permission Item.

        :param name: The name of the item.
        :param permissions: The permissions of the item.

        Example:
            - Dataset.click_dataset_permission_item('Group - admin', 'Allow | Special')
        """
        COM.click_on_element(xpaths.datasets.dataset_permissions_item(name, permissions))

    @classmethod
    def click_edit_dataset_button(cls):
        """
        This method clicks on the Edit Dataset button.

        Example:
            - Dataset.click_edit_dataset_button()
        """
        COM.click_button('edit-dataset')

    @classmethod
    def click_edit_dataset_space_button(cls):
        """
        This method clicks on the Edit Dataset Space button.

        Example:
            - Dataset.click_edit_dataset_space_button()
        """
        COM.click_button('edit-quotas')

    @classmethod
    def click_edit_permissions_button(cls):
        """
        This method clicks on the Edit Permissions button.

        Example:
            - Dataset.click_edit_permissions_button()
        """
        COM.click_link('edit-permissions')

    @classmethod
    def click_manage_role_link(cls, name: str):
        """
        This method clicks on the Manage Role Link.

        :param name: The name of the link.

        Example:
            - Dataset.click_manage_role_link('manage-vm')
        """
        COM.click_link(name)

    @classmethod
    def click_manage_user_quotas_link(cls):
        """
        This method clicks on the Manage User Quotas Link.

        Example:
            - Dataset.click_manage_user_quotas_link()
        """
        COM.click_link('manage-user-quotas')

    @classmethod
    def collapse_dataset(cls, name: str) -> None:
        """
        This method collapses the given dataset.

        :param name: name of the dataset to collapse.

        Example:
            - Dataset.collapse_dataset('test-dataset')
        """
        cls.expand_dataset_by_state(name, False)

    @classmethod
    def create_dataset_by_api(cls, name: str, share_type: str = 'GENERIC') -> Response:
        """
        This method create the given dataset.

        :param name: name of the given dataset
        :param share_type: type of the given dataset
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - Dataset.create_dataset_by_api('test-dataset')
            - Dataset.create_dataset_by_api('test-dataset', 'SMB')
        """
        return API_POST.create_dataset(name, share_type)

    @classmethod
    def create_remote_dataset_by_api(cls, name: str, share_type: str = 'GENERIC') -> Response:
        """
        This method creates the given remote dataset.

        :param name: name of the given remote dataset
        :param share_type: type of the given dataset
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - Dataset.create_remote_dataset_by_api('test-dataset')
            - Dataset.create_remote_dataset_by_api('test-dataset', 'SMB')
        """
        return API_POST.create_remote_dataset(name, share_type)

    @classmethod
    def delete_dataset_by_api(cls, name: str) -> Response:
        """
        This method deletes the given dataset.

        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - Dataset.delete_dataset_by_api('test-dataset')
        """
        return API_DELETE.delete_dataset(name)

    @classmethod
    def expand_dataset(cls, name: str) -> None:
        """
        This method expands the given dataset

        :param name: name of the dataset to expand

        Example:
            - Dataset.expand_dataset('test-dataset')
        """
        cls.expand_dataset_by_state(name, True)

    @classmethod
    def expand_dataset_by_state(cls, name: str, state: bool) -> None:
        """
        This method expands the given dataset

        :param name: name of the dataset to expand
        :param state: state to expand [True] or collapse [False]

        Example:
            - Dataset.expand_dataset_by_state('test-dataset', True)
        """
        name = "toggle-row-" + name.lower()
        value = "chevron_right"
        if state is False:
            value = "expand_more"

        if COM.is_visible(xpaths.common_xpaths.button_field(name)):
            if WebUI.xpath(xpaths.common_xpaths.button_field(name)).get_property("innerText") == value:
                WebUI.xpath(xpaths.common_xpaths.button_field(name)).click()

    @classmethod
    def select_dataset(cls, name: str) -> None:
        """
        This method selects the given dataset

        :param name: name of the dataset to select

        Example:
            - Dataset.select_dataset('test-dataset')
        """
        WebUI.xpath(xpaths.common_xpaths.any_xpath(f'//ix-tree-node//*[contains(text(),"{name}")]')).click()
        WebUI.delay(1)


    @classmethod
    def set_dataset_acl_by_api(cls, dataset: str, acltype: str, dacl: list) -> Response:
        """
        This method sets the dataset acl user and group permissions.

        :param dataset: is the user permissions.
        :param acltype: is the type of acl the dataset is. [NFS4/POSIX1E/DISABLED]
        :param dacl: is the dacl permissions.
        :return: the payload.

        Example:
            - Dataset.set_dataset_acl_by_api('test-dataset', 'NFS4', dacl_list)
        """
        payload = {
            "path": dataset,
            "dacl": dacl,
            "acltype": acltype,
            "options": {"stripacl": False}
        }
        return API_POST.set_filesystem_acl(payload)

    @classmethod
    def set_dataset_acl_user_and_group_payload(cls, user: str, group: str) -> list:
        """
        This method returns the dataset acl user and group permissions payload.

        :param user: is the user permissions.
        :param group: is the group permissions.
        :return: the payload.

        Example:
            - Dataset.set_dataset_acl_user_and_group_payload('FULL_CONTROL', 'FULL_CONTROL')
        """
        payload = [
            {
                "tag": "owner@",
                "id": -1,
                "perms": {"BASIC": user},
                "flags": {"BASIC": "INHERIT"},
                "type": "ALLOW"
            },
            {
                "tag": "group@",
                "id": -1,
                "perms": {"BASIC": group},
                "flags": {"BASIC": "INHERIT"},
                "type": "ALLOW"
            },
            {
                "tag": "GROUP",
                "id": 545,
                "perms": {"BASIC": "MODIFY"},
                "flags": {"BASIC": "INHERIT"},
                "type": "ALLOW"
            },
            {
                "tag": "GROUP",
                "id": 544,
                "perms": {"BASIC": "FULL_CONTROL"},
                "flags": {"BASIC": "INHERIT"},
                "type": "ALLOW"
            }
        ]
        return payload

    @classmethod
    def set_dataset_name(cls, name: str):
        """
        This method sets the dataset name.

        :param name: The name of the dataset.

        Example:
            - Dataset.set_dataset_name('test')
        """
        COM.set_textarea_field('name', name)

    @classmethod
    def set_dataset_permissions_user_and_group_by_api(cls, dataset: str, user: str, group: str) -> Response:
        """
        This method deletes the given dataset.

        :param dataset: is the dataset name.
        :param user: is the user to set permissions.
        :param group: is the group to set permissions.
        :return: the API request response.

        Example:
            - Dataset.set_dataset_permissions_user_and_group_by_api('test-dataset', 'smbuser', 'smbuser')
        """
        return API_POST.set_dataset_permissions_user_and_group(dataset, user, group)
