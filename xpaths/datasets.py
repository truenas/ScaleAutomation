
def dataset_permissions_item(name: str, permissions: str) -> str:
    """
    This function returns the xpath text of the given dataset permission item.

    :param name: The name of the item.
    :param permissions: The permissions of the item.
    :return: The xpath text of the given dataset permission item.
    """
    return f'//ix-permissions-item[contains(.,"{name}") and contains(.,"{permissions}")]'
