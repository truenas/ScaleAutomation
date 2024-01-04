
def truenas_help_card_link(link: str) -> str:
    """
    This method return the xpath text of the TrueNAS help card link

    :param link: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-help//*[@href="{link}"]'
