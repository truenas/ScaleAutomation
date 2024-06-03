
def advanced_access_terminate_session(name: str = "") -> str:
    """
    This function sets the text for the session to terminate

    :param name: is optional name of the session to terminate
    :return: xpath string for given session to terminate
    """
    return f'//*[contains(@data-test,"button-session-{name}") and contains(@data-test,"-exit-to-app-row-action")]'
