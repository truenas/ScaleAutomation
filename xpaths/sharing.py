
def iscsi_target_name(target_name: str) -> str:
    """
    This function sets the text for the given iSCSI target name

    :param target_name: text of the given iSCSI target name
    :return: xpath string for given iSCSI target name
    """
    return f'//*[@data-test="text-target-name-card-iscsi-target-{target_name}-row-text"]'
