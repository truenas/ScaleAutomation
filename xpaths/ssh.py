
def label_ssh_type_name(sshtype: str, name: str) -> str:
    """
    This function returns the xpath text of the given connection.

    :param sshtype: The type of connection.
    :param name: The name of connection.
    :return: The xpath text of the given connection.
    """
    return f'//ix-ssh-{sshtype}-card//span[starts-with(text(),"{name}")]'


def button_ssh_view_more_type(sshtype: str) -> str:
    """
    This function returns the xpath text of the given connection type view more button.

    :param sshtype: The type of connection.
    :return: The xpath text of the given connection type view more button.
    """
    return f'//ix-ssh-{sshtype}-card/descendant::button[@data-test="button-show-more"]'

