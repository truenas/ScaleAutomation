
def truenas_help_card_link(link: str) -> str:
    """
    This method return the xpath text of the TrueNAS help card link

    :param link: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-help//*[@href="{link}"]'


def drag_card(field: str) -> str:
    """
    This method return the xpath text of the TrueNAS help card link

    :param field: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-{field}//span[@class="cdk-drag-handle"]'


def drop_card(field: str) -> str:
    """
    This method return the xpath text of the TrueNAS help card link

    :param field: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-{field}//mat-card'


def card_list_item(field: str, item_position: int) -> str:
    return f'(//ix-widget-{field}//mat-list-item)[{item_position}]'
