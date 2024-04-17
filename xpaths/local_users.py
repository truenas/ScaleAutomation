
def user(name: str) -> str:
    """
    This function sets the text for the given local username

    :param name: text of the given username
    :return: xpath string for given username
    """
    return f'//*[@data-test="row-user-{name}"]'
