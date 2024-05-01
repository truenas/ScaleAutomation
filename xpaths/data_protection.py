
def scrub_task_description(description: str) -> str:
    """
    This function returns the xpath text of the given scrub task description.

    :param description: The description of the scrub task.
    :return: The xpath text of the given scrub task description.
    """
    return f'//*[starts-with(@data-test,"text-description-card-scrub-task-") and contains(@data-test,"{description}-row-text")]'


def scrub_task_delete_button(description: str) -> str:
    """
    This function returns the xpath text of the scrub task delete button by the given scrub task description.

    :param description: The description of the scrub task.
    :return: The xpath text of the scrub task delete button by the given scrub task description.
    """
    return f'//*[contains(@data-test,"{description}-delete-row-action")]'


def scrub_task_edit_button(description: str) -> str:
    """
    This function returns the xpath text of the scrub task edit button by the given scrub task description.

    :param description: The description of the scrub task.
    :return: The xpath text of the scrub task edit button by the given scrub task description.
    """
    return f'//*[contains(@data-test,"{description}-edit-row-action")]'


def scrub_task_enable_toggle(description: str) -> str:
    """
    This function returns the xpath text of the scrub task enable toggle by the given scrub task description.

    :param description: The description of the scrub task.
    :return: The xpath text of the scrub task enable toggle by the given scrub task description.
    """
    return f'//*[contains(@data-test,"{description}-row-toggle")]//button'
