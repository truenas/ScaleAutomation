
def cloud_sync_task_delete_button(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task delete button by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task delete button by the given cloud sync task description.
    """
    return f'//*[@data-test="button-card-cloudsync-task-{description}-delete-row-action"]'


def cloud_sync_task_description(description: str) -> str:
    """
    This function returns the xpath text of the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the given cloud sync task description.
    """
    return f'//*[@data-test="text-description-card-cloudsync-task-{description}-row-text"]'


def cloud_sync_task_dry_run_button(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task dry run button by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task dry run button by the given cloud sync task description.
    """
    return f'//*[@data-test="button-card-cloudsync-task-{description}-sync-row-action"]'


def cloud_sync_task_edit_button(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task edit button by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task edit button by the given cloud sync task description.
    """
    return f'//*[@data-test="button-card-cloudsync-task-{description}-edit-row-action"]'


def cloud_sync_task_enable_toggle(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task enable toggle by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task enable toggle by the given cloud cloud sync task description.
    """
    return f'//*[@data-test="toggle-enabled-card-cloudsync-task-{description}-row-toggle"]//button'


def cloud_sync_task_restore_button(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task restore button by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task restore button by the given cloud sync task description.
    """
    return f'//*[@data-test="button-card-cloudsync-task-{description}-restore-row-action"]'


def cloud_sync_task_run_now_button(description: str) -> str:
    """
    This function returns the xpath text of the cloud sync task run now button by the given cloud sync task description.

    :param description: The description of the cloud sync task.
    :return: The xpath text of the cloud sync task run now button by the given cloud sync task description.
    """
    return f'//*[@data-test="button-card-cloudsync-task-{description}-play-arrow-row-action"]'


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
