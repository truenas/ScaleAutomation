cpu_subtitle = '//*[@id="text-subtitle"]'
"""This variable returns the cpu subtitle xpath text"""
cpu_cores_chart = '//*[@id="cpu-cores-chart"]'
"""This variable returns the cpu cores chart xpath text"""


def card_list_item(field: str, item_position: int) -> str:
    """
    This function returns the xpath text of give card and list item_position.

    :param field: is the name of ix-widget.
    :param item_position: it the position of the list on the card.
    :return:  the xpath text of give card and list item_position
    """
    return f'(//ix-widget-{field}//mat-list-item)[{item_position}]'


def cpu_load_cores(index: int) -> str:
    """
    This function return the cpu load cores xpath text by the given index.

    :param index: the nuber of the item to get.
    :return: the cpu load cores xpath text by the given index.
    """
    return f'//*[@id="cpu-load-cores-legend-values"]/div[{index}]/span'


def drag_card(field: str) -> str:
    """
    This function return the xpath text of the TrueNAS help card link

    :param field: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    # return f'//ix-widget-{field}//span[@class="cdk-drag-handle"]'
    return f'//ix-widget-{field}//span[@class="grip ng-star-inserted"]'


def drop_card(field: str) -> str:
    """
    This function return the xpath text of the TrueNAS help card link

    :param field: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-{field}//mat-card'


def truenas_help_card_link(link: str) -> str:
    """
    This function return the xpath text of the TrueNAS help card link

    :param link: is the url text of the link on the TrueNAS help card
    :return: the xpath text of the TrueNAS help card link
    """
    return f'//ix-widget-help//*[@href="{link}"]'
