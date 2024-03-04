def ftp_directory_permissions_table_checkbox(level: str, perm: str) -> str:
    """
    This function sets the text for the given checkbox name on the directory permissions table

    :param level: the level of permission
    :param perm: the permission type
    :return: xpath string for given checkbox

    :example: ftp_directory_permissions_table_checkbox('user', 'read')
    """
    return ftp_permissions_table_checkbox('dir', level, perm)


def ftp_file_permissions_table_checkbox(level: str, perm: str) -> str:
    """
    This function sets the text for the given checkbox name on the file permissions table

    :param level: the level of permission
    :param perm: the permission type
    :return: xpath string for given checkbox

    :example: ftp_directory_permissions_table_checkbox('user', 'read')
    """
    return ftp_permissions_table_checkbox('file', level, perm)


def ftp_permissions_table_checkbox(table: str, level: str, perm: str) -> str:
    """
    This function sets the text for the given checkbox name on the given table

    :param table: the table to select
    :param level: the level of permission
    :param perm: the permission type
    :return: xpath string for given checkbox

    :example: ftp_permissions_table_checkbox('file', 'user', 'read')
              ftp_permissions_table_checkbox('dir', 'group', 'execute')
    """
    return f'//*[@data-test="row-{table}mask-{level}-permissions"]/ancestor::table//*[@data-test="checkbox-{level}-{perm}"]'
