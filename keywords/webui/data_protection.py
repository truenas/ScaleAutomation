import xpaths
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class Data_Protection:

    @classmethod
    def click_add_replication_button(cls) -> None:
        """
        This method clicks the Add Replication task button

        Example:
            - Data_Protection.click_Add_Replication_button()
        """
        COM.click_button('replication-task-add')

    @classmethod
    def click_snapshots_button(cls):
        """
        This method clicks the Snapshots button

        Example:
            - Data_Protection.click_snapshots_button()
        """
        COM.click_link('snapshot-task-snapshots')

    @classmethod
    def delete_all_periodic_snapshot_tasks(cls) -> None:
        """
        This method deletes all the Periodic Snapshot tasks

        Example:
            - Data_Protection.delete_all_periodic_snapshot_tasks()
        """
        while COM.is_visible('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]'):
            COM.click_on_element('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]')
            COM.assert_confirm_dialog()
        assert COM.is_visible('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]') is False

    @classmethod
    def delete_all_snapshots(cls):
        """
        This method deletes all the Snapshots

        Example:
            - Data_Protection.delete_all_snapshots()
        """
        if COM.assert_page_header('Snapshots') is False:
            NAV.navigate_to_periodic_snapshots()
        COM.set_checkbox('column-select-all')
        if COM.is_visible(xpaths.common_xpaths.button_field('delete-selected')) is True:
            COM.click_button('delete-selected')
            COM.set_checkbox('confirm')
            COM.click_button('delete')
            # delay to allow delete to complete
            assert COM.is_visible(xpaths.common_xpaths.button_field('close')) is True
            COM.click_button('close')
            COM.assert_text_is_visible('No records have been added yet')
        assert COM.assert_text_is_visible('No records have been added yet')
