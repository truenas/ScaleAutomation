progress_bar = '//mat-progress-bar'
"""This variable returns the default progress bar xpath text"""
progress_spinner = '//mat-spinner'
"""This variable returns the default spinner xpath text"""


def any_child_parent_target(child: str, parent: str, target: str) -> str:
    """
    This method sets the xpath for the given child/parent/target

    :param child: text of the child object
    :param parent: text of the parent object
    :param target: text of the target object
    :return: xpath string for given child/parent/target
    """
    return f'{child}/ancestor::{parent}//descendant::{target}'


def any_header(text: str, level: int) -> str:
    """
    This method sets the xpath for the given header

    :param text: text of the header
    :param level: level of the header
    :return: xpath string for given header
    """
    return f"//h{level}[contains(text(),'{text}')]"


def any_text(text: str) -> str:
    """
    This method sets the xpath for the given text

    :param text: text of the given text
    :return: xpath string for given text
    """
    return f"//*[contains(text(),'{text}')]"


def any_xpath(xpath: str) -> str:
    """
    This method sets the xpath for the given xpath

    :param xpath: text of the given xpath.
    :return: xpath string for given xpath.
    """
    return f"{xpath}"


def any_start_with_field(field: str) -> str:
    """
    This method sets the text for the given field name with starts with.

    :param field: text of the given field.
    :return: returns the xpath string for given field.
    """
    return f'//*[starts-with(@data-test,"{field}")]'


def button_field(field: str) -> str:
    """
    This method sets the text for the given button name

    :param field: text of the given button name
    :return: xpath string for given button
    """
    return f'//*[@data-test="button-{field}"]'


def button_share_action_by_name(sharetype: str, name: str, action: str) -> str:
    """
    This method sets the text for the given button name

    :param sharetype: type of the given share
    :param name: text of the given share name
    :param action: action to be taken
    :return: xpath string for the given acton button
    """
    return f'//ix-{sharetype}-card//span[contains(text(),"{name}")]/ancestor::tr/descendant::*[contains(@data-test,"-{action}-row-action")]'


def card_title(text: str) -> str:
    """
    The method returns the xpath text of the given card title.

    :param text: is the text of the card title.
    :return: the xpath text of the given card title.
    """
    return f'//mat-card//h3[contains(.,"{text}")]'


def checkbox_field(field: str) -> str:
    """
    This method sets the text for the given checkbox name

    :param field: text of the given checkbox name
    :return: xpath string for given checkbox
    """
    return f'//*[@data-test="checkbox-{field}"]'


def checkbox_field_attribute(field: str) -> str:
    """
    This method sets the text for the given checkbox attribute name

    :param field: text of the given checkbox attribute name
    :return: xpath string for given checkbox attribute
    """
    return f'//*[@data-test="checkbox-{field}"]//input'


def close_right_panel() -> str:
    """
    This method returns the text for the close right panel button

    :return: xpath string for the close right panel button
    """
    return '//*[@id="ix-close-icon"]'


def data_test_field(field: str) -> str:
    """
    This method sets the text for the given data-test tag

    :param field: text of the given data-test tag
    :return: xpath string for given data-test tag
    """
    return f'//*[@data-test="{field}"]'


def dataset_permissions_group(name: str) -> str:
    """
    This method sets the text for the given dataset permission group

    :param name: text of the given Group name
    :return: xpath string for given dataset permission group
    """
    return f'//*[contains(text(),"Group:")]/following-sibling::*[contains(text(),"{name}")]'


def dataset_permissions_ownership(name: str) -> str:
    """
    This method sets the text for the given dataset permission ownership

    :param name: text of the given Ownership name
    :return: xpath string for given dataset permission ownership
    """
    return f'//*[contains(text(),"Owner:")]/following-sibling::*[contains(text(),"{name}")]'


def input_field(field: str) -> str:
    """
    This method sets the text for the given input name

    :param field: text of the given input name
    :return: xpath string for given input
    """
    return f'//*[@data-test="input-{field}"]'


def link_dataset(name: str) -> str:
    """
    This method sets the text for the given dataset

    :param name: name of the given dataset
    :return: xpath string for given dataset
    """
    return f'//ix-dataset-node//*[contains(text(),"{name}")]'


def link_field(field: str) -> str:
    """
    This method sets the text for the given link name

    :param field: text of the given link name
    :return: xpath string for given link
    """
    return f'//*[@data-test="link-{field}"]'


def option_field(field: str) -> str:
    """
    This method sets the text for the given option name

    :param field: text of the given option name
    :return: xpath string for given option
    """
    return f'//*[@data-test="option-{field}"]'


def search_field() -> str:
    """
    This method sets the text for the search field

    :return: xpath string for given select
    """
    return '//*[@data-test="input"]'


def select_field(field: str) -> str:
    """
    This method sets the text for the given select name

    :param field: text of the given select name
    :return: xpath string for given select
    """
    return f'//*[@data-test="select-{field}"]'


def selected_dataset(name: str) -> str:
    """
    This method sets the text for the given dataset

    :param name: name of the given dataset
    :return: xpath string for given dataset
    """
    return f'//*[contains(@class,"own-name") and contains(text(),"{name}")]'


def share_attached(name: str) -> str:
    """
    This method sets the text for the given attached share

    :param name: name of the given attached share
    :return: xpath string for given attached share
    """
    return f'''//*[contains(text(),"Share Attached:")]/following-sibling::*[contains(text(),"Dataset is shared via SMB as '{name}'")]'''


def share_attribute(sharetype: str, attribute: str, desc: str) -> str:
    """
    This method sets the text for the given share name

    :param sharetype: type of the given share
    :param attribute: attribute of the given share [name/path/description]
    :param desc: description of the given share
    :return: xpath string for given share name
    """
    index = 1
    if attribute == 'name':
        index = 1
    if attribute == 'path':
        index = 2
    if attribute == 'description':
        index = 3
    return f'//ix-{sharetype}-card//*[@data-test="row"]/td[{index}]/descendant::*[contains(text(),"{desc}")]'


def share_enabled_slider(sharetype: str, name: str) -> str:
    """
    This method sets the text for the given share name

    :param sharetype: type of the given share
    :param name: name of the given share
    :return: xpath string for given share name
    """
    return f'//ix-{sharetype}-card//*[contains(text(),"{name}")]/ancestor::tr/descendant::mat-slide-toggle//button'


def toggle_field(field: str) -> str:
    """
    This method sets the text for the given toggle field

    :param field: name of the given toggle field
    :return: xpath string for given toggle field
    """
    return f'//*[@data-test="toggle-{field}"]//button'
