"""This module contains common xpath strings"""

overlay_container = '//*[@class="cdk-overlay-container"]'
"""This variable returns the overlay container xpath text and is used to close the select option dropdown"""
progress_bar = '//mat-progress-bar'
"""This variable returns the default progress bar xpath text"""
progress_spinner = '//mat-spinner'
"""This variable returns the default spinner xpath text"""


def any_child_parent_target(child: str, parent: str, target: str) -> str:
    """
    This function sets the xpath for the given child/parent/target

    :param child: text of the child object
    :param parent: text of the parent object
    :param target: text of the target object
    :return: xpath string for given child/parent/target
    """
    return f'{child}/ancestor::{parent}//descendant::{target}'


def any_data_test(name: str) -> str:
    """
    This function sets the xpath for the given data-test object

    :param name: name of the data-test object
    :return: xpath string for given data-test object
    """
    return f'//*[@data-test="{name}"]'


def any_header(text: str, level: int) -> str:
    """
    This function sets the xpath for the given header

    :param text: text of the header
    :param level: level of the header
    :return: xpath string for given header
    """
    return f"//h{level}[contains(text(),'{text}')]"


def any_pill(name: str, text: str) -> str:
    """
    This function sets the xpath for the given pill

    :param name: name of the input associated with the pill
    :param text: text of the pill
    :return: xpath string for given pill
    """
    return f'//*[@data-test="input-{name}"]/preceding-sibling::mat-chip-row/descendant::*[contains(text(),"{text}")]'


def any_pill_delete(name: str, text: str) -> str:
    """
    This function sets the xpath for the given pill

    :param name: name of the input associated with the pill
    :param text: text of the pill
    :return: xpath string for given pill
    """
    return f'//*[@data-test="input-{name}"]/preceding-sibling::mat-chip-row/descendant::*[contains(text(),"{text}")]/ancestor::span/following-sibling::*/ix-icon'


def any_start_with_field(field: str) -> str:
    """
    This function sets the text for the given field name with starts with.

    :param field: text of the given field.
    :return: returns the xpath string for given field.
    """
    return f'//*[starts-with(@data-test,"{field}")]'


def any_text(text: str) -> str:
    """
    This function sets the xpath for the given text

    :param text: text of the given text
    :return: xpath string for given text
    """
    return f"//*[contains(text(),'{text}')]"


def any_xpath(xpath: str) -> str:
    """
    This function sets the xpath for the given xpath

    :param xpath: text of the given xpath.
    :return: xpath string for given xpath.
    """
    return f"{xpath}"


def button_field(field: str) -> str:
    """
    This function sets the text for the given button name

    :param field: text of the given button name
    :return: xpath string for given button
    """
    return f'//*[@data-test="button-{field}"]'


def button_field_by_row(field: str, row: int) -> str:
    """
    This function sets the text for the given button name

    :param field: text of the given button name
    :param row: row number of the given button
    :return: xpath string for given button
    """
    return f'(//*[@data-test="button-{field}"])[{row}]'


def button_share_action_by_name(sharetype: str, name: str, action: str) -> str:
    """
    This function sets the text for the given button name

    :param sharetype: type of the given share
    :param name: text of the given share name
    :param action: action to be taken
    :return: xpath string for the given acton button
    """
    return f'//ix-{sharetype}-card//span[contains(text(),"{name}")]/ancestor::tr/descendant::*[contains(@data-test,"-{action}-row-action")]'


def button_share_actions_menu(sharetype: str) -> str:
    """
    This function sets the text for the given button name

    :param sharetype: type of the given share
    :return: xpath string for the given acton button
    """
    return f'//ix-{sharetype}-card//ix-service-extra-actions//button'


def card_label_and_value(card_tile: str, label: str, value: str) -> str:
    """
    This function sets the text for the given card label and value.

    :param card_tile: text of the given card tile.
    :param label: text of the given label.
    :param value: text of the given value.
    :return: the xpath text of the given card label and value.
    """
    return f'//mat-card[contains(.,"{card_tile}")]//*[contains(.,"{label}") and contains(.,"{value}")]'


def card_title(text: str) -> str:
    """
    The function returns the xpath text of the given card title.

    :param text: is the text of the card title.
    :return: the xpath text of the given card title.
    """
    return f'//mat-card//h3[contains(.,"{text}")]'


def checkbox_field(field: str) -> str:
    """
    This function sets the text for the given checkbox name

    :param field: text of the given checkbox name
    :return: xpath string for given checkbox
    """
    return f'//*[@data-test="checkbox-{field}"]'


def checkbox_field_attribute(field: str) -> str:
    """
    This function sets the text for the given checkbox attribute name

    :param field: text of the given checkbox attribute name
    :return: xpath string for given checkbox attribute
    """
    return f'//*[@data-test="checkbox-{field}"]//input'


def checkbox_field_by_row(field: str, row: int) -> str:
    """
    This function sets the text for the given checkbox name

    :param field: text of the given checkbox name
    :param row: row number of the given checkbox
    :return: xpath string for given checkbox
    """
    return f'(//*[@data-test="checkbox-{field}"])[{row}]'


def checkbox_field_by_row_attribute(field: str, row: int) -> str:
    """
    This function sets the text for the given checkbox attribute name

    :param field: text of the given checkbox attribute name
    :param row: row number of the given checkbox
    :return: xpath string for given checkbox attribute
    """
    return f'(//*[@data-test="checkbox-{field}"])[{row}]//input'


def close_right_panel() -> str:
    """
    This function returns the text for the close right panel button

    :return: xpath string for the close right panel button
    """
    return '//*[@id="ix-close-icon"]'


def data_test_field(field: str) -> str:
    """
    This function sets the text for the given data-test tag

    :param field: text of the given data-test tag
    :return: xpath string for given data-test tag
    """
    return f'//*[@data-test="{field}"]'


def dataset_permissions_group(name: str) -> str:
    """
    This function sets the text for the given dataset permission group

    :param name: text of the given Group name
    :return: xpath string for given dataset permission group
    """
    return f'//*[contains(text(),"Group:")]/following-sibling::*[contains(text(),"{name}")]'


def dataset_permissions_ownership(name: str) -> str:
    """
    This function sets the text for the given dataset permission ownership

    :param name: text of the given Ownership name
    :return: xpath string for given dataset permission ownership
    """
    return f'//*[contains(text(),"Owner:")]/following-sibling::*[contains(text(),"{name}")]'


def input_field(field: str) -> str:
    """
    This function sets the text for the given input name

    :param field: text of the given input name
    :return: xpath string for given input
    """
    return f'//*[@data-test="input-{field}"]'


def input_delete_button(field: str) -> str:
    """
    This function sets the text for the given input name

    :param field: text of the given input name
    :return: xpath string for given input
    """
    return f'//*[@data-test="input-{field}"]/..//ix-icon'


def label_and_value(label: str, value: str) -> str:
    """
    This function sets the text for the given label and value

    :param label: text of the given label
    :param value: text of the given value
    :return: xpath string for given label and value
    """
    return f'//*[contains(.,"{label}") and contains(.,"{value}")]'


def link_field(field: str) -> str:
    """
    This function sets the text for the given link name

    :param field: text of the given link name
    :return: xpath string for given link
    """
    return f'//*[@data-test="link-{field}"]'


def option_field(field: str) -> str:
    """
    This function sets the text for the given option name

    :param field: text of the given option name
    :return: xpath string for given option
    """
    return f'//*[@data-test="option-{field}"]'


def radio_button_field(field: str) -> str:
    """
    This function sets the text for the given radio button name

    :param field: text of the given radio button name
    :return: xpath string for given radio button
    """
    return f'//*[@data-test="radio-button-{field}"]'


def radio_button_field_attribute(field: str) -> str:
    """
    This function sets the text for the given checkbox attribute name

    :param field: text of the given checkbox attribute name
    :return: xpath string for given checkbox attribute
    """
    return f'//*[@data-test="radio-button-{field}"]//input'


def search_field() -> str:
    """
    This function sets the text for the search field

    :return: xpath string for given select
    """
    return '//*[@data-test="input-search"]'


def select_field(field: str) -> str:
    """
    This function sets the text for the given select name

    :param field: text of the given select name
    :return: xpath string for given select
    """
    return f'//*[@data-test="select-{field}"]'


def select_field_by_row(field: str, row: int) -> str:
    """
    This function sets the text for the given select name

    :param field: text of the given select name
    :param row: row number of the given select
    :return: xpath string for given select
    """
    return f'(//*[@data-test="select-{field}"])[{row}]'


def selected_dataset(name: str) -> str:
    """
    This function sets the text for the given dataset

    :param name: name of the given dataset
    :return: xpath string for given dataset
    """
    return f'//*[contains(@class,"own-name") and contains(text(),"{name}")]'


def share_attached(name: str, sharetype: str) -> str:
    """
    This function sets the text for the given attached share

    :param name: name of the given attached share
    :param sharetype: the type of attached share
    :return: xpath string for given attached share
    """
    xpath = f"""//*[contains(text(),"Share Attached:")]/following-sibling::*[contains(text(), "Dataset is shared via """
    if sharetype == 'smb':
        return xpath+f"""SMB as '{name}'")]"""
    if sharetype == 'nfs':
        return xpath+f'NFS")]'


def share_attribute(sharetype: str, attribute: str, desc: str) -> str:
    """
    This function sets the text for the given share name

    :param sharetype: type of the given share
    :param attribute: attribute of the given share [name/path/description]
    :param desc: description of the given share
    :return: xpath string for given share name
    """
    index = 1
    if sharetype == "smb":
        if attribute == 'name':
            index = 1
        if attribute == 'path':
            index = 2
        if attribute == 'description':
            index = 3
    if sharetype == 'nfs':
        if attribute == 'path':
            index = 1
        if attribute == 'description':
            index = 2
    return f'//ix-{sharetype}-card//*[@data-test="row"]/td[{index}]/descendant::*[contains(text(),"{desc}")]'


def share_enabled_slider(sharetype: str, name: str) -> str:
    """
    This function sets the text for the given share name

    :param sharetype: type of the given share
    :param name: name of the given share
    :return: xpath string for given share name
    """
    return f'//ix-{sharetype}-card//*[contains(text(),"{name}")]/ancestor::tr/descendant::mat-slide-toggle//button'


def step_header_is_open(header: str) -> str:
    """
    This function sets the text for the given step header

    :param header: The name of the header of the step.
    :return: The xpath string for the given step header.
    """
    # tabindex="0" means the step is open in the UI.
    return f'//mat-step-header[@tabindex="0" and contains(.,"{header}")]'


def textarea_field(field: str) -> str:
    """
    This function sets the text for the given textarea name

    :param field: text of the given textarea name
    :return: xpath string for given textarea
    """
    return f'//*[@data-test="textarea-{field}"]'


def toggle_field(field: str) -> str:
    """
    This function sets the text for the given toggle field

    :param field: name of the given toggle field
    :return: xpath string for given toggle field
    """
    return f'//*[@data-test="toggle-{field}"]//button'


def tree_node_field(field: str) -> str:
    """
    This function sets the text for the given tree node name

    :param field: text of the given tree node name
    :return: xpath string for given tree node
    """
    return f'//ix-tree-node//span[contains(text(),"{field}")]'
