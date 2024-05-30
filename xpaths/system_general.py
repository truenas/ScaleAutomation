
def delete_ntp_server(name: str) -> str:
    """
    This function sets the text for the delete button of the given NTP server.

    :param name: the name of NTP server
    :return: xpath string for the delete button of the given NTP server

    :example: ftp_permissions_table_checkbox('0.debian.pool')
    """
    return f'//*[contains(@data-test,"button-ntp-server-{name}") and contains(@data-test,"-delete-row-action")]'
