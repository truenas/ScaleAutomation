
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
