
def builtin(name: str) -> str:
    """
    This function sets the xpath for the given user builtin value

    :param name: name of the given user
    :return: xpath string for given user builtin value
    """
    return f'//*[@data-test="text-builtin-user-{name}-row-yesno"]'


def full_name(name: str) -> str:
    """
    This function sets the xpath for the given user full name value

    :param name: name of the given user
    :return: xpath string for given user full name value
    """
    return f'//*[@data-test="text-full-name-user-{name}-row-text"]'


def roles(name: str) -> str:
    """
    This function sets the xpath for the given user roles value

    :param name: name of the given user
    :return: xpath string for given user roles value
    """
    return f'//*[@data-test="text-roles-user-{name}-row-text"]'


def uid(name: str) -> str:
    """
    This function sets the xpath for the given user uid value

    :param name: name of the given user
    :return: xpath string for given user uid value
    """
    return f'//*[@data-test="text-uid-user-{name}-row-text"]'


def user(name: str) -> str:
    """
    This function sets the xpath for the given user username value

    :param name: name of the given user
    :return: xpath string for given user username value
    """
    return f'//*[@data-test="text-username-user-{name}-row-text"]'
