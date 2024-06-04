
def boot_pool_status(status: str) -> str:
    """
    This method returns the xpath of the boot pool status.
    :param status: The status of the boot pool.
    :return: The xpath of the boot pool status.
    """
    return f'//ix-bootenv-node-item[contains(., "{status}") and contains(.,"boot-pool")]'
