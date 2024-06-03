
def bootenv_actions_button(be_name: str) -> str:
    """
    This method returns the xpath of the boot environment actions button.
    :param be_name: The name of the boot environment.
    :return: The xpath of the boot environment actions button.
    """
    return f'//*[@data-test="row-{be_name}"]//*[@data-test="button-bootenv-actions"]'


def boot_pool_status(status: str) -> str:
    """
    This method returns the xpath of the boot pool status.
    :param status: The status of the boot pool.
    :return: The xpath of the boot pool status.
    """
    return f'//ix-bootenv-node-item[contains(., "{status}") and contains(.,"boot-pool")]'
