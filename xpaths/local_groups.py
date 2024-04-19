
def allow_sudo_commands(name: str) -> str:
    """
    This function sets the xpath for the given group allow sudo commands value

    :param name: name of the given group
    :return: xpath string for given group allow sudo commands value
    """
    return f'//*[@data-test="text-allows-sudo-commands-group-{name}-row-yesno"]'


def builtin(name: str) -> str:
    """
    This function sets the xpath for the given group builtin value

    :param name: name of the given group
    :return: xpath string for given group builtin value
    """
    return f'//*[@data-test="text-builtin-group-{name}-row-yesno"]'


def gid(name: str) -> str:
    """
    This function sets the xpath for the given group gid value

    :param name: name of the given group
    :return: xpath string for given group gid value
    """
    return f'//*[@data-test="text-gid-group-{name}-row-text"]'


def group(name: str) -> str:
    """
    This function sets the xpath for the given group group value

    :param name: name of the given group
    :return: xpath string for given group group value
    """
    return f'//*[@data-test="text-group-group-{name}-row-text"]'


def members_group_member(name: str) -> str:
    """
    This function sets the xpath for the given group member's group member value

    :param name: name of the given member user
    :return: xpath string for given group member's group member value
    """
    return f'//*[@id="member-list"]//*[text()="{name}"]'


def members_user(name: str) -> str:
    """
    This function sets the xpath for the given group member's user value

    :param name: name of the given member user
    :return: xpath string for given group member's user value
    """
    return f'//mat-list-item//*[contains(text(),"{name}")]'


def roles(name: str) -> str:
    """
    This function sets the xpath for the given group roles value

    :param name: name of the given group
    :return: xpath string for given group roles value
    """
    return f'//*[@data-test="text-roles-group-{name}-row-text"]'


def samba_auth(name: str) -> str:
    """
    This function sets the xpath for the given group samba auth value

    :param name: name of the given group
    :return: xpath string for given group samba auth value
    """
    return f'//*[@data-test="text-samba-authentication-group-{name}-row-yesno"]'
