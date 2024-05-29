
def cloud_credential_add_button() -> str:
    """
    This function returns the xpath text of the cloud credential add button.

    :return: The xpath text of the cloud credential add button.
    """
    return 'add-cloud-credential'


def cloud_credential_delete_button(name: str) -> str:
    """
    This function returns the xpath text of the cloud credential delete button by the given name.

    :param name: The name of the cloud credential.
    :return: The xpath text of the cloud credential delete button by the given name.
    """
    return f'cloud-cred-{name}-delete-row-action'


def cloud_credential_description(name: str, description: str) -> str:
    """
    This function returns the xpath text of the cloud credential description by the given description.

    :param name: The name of the cloud credential.
    :param description: The description of the cloud credential.
    :return: The xpath text of the cloud credential description by the given description.
    """
    return f'//*[@data-test="text-provider-cloud-cred-{name}-row-text" and contains(text(), "{description}")]'


def cloud_credential_edit_button(name: str) -> str:
    """
    This function returns the xpath text of the cloud credential edit button by the given name.

    :param name: The name of the cloud credential.
    :return: The xpath text of the cloud credential edit button by the given name.
    """
    return f'cloud-cred-{name}-edit-row-action'


def cloud_credential_name(name: str) -> str:
    """
    This function returns the xpath text of the cloud credential name by the given name.

    :param name: The name of the cloud credential.
    :return: The xpath text of the cloud credential name by the given name.
    """
    return f'//*[@data-test="text-name-cloud-cred-{name}-row-text"]'


def ssh_connection_add_button() -> str:
    """
    This function returns the xpath text of the ssh connection add button.

    :return: The xpath text of the ssh connection add button.
    """
    return 'add-ssh-connection'


def ssh_connection_delete_button(name: str) -> str:
    """
    This function returns the xpath text of the ssh connection delete button by the given name.

    :param name: The name of the ssh connection.
    :return: The xpath text of the ssh connection delete button by the given name.
    """
    return f'ssh-con-{name}-delete-row-action'


def ssh_connection_edit_button(name: str) -> str:
    """
    This function returns the xpath text of the ssh connection edit button by the given name.

    :param name: The name of the ssh connection.
    :return: The xpath text of the ssh connection edit button by the given name.
    """
    return f'ssh-con-{name}-edit-row-action'


def ssh_connection_name(name: str) -> str:
    """
    This function returns the xpath text of the ssh connection name by the given name.

    :param name: The name of the ssh connection.
    :return: The xpath text of the ssh connection name by the given name.
    """
    return f'//*[@data-test="text-name-ssh-con-{name}-row-text"]'


def ssh_keypairs_add_button() -> str:
    """
    This function returns the xpath text of the ssh keypair add button.

    :return: The xpath text of the ssh keypair add button.
    """
    return 'add-ssh-keypair'


def ssh_keypairs_delete_button(name: str) -> str:
    """
    This function returns the xpath text of the ssh keypair delete button by the given name.

    :param name: The name of the ssh keypair.
    :return: The xpath text of the ssh keypair delete button by the given name.
    """
    return f'ssh-keypair-{name}-key-delete-row-action'


def ssh_keypairs_edit_button(name: str) -> str:
    """
    This function returns the xpath text of the ssh keypair edit button by the given name.

    :param name: The name of the ssh keypair.
    :return: The xpath text of the ssh keypair edit button by the given name.
    """
    return f'ssh-keypair-{name}-key-edit-row-action'


def ssh_keypairs_name(name: str) -> str:
    """
    This function returns the xpath text of the ssh keypair name by the given name.

    :param name: The name of the ssh keypair.
    :return: The xpath text of the ssh keypair name by the given name.
    """
    return f'//*[@data-test="text-name-ssh-keypair-{name}-key-row-text"]'
