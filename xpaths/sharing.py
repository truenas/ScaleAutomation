
def iscsi_card_target_name(target_name: str) -> str:
    """
    This function sets the text for the given iSCSI target name

    :param target_name: text of the given iSCSI target name
    :return: xpath string for given iSCSI target name
    """
    return f'//*[@data-test="text-target-name-card-iscsi-target-{target_name}-row-text"]'


def share_edit_button(share_type: str, name: str) -> str:
    """
    This function sets the text for the given share edit button

    :param share_type: type of the given share [smb-share/nfs-share/iscsi-target]
    :param name: name of the given share
    :return: xpath string for given share edit button
    """
    return f'//*[@data-test="button-card-{share_type}-{name}-edit-row-action"]'


def share_enabled_toggle(share_type: str, name: str) -> str:
    """
    This function sets the text for the given share enabled toggle

    :param share_type: type of the given share [smb/nfs]
    :param name: name of the given share
    :return: xpath string for given share enabled toggle
    """
    return f'//*[@data-test="toggle-enabled-card-{share_type}-share-{name}-row-toggle"]//button'


def share_row_name(first_col: str, share_type: str, name: str) -> str:
    """
    This function sets the text of the row first column for given share

    :param first_col: name of the first column of the given share [name/path/target-name]
    :param share_type: type of the given share [smb-share/nfs-share/iscsi-target]
    :param name: name of the given share
    :return: xpath string of the row first column for given share
    """
    return f'//*[@data-test="text-{first_col}-card-{share_type}-{name}-row-text"]'
