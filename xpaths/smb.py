

def smb_share_options(name: str) -> str:
    """
    This function sets the text for the given share name

    :param name: name of the given share
    :return: xpath string for given share name
    """
    return f'//*[@data-test="row-{name}"]//*[@data-test="button-samba-options"]'

