from keywords.webui.common import Common as COM


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

