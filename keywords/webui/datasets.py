import xpaths
from helper.api import Response
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common


class Datasets:

    @classmethod
    def assert_add_dataset_button(cls) -> bool:
        """
        This method return True or False whether the add dataset button is visible.
        :return: True if the add dataset button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_add_dataset_button()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.button_field('add-dataset'))

    @classmethod
    def assert_add_zvol_button(cls) -> bool:
        """
        This method return True or False whether the add zvol button is visible.
        :return: True if the add zvol button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_add_zvol_button()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.button_field('add-zvol'))

    @classmethod
    def assert_applied_dataset_quota_size(cls, size):
        """
        This method returns True or False whether the applied dataset quota size is visible.

        :param size: The applied dataset quota size.
        :return: True if the applied dataset quota size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_applied_dataset_quota_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Applied Dataset Quota:', size)

    @classmethod
    def assert_applied_inherited_quotas_size(cls, size):
        """
        This method returns True or False whether the applied inherited quotas size is visible.

        :param size: The applied inherited quotas size.
        :return: True if the applied inherited quotas size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_applied_inherited_quotas_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Inherited Quotas:', size)

    @classmethod
    def assert_children_size(cls, size: str) -> bool:
        """
        This method return True if the given size is set otherwise it returns False.

        :param size: is the size of the children
        :return: True if the given size is set otherwise it returns False.

        Example:
            - Dataset.assert_Children_Size('1 GiB')
        """
        return Common.assert_label_and_value_exist('Children', size)

    @classmethod
    def assert_dataset_group(cls, name: str) -> bool:
        """
        This method return True if the given dataset group is set otherwise it returns False.

        :param name: name of the given dataset group
        :return: True if the given dataset group is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_group('root')
        """
        return Common.assert_label_and_value_exist('Group:', name)

    @classmethod
    def assert_dataset_owner(cls, name: str) -> bool:
        """
        This method return True if the given dataset owner is set otherwise it returns False.

        :param name: name of the given dataset owner
        :return: True if the given dataset owner is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_owner('root')
        """
        return Common.assert_label_and_value_exist('Owner:', name)

    @classmethod
    def assert_dataset_permissions_edit_button(cls):
        """
        This method returns True or False whether the edit permissions button is visible.

        :return: True if the edit permissions button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_dataset_permissions_edit_button()
        """
        return Common.is_visible(xpaths.common_xpaths.link_field('edit-permissions'))

    @classmethod
    def assert_dataset_permission_item(cls, name: str, permissions: str) -> bool:
        """
        This method return True or False whether the given dataset permission item exists.

        :param name: name of the given dataset permission item
        :param permissions: permissions of the given dataset permission item
        :return: True if the given dataset permission item is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_permission_item('Group - admin', 'Allow | Special')
        """
        return Common.is_visible(xpaths.datasets.dataset_permissions_item(name, permissions))

    @classmethod
    def assert_dataset_posix_permissions_group_obj(cls, group_name: str) -> bool:
        """
        This method return True or False whether the given dataset posix permissions group object exists.

        :param group_name: name of the given dataset posix permissions group object
        :return: True if the given dataset posix permissions group object is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_posix_permissions_group_obj('root')
        """
        return Common.is_visible(xpaths.datasets.dataset_posix_permissions_obj('Group', group_name))

    @classmethod
    def assert_datasets_page_header(cls) -> bool:
        """
        This method return True or False whether the datasets page header is visible.

        :return: True if the datasets page header is visible otherwise it returns False.

        Example:
            - Dataset.assert_datasets_page_header()
        """
        result = Common.assert_page_header('Datasets')
        # Ensure the progress bar is hot of the way.
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.progress_bar)
        return result

    @classmethod
    def assert_dataset_roles_iscsi_icon(cls):
        """
        This method return True or False whether the given dataset displays the iscsi share connected icon

        :return: True if the given dataset displays the iscsi share connected icon otherwise it returns False.

        Example:
            - Dataset.assert_dataset_roles_iscsi_icon()
        """
        return Common.is_visible(xpaths.datasets.dataset_roles_icon('iscsi_share'))

    @classmethod
    def assert_dataset_roles_nfs_icon(cls):
        """
        This method return True or False whether the given dataset displays the nfs share connected icon

        :return: True if the given dataset displays the nfs share connected icon otherwise it returns False.

        Example:
            - Dataset.assert_dataset_roles_nfs_icon()
        """
        return Common.is_visible(xpaths.datasets.dataset_roles_icon('nfs_share'))

    @classmethod
    def assert_dataset_roles_share_icon(cls, name: str, share_type: str) -> bool:
        """
        This method return True if the given dataset is selected otherwise it returns False.

        :param name: name of the given dataset
        :param share_type: the type of share connected to the dataset
        :return: True if the given dataset displays the specified share connected icon otherwise it returns False.

        Example:
            - Dataset.assert_dataset_roles_share_icon('dataset_name', 'smb')
        """
        child = f'//ix-tree-node//*[contains(text(),"{name}")]'
        parent = 'ix-dataset-node'
        target = f'ix-icon[@name="ix:{share_type}_share"]'
        return Common.is_visible(xpaths.common_xpaths.any_child_parent_target(child, parent, target))

    @classmethod
    def assert_dataset_roles_smb_icon(cls):
        """
        This method return True or False whether the given dataset displays the smb share connected icon

        :return: True if the given dataset displays the smb share connected icon otherwise it returns False.

        Example:
            - Dataset.assert_dataset_roles_smb_icon()
        """
        return Common.is_visible(xpaths.datasets.dataset_roles_icon('smb_share'))

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
    def assert_dataset_share_attached(cls, name: str, share_type: str) -> bool:
        """
        This method return True if the given share is attached to the dataset otherwise it returns False.

        :param name: name of the given share.
        :param share_type: the type of attached share
        :return: True if the given share is attached to the dataset otherwise it returns False.

        Example:
            - Dataset.assert_dataset_share_attached('root')
        """
        print("returned xpath: "+xpaths.common_xpaths.share_attached(name, share_type))
        return Common.is_visible(xpaths.common_xpaths.share_attached(name, share_type))

    @classmethod
    def assert_dataset_tree(cls) -> bool:
        """
        This method return True or False if the dataset tree is visible.
        :return: True if the dataset tree is visible, otherwise it returns False.

        Example:
            - Dataset.assert_dataset_tree()
        """
        return Common.is_visible(xpaths.common_xpaths.any_xpath('//ix-tree-node'))

    @classmethod
    def assert_dataset_user_obj(cls, user: str) -> bool:
        """
        This method return True or False whether the given dataset user object exists.

        :param user: name of the given dataset user object
        :return: True if the given dataset user object is set otherwise it returns False.

        Example:
            - Dataset.assert_dataset_user_obj('root')
        """
        return Common.is_visible(xpaths.datasets.dataset_posix_permissions_obj('User', user))

    @classmethod
    def assert_delete_dataset_button(cls):
        """
        This method returns True or False if the delete dataset button is visible.

        :return: True if the delete dataset button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_delete_dataset_button()
        """
        return Common.is_visible(xpaths.common_xpaths.button_field('delete-dataset'))

    @classmethod
    def assert_details_card_field_value(cls, label: str, value: str) -> bool:
        """
        This method returns True or False if the given details card field value is visible.

        :param label: The name of the label
        :param value: The value of the label
        :return: True if the given details card field value is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_card_field_value('Type:', 'FILESYSTEM')
        """
        return Common.assert_label_and_value_exist(label, value)

    @classmethod
    def assert_details_case_sensitivity(cls, value):
        """
        This method returns True or False if the case sensitivity is visible.

        :param value: The case sensitivity
        :return: True if the case sensitivity is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_case_sensitivity('Sensitive')
        """
        return cls.assert_details_card_field_value("Case Sensitivity:", value)

    @classmethod
    def assert_details_compression_level(cls, value):
        """
        This method returns True or False if the compression level is visible.

        :param value: The compression level
        :return: True if the compression level is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_compression_level('lz4')
        """
        return cls.assert_details_card_field_value("Compression Level:", value)

    @classmethod
    def assert_details_enable_atime(cls, value):
        """
        This method returns True or False if the enable atime is visible.

        :param value: The enable atime
        :return: True if the enable atime is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_enable_atime('Enabled')
        """
        return cls.assert_details_card_field_value("Enable Atime:", value)

    @classmethod
    def assert_details_path(cls, value):
        """
        This method returns True or False if the path is visible.

        :param value: The path
        :return: True if the path is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_path('/root')
        """
        return cls.assert_details_card_field_value("Path:", value)

    @classmethod
    def assert_details_sync(cls, value):
        """
        This method returns True or False if the sync is visible.

        :param value: The sync
        :return: True if the sync is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_sync('Always')
        """
        return cls.assert_details_card_field_value("Sync:", value)

    @classmethod
    def assert_details_type(cls, value):
        """
        This method returns True or False if the type is visible.

        :param value: The type
        :return: True if the type is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_type('FILESYSTEM')
        """
        return cls.assert_details_card_field_value("Type:", value)

    @classmethod
    def assert_details_zfs_deduplication(cls, value):
        """
        This method returns True or False if the zfs deduplication is visible.

        :param value: The zfs deduplication
        :return: True if the zfs deduplication is visible, otherwise it returns False.

        Example:
            - Dataset.assert_details_zfs_deduplication('Enabled')
        """
        return cls.assert_details_card_field_value("ZFS Deduplication:", value)

    @classmethod
    def assert_edit_dataset_button(cls):
        """
        This method returns True or False if the edit dataset button is visible.

        :return: True if the edit dataset button is visible, otherwise it returns False.

        Example:
            - Dataset.assert_edit_dataset_button()
        """
        return Common.is_visible(xpaths.common_xpaths.button_field('edit-dataset'))

    @classmethod
    def assert_edit_dataset_panel_header(cls):
        """
        This method returns True or False if the edit dataset panel header is visible.

        :return: True if the edit dataset panel header is visible, otherwise it returns False.

        Example:
            - Dataset.assert_edit_dataset_panel_header()
        """
        return Common.assert_right_panel_header('Edit Dataset')

    @classmethod
    def assert_group_quotas(cls, text: str) -> bool:
        """
        This method returns True or False if the group quotas is visible.

        :param text: The group quotas.
        :return: True if the group quotas is visible, otherwise it returns False.

        Example:
            - Dataset.assert_group_quotas('Quotas set for')
        """
        return Common.assert_label_and_value_exist('Group Quotas:', text)

    @classmethod
    def assert_data_written_size(cls, size: str) -> bool:
        """
        This method returns True or False if the data written size is visible.

        :param size: The data written size.
        :return: True if the data written size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_data_written_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Data Written', size)

    @classmethod
    def assert_reserved_for_dataset_size(cls, size):
        """
        This method returns True or False whether the reserved for dataset size is visible.
        :param size: The reserved for dataset size.
        :return: True if the reserved for dataset size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_reserved_for_dataset_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Reserved for Dataset:', size)

    @classmethod
    def assert_reserved_for_dataset_and_children_size(cls, size):
        """
        This method returns True or False whether the reserved for dataset and children size is visible.
        :param size: The reserved for dataset and children size.
        :return: True if the reserved for dataset and children size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_reserved_for_dataset_and_children_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Reserved for Dataset & Children:', size)

    @classmethod
    def assert_search_field(cls) -> bool:
        """
        This method returns True or False whether the search field is visible.

        :return: True if the search field is visible, otherwise it returns False.

        Example:
            - Dataset.assert_search_field()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.input_field('search'))

    @classmethod
    def assert_selected_dataset_name(cls, dataset: str) -> bool:
        """
        This method returns True or False if the selected dataset name is visible.

        :param dataset: The selected dataset name.
        :return: True if the selected dataset name is visible, otherwise it returns False.

        Example:
            - Dataset.assert_selected_dataset_name('root')
        """
        return WebUI.wait_until_visible(xpaths.datasets.selected_dataset_name(dataset), shared_config['SHORT_WAIT'])

    @classmethod
    def assert_space_available_to_dataset_size(cls, size: str) -> bool:
        """
        This method returns True or False if the space available to dataset size is visible.

        :param size: The space available to dataset size.
        :return: True if the space available to dataset size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_space_available_to_dataset_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Space Available to Dataset:', size)

    @classmethod
    def assert_total_allocation_size(cls, size: str) -> bool:
        """
        This method returns True or False if the total allocation size is visible.

        :param size: The total allocation size.
        :return: True if the total allocation size is visible, otherwise it returns False.

        Example:
            - Dataset.assert_total_allocation_size('96 KiB')
        """
        return Common.assert_label_and_value_exist('Total Allocation:', size)

    @classmethod
    def assert_user_quotas(cls, text: str) -> bool:
        """
        This method returns True or False if the user quotas is visible.

        :param text: The user quotas.
        :return: True if the user quotas is visible, otherwise it returns False.

        Example:
            - Dataset.assert_user_quotas('Quotas set for')
        """
        return Common.assert_label_and_value_exist('User Quotas:', text)

    @classmethod
    def click_add_dataset_button(cls):
        """
        This method clicks on the add dataset button.

        Example:
            - Dataset.click_add_dataset_button()
        """
        Common.click_button('add-dataset')

    @classmethod
    def click_add_zvol_button(cls):
        """
        This method clicks on the add zvol button.

        Example:
            - Dataset.click_add_zvol_button()
        """
        Common.click_button('add-zvol')

    @classmethod
    def click_advanced_basic_options_button(cls):
        """
        This method clicks on the advanced basic options button.

        Example:
            - Dataset.click_advanced_basic_options_button()
        """
        Common.click_button('custom-button-advanced-options')

    @classmethod
    def click_create_snapshot_button(cls):
        """
        This method clicks on the Create Snapshot button.

        Example:
            - Dataset.click_Create_Snapshot_button()
        """
        Common.click_button('create-snapshot')

    @classmethod
    def click_dataset_location(cls, location: str):
        """
        This method clicks on the Dataset Location.

        :param location: The location of the dataset.

        Example:
            - Dataset.click_dataset_location('root')
        """
        Common.set_input_field('search', location)
        Common.click_on_element(xpaths.datasets.link_dataset(location))

    @classmethod
    def click_dataset_permission_item(cls, name: str, permissions: str):
        """
        This method clicks on the Dataset Permission Item.

        :param name: The name of the item.
        :param permissions: The permissions of the item.

        Example:
            - Dataset.click_dataset_permission_item('Group - admin', 'Allow | Special')
        """
        Common.click_on_element(xpaths.datasets.dataset_permissions_item(name, permissions))

    @classmethod
    def click_delete_dataset_button(cls):
        """
        This method clicks on the Delete Dataset button.

        Example:
            - Dataset.click_delete_dataset_button()
        """
        Common.click_button('delete-dataset')

    @classmethod
    def click_edit_dataset_button(cls):
        """
        This method clicks on the Edit Dataset button.

        Example:
            - Dataset.click_edit_dataset_button()
        """
        Common.click_button('edit-dataset')

    @classmethod
    def click_edit_dataset_space_button(cls):
        """
        This method clicks on the Edit Dataset Space button.

        Example:
            - Dataset.click_edit_dataset_space_button()
        """
        Common.click_button('edit-quotas')

    @classmethod
    def click_edit_permissions_button(cls):
        """
        This method clicks on the Edit Permissions button.

        Example:
            - Dataset.click_edit_permissions_button()
        """
        Common.click_link('edit-permissions')

    @classmethod
    def click_manage_group_quotas_link(cls):
        Common.click_link('tank-space-management-manage-group-quotas')

    @classmethod
    def click_manage_role_link(cls, name: str):
        """
        This method clicks on the Manage Role Link.

        :param name: The name of the link.

        Example:
            - Dataset.click_manage_role_link('manage-vm')
        """
        Common.click_link(name)

    @classmethod
    def click_manage_user_quotas_link(cls):
        """
        This method clicks on the Manage User Quotas Link.

        Example:
            - Dataset.click_manage_user_quotas_link()
        """
        Common.click_link('tank-space-management-manage-user-quotas')

    @classmethod
    def click_protection_manage_link(cls, link: str):
        """
        This method clicks on the Manage Link.

        :param link: The name of the link.

        Example:
            - Dataset.click_protection_manage_link('manage-snapshots')
            - Dataset.click_protection_manage_link('Manage Snapshots')
        """
        link = link.lower().replace(' ', '-')
        Common.click_link(link)
        match link:
            case "manage-snapshots":
                name = 'Snapshots:'
            case "manage-snapshot-tasks":
                name = 'Periodic Snapshot Tasks'
            case "manage-replication-tasks":
                name = 'Replication Tasks'
            case "manage-cloudsync-tasks":
                name = 'Cloud Sync Tasks'
            case "manage-rsync-tasks":
                name = 'Rsync Tasks'
            case _:
                name = ''
        return Common.assert_page_header(name)

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
    def delete_dataset(cls, pool: str, dataset: str):
        """
        This method deletes the given dataset.
        :param pool: The name of the pool.
        :param dataset: The name of the dataset.

        Example:
            - Dataset.delete_dataset('test-pool', 'test-dataset')
        """
        if WebUI.wait_until_visible(xpaths.common_xpaths.any_text(dataset), shared_config['SHORT_WAIT']):
            cls.click_dataset_location(dataset)
            Common.click_button('delete-dataset')
            Common.assert_dialog_visible(f'Delete dataset {pool}/{dataset}')
            Common.set_input_field('confirm-dataset-name', f'{pool}/{dataset}')
            Common.set_checkbox('confirm')
            Common.click_on_element(xpaths.common_xpaths.button_field_by_row('delete-dataset', 2))
            WebUI.delay(1)

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

        if Common.is_visible(xpaths.common_xpaths.button_field(name)):
            if Common.get_element_property(xpaths.common_xpaths.button_field(name), 'innerText') == value:
                WebUI.xpath(xpaths.common_xpaths.button_field(name)).click()

    @classmethod
    def get_dataset_size_usage_by_type(cls, dataset: str, usage_type: str) -> str:
        """
        This method returns the size of the given dataset.

        :param dataset: The name of the dataset.
        :param usage_type: The type of the usage.
        :return: The size of the dataset.

        Example:
            - Dataset.get_dataset_size_usage_by_type('test-dataset', 'USED')
        """
        xpath = f'//span[contains(text(),"{dataset}")]'
        to = xpaths.common_xpaths.any_child_parent_target(xpath, 'ix-dataset-node', "div/div[2]")
        size = WebUI.get_attribute(to, 'innerText')
        return size.partition('/')[0] if usage_type == "USED" else size.partition('/')[2]

    @classmethod
    def has_encryption(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has encryption.
        :param dataset: The name of the dataset.
        :return: True if the dataset has encryption is visible otherwise it returns False.

        Example:
            - Dataset.has_encryption('test-dataset')
        """
        xpath = xpaths.common_xpaths.tree_node_field(dataset)
        to = xpaths.common_xpaths.any_child_parent_target(xpath, 'ix-dataset-node', 'ix-dataset-encryption-cell')
        return WebUI.get_attribute(to, 'innerText') != 'Unencrypted'

    @classmethod
    def has_roles(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has roles.
        :param dataset: The name of the dataset.
        :return: True if the dataset has roles otherwise it returns False.

        Example:
            - Dataset.has_roles('test-dataset')
        """
        xpath = xpaths.common_xpaths.tree_node_field(dataset)
        to = xpaths.common_xpaths.any_child_parent_target(xpath, 'ix-dataset-node', 'ix-dataset-roles-cell')
        return int(WebUI.get_attribute(to, 'childElementCount')) > 0

    @classmethod
    def has_role(cls, dataset: str, role: str) -> bool:
        """
        This method checks if the given dataset has the given role.
        :param dataset: The name of the dataset.
        :param role: The name of the role.
        :return: True if the dataset role is visible otherwise it returns False.

        Example:
            - Dataset.has_role('test-dataset', 'apps')
        """
        xpath = f'//span[contains(text(),"{dataset}")]'
        target = f'ix-icon[@data-mat-icon-name="{role}"]'
        to = xpaths.common_xpaths.any_child_parent_target(xpath, 'ix-dataset-node', target)
        return WebUI.wait_until_visible(to, shared_config['SHORT_WAIT'])

    @classmethod
    def has_role_apps(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'apps'.
        :param dataset: The name of the dataset.
        :return: True if the dataset apps role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_apps('test-dataset')
        """
        return cls.has_role(dataset, "apps")

    @classmethod
    def has_role_nfs_share(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'nfs_share'.
        :param dataset: The name of the dataset.
        :return: True if the dataset nfs_share role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_nfs_share('test-dataset')
        """
        return cls.has_role(dataset, "nfs_share")

    @classmethod
    def has_role_share(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'share'.
        :param dataset: The name of the dataset.
        :return: True if the dataset share role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_share('test-dataset')
        """
        return cls.has_role(dataset, "share")

    @classmethod
    def has_role_smb_share(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'smb_share'.
        :param dataset: The name of the dataset.
        :return: True if the dataset smb_share role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_smb_share('test-dataset')
        """
        return cls.has_role(dataset, "smb_share")

    @classmethod
    def has_role_system(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'system'.
        :param dataset: The name of the dataset.
        :return: True if the dataset system role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_system('test-dataset')
        """
        return cls.has_role(dataset, "logo_truenas_scale_mark")

    @classmethod
    def has_role_virtual(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset has the role 'virtual'.

        :param dataset: The name of the dataset.
        :return: True if the dataset virtual role is visible otherwise it returns False.

        Example:
            - Dataset.has_role_virtual('test-dataset')
        """
        return cls.has_role(dataset, "computer")

    @classmethod
    def is_add_snapshot_right_panel_visible(cls) -> bool:
        """
        This method checks if the add snapshot right panel is visible.

        :return: True if the add snapshot right panel is visible otherwise it returns False.

        Example:
            - Dataset.is_add_snapshot_right_panel_visible()
        """
        return Common.assert_right_panel_header('Add Snapshot')

    @classmethod
    def is_capacity_settings_right_panel_visible(cls) -> bool:
        """
        This method checks if the capacity settings right panel is visible.

        :return: True if the capacity settings right panel is visible otherwise it returns False.

        Example:
            - Dataset.is_capacity_settings_right_panel_visible()
        """
        return Common.assert_right_panel_header('Capacity Settings')

    @classmethod
    def is_dataset_not_visible(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset is not visible.
        :param dataset: Test name of the dataset.
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - Dataset.is_dataset_not_visible('test-dataset')
        """
        Common.assert_progress_bar_not_visible()
        return WebUI.wait_until_not_visible(xpaths.datasets.link_dataset(dataset), shared_config['SHORT_WAIT']) is True

    @classmethod
    def is_dataset_visible(cls, pool: str, dataset: str) -> bool:
        """
        This method checks if the given dataset is visible and expanded.
        :param pool: The name of the pool.
        :param dataset: Test name of the dataset.
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - Dataset.is_dataset_visible('test-pool', 'test-dataset')
        """
        Common.assert_progress_bar_not_visible()
        pool += '-' if pool != '' else ''
        if WebUI.wait_until_visible(xpaths.datasets.link_dataset(dataset), shared_config['SHORT_WAIT']) is True:
            Common.assert_tree_is_expanded(pool+dataset)
        return WebUI.wait_until_visible(xpaths.datasets.link_dataset(dataset), shared_config['SHORT_WAIT']) is True

    @classmethod
    def is_data_protection_card_visible(cls) -> bool:
        """
        This method checks if the data protection card is visible.

        :return: True if the data protection card is visible, otherwise it returns False.

        Example:
            - Dataset.is_data_protection_card_visible()
        """
        return Common.is_card_visible('Data Protection')

    @classmethod
    def is_details_card_visible(cls) -> bool:
        """
        This method checks if the details card is visible.

        :return: True if the details card is visible, otherwise it returns False.

        Example:
            - Dataset.is_details_card_visible()
        """
        return Common.is_card_visible('Dataset Details')

    @classmethod
    def is_locked(cls, dataset: str) -> bool:
        """
        This method checks if the given dataset is locked.

        :param dataset: The name of the dataset.
        :return: True if the dataset is locked, otherwise it returns False.

        Example:
            - Dataset.is_locked('test-dataset')
        """
        return WebUI.get_text(xpaths.datasets.dataset_encryption_text(dataset)) == 'Locked'

    @classmethod
    def is_permissions_advanced_item_visible(cls, name: str, permission_item: str) -> bool:
        """
        This method checks if the given dataset permission item is visible.

        :param name: The name of the dataset.
        :param permission_item: The permission item text.
        :return: True if the dataset permission item is visible, otherwise it returns False.

        Example:
            - Dataset.is_permissions_advanced_item_visible('test-dataset', 'View')
        """
        return Common.is_visible(xpaths.datasets.dataset_permissions_item_advanced(name, permission_item))

    @classmethod
    def is_permissions_card_visible(cls) -> bool:
        """
        This method checks if the permissions card is visible.

        :return: True if the permissions card is visible, otherwise it returns False.

        Example:
            - Dataset.is_permissions_card_visible()
        """
        return Common.is_card_visible('Permissions')

    @classmethod
    def get_protection_task_value(cls, task: str) -> str:
        """
        This method returns the value of the given task.

        :param task: The name of the task.
        :return: The value of the task.

        Example:
            - Dataset.get_protection_task_value('smb_share')
        """
        assert cls.is_protection_task_visible(task) is True
        return WebUI.get_attribute(xpaths.datasets.dataset_protection_task(task, '/following-sibling::div'),
                                   'innerText')

    @classmethod
    def is_protection_task_visible(cls, task: str) -> bool:
        """
        This method checks if the given task is visible.

        :param task: The name of the task.
        :return: True if the task is visible, otherwise it returns False.

        Example:
            - Dataset.is_protection_task_visible('smb_share')
        """
        return Common.is_visible(xpaths.datasets.dataset_protection_task(task))

    @classmethod
    def is_roles_card_visible(cls) -> bool:
        """
        This method checks if the roles card is visible.

        :return: True if the roles card is visible, otherwise it returns False.

        Example:
            - Dataset.is_roles_card_visible()
        """
        return Common.is_card_visible('Roles')

    @classmethod
    def is_user_quotas_page_visible(cls):
        """
        This method checks if the user quotas page is visible.

        :return: True if the user quotas page is visible, otherwise it returns False.

        Example:
            - Dataset.is_user_quotas_page_visible()
        """
        return Common.assert_page_header('User Quotas')

    @classmethod
    def is_group_quotas_page_visible(cls):
        """
        This method checks if the group quotas page is visible.

        :return: True if the group quotas page is visible, otherwise it returns False.

        Example:
            - Dataset.is_group_quotas_page_visible()
        """
        return Common.assert_page_header('Group Quotas')

    @classmethod
    def is_space_management_card_visible(cls) -> bool:
        """
        This method checks if the space management card is visible.

        :return: True if the space management card is visible, otherwise it returns False.

        Example:
            - Dataset.is_space_management_card_visible()
        """
        return Common.is_card_visible('Dataset Space Management')

    @classmethod
    def lock_dataset(cls, dataset: str):
        """
        This method locks the given dataset.

        :param dataset: The name of the dataset.

        Example:
            - Dataset.lock_dataset('test-dataset')
        """
        cls.select_dataset(dataset)
        Common.click_button('lock')
        xpath = '//*[@data-test="button-cancel"]/following-sibling::button'
        Common.click_on_element(xpaths.common_xpaths.any_xpath(xpath))
        Common.assert_progress_bar_not_visible()

    @classmethod
    def select_dataset(cls, dataset_name: str) -> None:
        """
        This method selects the given dataset

        :param dataset_name: The name of the dataset to select

        Example:
            - Dataset.select_dataset('test-dataset')
        """
        WebUI.xpath(xpaths.datasets.link_dataset(dataset_name)).click()
        WebUI.delay(0.5)

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
    def set_dataset_and_child_datasets_quota_critical_alert_at(cls, percentage: str):
        """
        This method sets the quota for this dataset.

        :param percentage: The quota percentage.

        Example:
            - Dataset.set_dataset_and_child_datasets_quota_critical_alert_at('96 KiB')
        """
        Common.set_input_field('quota-critical', percentage)

    @classmethod
    def set_dataset_and_child_datasets_quota_warning_alert_at(cls, percentage: str):
        """
        This method sets the quota for this dataset.

        :param percentage: The quota percentage.

        Example:
            - Dataset.set_dataset_and_child_datasets_quota_warning_alert_at('96 KiB')
        """
        Common.set_input_field('quota-warning', percentage)

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
        Common.set_textarea_field('name', name)

    @classmethod
    def set_dataset_permissions_user_and_group_by_api(cls, dataset: str, user: str, group: str) -> Response:
        """
        This method deletes the given dataset.

        :param dataset: is the dataset name.
        :param user: is the user to set permissions.
        :param group: is the group to set permissions.
        :return: the API request response.

        Example:
            - Dataset.set_dataset_permissions_user_and_group_by_api('test-dataset', 'smb_user', 'smb_user')
        """
        return API_POST.set_dataset_permissions_user_and_group(dataset, user, group)

    @classmethod
    def set_dataset_quota_critical_alert_at(cls, percentage: str):
        """
        This method sets the quota critical alert at.

        :param percentage: The quota critical alert at.

        Example:
            - Dataset.set_dataset_quota_critical_alert_at('96 KiB')
        """
        Common.set_input_field('refquota-critical', percentage)

    @classmethod
    def set_dataset_quota_warning_alert_at(cls, percentage: str):
        """
        This method sets the quota warning alert at.

        :param percentage: The quota warning alert at.

        Example:
            - Dataset.set_dataset_quota_warning_alert_at('96 KiB')
        """
        Common.set_input_field('refquota-warning', percentage)

    @classmethod
    def set_default_dataset_and_child_datasets_quota_critical_alert_checkbox(cls):
        """
        This method sets the quota critical alert checkbox.

        Example:
            - Dataset.set_default_dataset_and_child_datasets_quota_critical_alert_checkbox()
        """
        Common.set_checkbox('quota-critical-inherit')

    @classmethod
    def set_default_dataset_and_child_datasets_quota_warning_alert_checkbox(cls):
        """
        This method sets the quota warning alert checkbox.

        Example:
            - Dataset.set_default_dataset_and_child_datasets_quota_warning_alert_checkbox()
        """
        Common.set_checkbox('quota-warning-inherit')

    @classmethod
    def set_default_dataset_quota_critical_alert_checkbox(cls):
        """
        This method sets the quota critical alert checkbox.

        Example:
            - Dataset.set_default_dataset_quota_critical_alert_checkbox()
        """
        Common.set_checkbox('refquota-critical-inherit')

    @classmethod
    def set_default_dataset_quota_warning_alert_checkbox(cls):
        """
        This method sets the quota warning alert checkbox.

        Example:
            - Dataset.set_default_dataset_quota_warning_alert_checkbox()
        """
        Common.set_checkbox('refquota-warning-inherit')

    @classmethod
    def set_quota_for_this_dataset(cls, size: str):
        """
        This method sets the quota for this dataset.

        :param size: The quota size.

        Example:
            - Dataset.set_quota_for_this_dataset('96 KiB')
        """
        Common.set_input_field('refquota', size)

    @classmethod
    def set_quota_for_this_dataset_and_all_children(cls, size: str):
        """
        This method sets the quota for this dataset and all children.

        :param size: The quota size.

        Example:
            - Dataset.set_quota_for_this_dataset_and_all_children('96 KiB')
        """
        Common.set_input_field('quota', size)

    @classmethod
    def set_reserved_space_for_this_dataset(cls, size: str):
        """
        This method sets the reserved space for this dataset.

        :param size: The reserved space size.

        Example:
            - Dataset.set_reserved_space_for_this_dataset('96 KiB')
        """
        Common.set_input_field('refreservation', size)

    @classmethod
    def set_reserved_space_for_this_dataset_and_all_children(cls, size: str):
        """
        This method sets the reserved space for this dataset and all children.

        :param size: The reserved space size.

        Example:
            - Dataset.set_reserved_space_for_this_dataset_and_all_children('96 KiB')
        """
        Common.set_input_field('reservation', size)

    @classmethod
    def unlock_dataset(cls, dataset: str, passphrase: str):
        """
        This method unlocks the given dataset.

        :param dataset: is the dataset name.
        :param passphrase: is the passphrase to unlock the dataset.

        Example:
            - Dataset.unlock_dataset('test-dataset', 'smb_user')
        """
        cls.select_dataset(dataset)
        Common.click_link('unlock')
        Common.set_input_field('passphrase', passphrase)
        Common.click_save_button()
        Common.assert_dialog_visible('Unlock Datasets')
        Common.click_button('continue')
        Common.assert_progress_bar_not_visible()
        Common.click_button('close')

    @classmethod
    def unset_default_dataset_and_child_datasets_quota_critical_alert_checkbox(cls):
        """
        This method unsets the quota critical alert checkbox.

        Example:
            - Dataset.unset_default_dataset_and_child_datasets_quota_critical_alert_checkbox()
        """
        Common.unset_checkbox('quota-critical-inherit')

    @classmethod
    def unset_default_dataset_and_child_datasets_quota_warning_alert_checkbox(cls):
        """
        This method unsets the quota warning alert checkbox.

        Example:
            - Dataset.unset_default_dataset_and_child_datasets_quota_warning_alert_checkbox()
        """
        Common.unset_checkbox('quota-warning-inherit')

    @classmethod
    def unset_default_dataset_quota_critical_alert_checkbox(cls):
        """
        This method unsets the quota critical alert checkbox.

        Example:
            - Dataset.unset_default_dataset_quota_critical_alert_checkbox()
        """
        Common.unset_checkbox('refquota-critical-inherit')

    @classmethod
    def unset_default_dataset_quota_warning_alert_checkbox(cls):
        """
        This method unsets the quota warning alert checkbox.

        Example:
            - Dataset.unset_default_dataset_quota_warning_alert_checkbox()
        """
        Common.unset_checkbox('refquota-warning-inherit')

    @classmethod
    def unset_quota_for_this_dataset(cls):
        """
        This method unsets the quota for this dataset.

        Example:
            - Dataset.unset_quota_for_this_dataset()
        """
        Common.click_on_element(xpaths.common_xpaths.input_delete_button('refquota'))

    @classmethod
    def unset_quota_for_this_dataset_and_all_children(cls):
        """
        This method unsets the quota for this dataset and all children.

        Example:
            - Dataset.unset_quota_for_this_dataset_and_all_children()
        """
        Common.click_on_element(xpaths.common_xpaths.input_delete_button('quota'))
