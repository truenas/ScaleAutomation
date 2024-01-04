import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from helper.api import Response


class Datasets:
    @classmethod
    def assert_dataset_group(cls, name: str) -> bool:
        """
        This method return True if the given dataset group is set otherwise it returns False.

        :param name: name of the given dataset group
        :return: True if the given dataset group is set otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@class="label" and contains(text(),"Group:")]/following-sibling::*[contains(text(),"{name}")]'))

    @classmethod
    def assert_dataset_owner(cls, name: str) -> bool:
        """
        This method return True if the given dataset owner is set otherwise it returns False.

        :param name: name of the given dataset owner
        :return: True if the given dataset owner is set otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@class="label" and contains(text(),"Owner:")]/following-sibling::*[contains(text(),"{name}")]'))

    @classmethod
    def assert_dataset_roles_smb_icon(cls, name: str) -> bool:
        """
        This method return True if the given dataset is selected otherwise it returns False.

        :param name: name of the given dataset
        :return: True if the given dataset is selected otherwise it returns False.
        """
        child = f'//ix-tree-node//*[contains(text(),"{name}")]'
        parent = 'ix-dataset-node'
        target = "ix-icon[@name='ix:smb_share']"
        return COM.is_visible(xpaths.common_xpaths.any_child_parent_target(child, parent, target))

    @classmethod
    def assert_dataset_selected(cls, name: str) -> bool:
        """
        This method return True if the given dataset is selected otherwise it returns False.

        :param name: name of the given dataset
        :return: True if the given dataset is selected otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.selected_dataset(name))

    @classmethod
    def assert_dataset_share_attached(cls, name: str) -> bool:
        """
        This method return True if the given share is attached to the dataset otherwise it returns False.

        :param name: name of the given share
        :return: True if the given share is attached to the dataset otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attached(name))

    @classmethod
    def collapse_dataset(cls, name: str) -> None:
        """
        This method collapses the given dataset

        :param name: name of the dataset to collapse
        """
        cls.expand_dataset_by_state(name, False)

    @classmethod
    def create_dataset_by_api(cls, name: str, sharetype: str = 'GENERIC') -> Response:
        """
        This method deletes the given dataset.

        :param name: name of the given dataset
        :param sharetype: type of the given dataset
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_POST.create_dataset(name, sharetype)

    @classmethod
    def delete_dataset_by_api(cls, name: str) -> Response:
        """
        This method deletes the given dataset.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_DELETE.delete_dataset(name)

    @classmethod
    def expand_dataset(cls, name: str) -> None:
        """
        This method expands the given dataset

        :param name: name of the dataset to expand
        """
        cls.expand_dataset_by_state(name, True)

    @classmethod
    def expand_dataset_by_state(cls, name: str, state: bool) -> None:
        """
        This method expands the given dataset

        :param name: name of the dataset to expand
        :param state: state to expand [True] or collapse [False]
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
        """
        WebUI.xpath(xpaths.common_xpaths.any_xpath(f'//ix-tree-node//*[contains(text(),"{name}")]')).click()
        WebUI.delay(1)

    @classmethod
    def set_dataset_acl_by_api(cls, dataset: str, acltype: str, dacl: str) -> Response:
        """
        This method sets the dataset acl user and group permissions.

        :param dataset: is the user permissions.
        :param acltype: is the type of acl the dataset is. [NFS4/POSIX1E/DISABLED]
        :param dacl: is the dacl permissions.
        :return: the payload.
        """
        payload = '{"path": "'+dataset+'", "dacl": '+dacl+', "acltype": "'+acltype+'", "options": {"stripacl": false}}'
        return API_POST.set_filesystem_acl(payload)

    @classmethod
    def set_dataset_acl_user_and_group_payload(cls, user: str, group: str) -> str:
        """
        This method returns the dataset acl user and group permissions payload.

        :param user: is the user permissions.
        :param group: is the group permissions.
        :return: the payload.
        """
        payload = '[{"tag": "owner@", "id": -1, "perms": {"BASIC": "'+user+'" } "flags": {"BASIC": "INHERIT" }, "type": "ALLOW" }, {"tag": "group@", "id": -1, "perms": {"BASIC": "'+group+'" }, "flags": {"BASIC": "INHERIT" }, "type": "ALLOW" }, {"tag": "GROUP", "id": 545, "perms": {"BASIC": "MODIFY" }, "flags": {"BASIC": "INHERIT" }, "type": "ALLOW" }, {"tag": "GROUP", "id": 544, "perms": {"BASIC": "FULL_CONTROL" }, "flags": {"BASIC": "INHERIT" }, "type": "ALLOW" }]'
        return payload

    @classmethod
    def set_dataset_permissions_user_and_group_by_api(cls, dataset: str, user: str, group: str) -> Response:
        """
        This method deletes the given dataset.

        :param dataset: is the dataset name.
        :param user: is the user to set permissions.
        :param group: is the group to set permissions.
        :return: the API request response.
        """
        return API_POST.set_dataset_permissions_user_and_group(dataset, user, group)

