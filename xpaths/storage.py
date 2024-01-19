
def label_disk_name_by_row(row: int) -> str:
    """
    This function returns the disk name xpath text of the given row.

    :param row: The row number of the disk name.
    :return: The disk name xpath text of the given row.
    """
    return f'(//datatable-body-row)[{row}]//datatable-body-cell[2]/div'


def pool_cards_item_value(pool_name: str, item: str, value: str) -> str:
    """
    This function returns the xpath text of the given pool name, item and value.

    :param pool_name: the name of the pool
    :param item: the item to look at
    :param value: the value of the item.
    :return: the xpath text of the given pool name, item and value.
    """
    return f'//ix-dashboard-pool[contains(.,"{pool_name} ")]//*[contains(.,"{item}") and contains(.,"{value}")]'


def pool_name_header(pool_name: str) -> str:
    """
    This function returns the xpath text of the given pool name header.

    :param pool_name: the name of the pool
    :return: the xpath text of the given pool name header.
    """
    return f'//*[contains(text(),"{pool_name}") and @class="pool-name"]'


def pool_wizard_step_header_open(header: str) -> str:
    """
    This function returns the xpath text of the given pool name header.

    :param header: the name of the header
    :return: the xpath text of the given pool name header.
    """
    # tabindex="0" means the header is visible in the UI.
    return f'//mat-step-header[@tabindex="0" and contains(.,"{header}")]'
