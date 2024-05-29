
def checkbox_locked_snapshot_hold(name: str) -> str:
    """
    This function returns the xpath text of the hold checkbox for a dataset snapshot.

    :param name: The name of the given dataset.
    :return: xpath text of the hold checkbox for a dataset snapshot.
    """
    return f'//*[contains(text(),"{name}")]/ancestor::tbody//*[@data-test="checkbox"]/ancestor::span//ix-icon[@name="lock"]'


def dataset_encryption_text(dataset_name: str) -> str:
    """
    This function returns the xpath text of the given dataset encryption text.

    :param dataset_name: The name of the dataset.
    :return: The xpath text of the given dataset encryption text.
    """
    return f'//ix-dataset-node[contains(.,"{dataset_name}")]//ix-dataset-encryption-cell/div/div'


def dataset_ace_permission_checkbox(level: str) -> str:
    """
    This function returns the xpath text of the given dataset ace permission checkbox.

    :param level: The level of the permission.
    :return: The xpath text of the given dataset encryption text.
    """
    return f'//ix-edit-posix-ace//*[contains(text(), "{level}")]//ancestor::mat-checkbox'


def dataset_permission_custom_preset_delete_button(name: str) -> str:
    """
    This function returns the xpath text of the given custom preset delete button.

    :param name: The name of the preset.
    :return: the xpath text of the given custom preset delete button.
    """
    return f'//*[contains(text(), "{name}")]//parent::*//child::*[@name="cancel"]'


def dataset_permissions_item(name: str, permissions: str) -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param name: The name of the item.
    :param permissions: The permissions of the item.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//ix-permissions-item[contains(.,"{name}") and contains(.,"{permissions}")]'


def dataset_permissions_item_advanced(name: str, permission_item: str) -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param name: The name of the dataset.
    :param permission_item: The permission item text.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//cdk-accordion-item[contains(.,"{name}")]//*[contains(text(),"{permission_item}")]'


def dataset_posix_permissions_obj(obj_type: str, name: str) -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param obj_type: The object type of the item.
    :param name: The name of the item.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//*[contains(text(),"POSIX Permissions")]/..//*[contains(text(),"{obj_type} Obj – {name}")]'


def dataset_protection_task(task: str, value: str = '') -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param task: The name of the task.
    :param value: The value of the task.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//ix-data-protection-card//mat-card-content//div/div[contains(.,"{task}")]{value}'


def dataset_roles_icon(share_type: str) -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param share_type: The share type of the item.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//ix-dataset-roles-cell//ix-icon[@name="ix:{share_type}"]'


def link_dataset(name: str) -> str:
    """
    This function returns the xpath text of the given dataset.

    :param name: The name of the given dataset.
    :return: xpath string for given dataset.
    """
    return f'//ix-dataset-node//*[contains(text(),"{name}")]'


def selected_dataset_name(name: str) -> str:
    """
    This function returns the xpath text of the given dataset.

    :param name: The name of the given dataset.
    :return: xpath string for given dataset.
    """
    return f'//*[contains(@class,"own-name") and contains(text(),"{name}")]'


def selected_dataset_group() -> str:
    """
    This function returns the xpath text of the given  dataset's group.

    :return: xpath string for given dataset.
    """
    return '//*[contains(text(),"Group:")]//ancestor::div/*[@class="value ng-star-inserted"]'


def selected_dataset_owner() -> str:
    """
    This function returns the xpath text of the given dataset's owner.

    :return: xpath string for given dataset.
    """
    return '//*[contains(text(),"Owner:")]//ancestor::div/*[@class="value ng-star-inserted"]'

