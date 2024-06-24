

def smb_acl_empty_entry_who() -> str:
    """
    This function returns the text for the first empty who field in the SMB ACL panel

    :return: xpath string for the first empty who field in the SMB ACL panel
    """
    return '(//*[contains(@class, "select-placeholder")]/ancestor::ix-select//*[@data-test="select-ae-who"])[1]'


def smb_acl_select_field(entry_type: str, field_type: str) -> str:
    """
    This function returns the text for the given share ACL select field

    :param entry_type: type of the entry. [user/group]
    :param field_type: type of the field. [perm/type]
    :return: xpath string for given share ACL select field
    """
    return f'//*[contains(text(),"{entry_type}")]/ancestor::ix-list-item//*[@data-test="select-ae-{field_type}"]'


def smb_share_options(name: str) -> str:
    """
    This function returns the text for the given share name options button

    :param name: name of the given share
    :return: xpath string for given share name options button
    """
    return f'//*[@data-test="row-{name}"]//*[@data-test="button-samba-options"]'

