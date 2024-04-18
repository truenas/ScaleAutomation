
def builtin(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="text-builtin-user-{name}-row-yesno"]'


def full_name(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="text-full-name-user-{name}-row-text"]'


def roles(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="text-roles-user-{name}-row-text"]'


def uid(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="text-uid-user-{name}-row-text"]'


def user(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="text-username-user-{name}-row-text"]'
