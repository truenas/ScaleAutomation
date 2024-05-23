
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
    :return: The xpath text of the cloud sync task enable toggle by the given cloud sync task description.
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


def periodic_snapshot_task_delete_button(path: str) -> str:
    """
    This function returns the xpath text delete button of the given periodic snapshot task path.

    :param path: The path of the periodic snapshot task.
    :return: The xpath text delete button of the given periodic snapshot task path.
    """
    return f'//*[contains(@data-test,"button-snapshot-task-{path}") and contains(@data-test,"-delete-row-action")]'


def periodic_snapshot_task_edit_button(path: str) -> str:
    """
    This function returns the xpath text edit button of the given periodic snapshot task path.

    :param path: The path of the periodic snapshot task.
    :return: The xpath text edit button of the given periodic snapshot task path.
    """
    return f'//*[contains(@data-test,"button-snapshot-task-{path}") and contains(@data-test,"-edit-row-action")]'


def periodic_snapshot_task_enable_toggle(path: str) -> str:
    """
    This function returns the xpath text of the periodic snapshot task enable toggle by the given periodic snapshot task path.

    :param path: The path of the periodic snapshot task.
    :return: The xpath text of the periodic snapshot task enable toggle by the given periodic snapshot task path.
    """
    return f'//*[contains(@data-test,"toggle-enabled-snapshot-task-{path}")]//button'


def periodic_snapshot_task_path(path: str) -> str:
    """
    This function returns the xpath text of the given periodic snapshot task path.

    :param path: The path of the periodic snapshot task.
    :return: The xpath text of the given periodic snapshot task path.
    """
    return f'//*[contains(@data-test,"text-pool-dataset-snapshot-task-{path}")]'


def replication_task_delete_button(name: str) -> str:
    """
    This function returns the xpath text of the given replication task name.

    :param name: The description of the replication task.
    :return: The xpath text of the given replication task name.
    """
    return f'//*[@data-test="button-replication-task-{name}-delete-row-action"]'


def replication_task_enable_toggle(name: str) -> str:
    """
    This function returns the xpath text of the replication task enable toggle by the given periodic snapshot task path.

    :param name: The name of the replication task.
    :return: The xpath text of the replication task enable toggle by the given replication task path.
    """
    return f'//*[contains(@data-test,"toggle-enabled-replication-task-{name}-row-toggle")]//button'


def replication_task_name(name: str) -> str:
    """
    This function returns the xpath text of the given replication task name.

    :param name: The description of the replication task.
    :return: The xpath text of the given replication task name.
    """
    return f'//*[@data-test="text-name-replication-task-{name}-row-text"]'


def replication_task_restore_button(name: str) -> str:
    """
    This function returns the xpath text of the given replication task name.

    :param name: The description of the replication task.
    :return: The xpath text of the given replication task name.
    """
    return f'//*[@data-test="button-replication-task-{name}-restore-row-action"]'


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


def smart_test_delete_button(description: str) -> str:
    """
    This function returns the xpath text of the smart task delete button by the given scrub task description.

    :param description: The description of the smart task.
    :return: The xpath text of the smart task delete button by the given scrub task description.
    """
    return f'//*[starts-with(@data-test,"text-description-smart-task") and contains(text(),"{description}")]/ancestor::tr/descendant::*[contains(@data-test,"-delete-row-action")]'


def smart_test_description(description: str) -> str:
    """
    This function returns the xpath text of the smart task edit button by the given smart task description.

    :param description: The description of the smart task.
    :return: The xpath text of the smart task edit button by the given smart task description.
    """
    return f'//*[starts-with(@data-test,"text-description-smart-task") and contains(text(),"{description}")]'


def smart_test_edit_button(description: str) -> str:
    """
    This function returns the xpath text of the smart task edit button by the given smart task description.

    :param description: The description of the smart task.
    :return: The xpath text of the smart task edit button by the given smart task description.
    """
    return f'//*[contains(text(),"{description}")]/ancestor::tr/descendant::*[contains(@data-test,"-edit-row-action")]'


def smart_test_page_delete_button_lock(description: str) -> str:
    """
    This function returns the xpath text of the smart test page delete button lock by the given smart test description.

    :param description: The description of the smart task.
    :return: The xpath text of the smart test page delete button lock by the given smart test description.
    """
    return f'//*[contains(text(),"{description}")]/ancestor::tr/descendant::*[contains(@data-test,"-delete-row-action")]/..//ix-icon[@name="lock"]'


def smart_test_page_link(title: str) -> str:
    """
    This function returns the xpath text of the smart task page link by the given smart task title.

    :param title: The description of the smart task.
    :return: The xpath text of the smart task page link by the given smart task title.
    """
    return f'//h3[contains(text(),"{title}")]'


def vm_periodic_snapshot_task_delete_button(path: str) -> str:
    """
    This function returns the xpath text delete button of the given vm periodic snapshot task path.

    :param path: The path of the periodic snapshot task.
    :return: The xpath text delete button of the given vm periodic snapshot task path.
    """
    #  TODO: fix this when UI available
    return f'//*[contains(@data-test,"button-vm-snapshot-task-{path}") and contains(@data-test,"-delete-row-action")]'
