import xpaths
from helper.reporting import take_screenshot, create_timestamp
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Navigation:
    @classmethod
    def navigate_to(cls, location: str, header: str, location2: str = "") -> None:
        """
        This method navigates to the given location and verifies the given page header displays

        :param location: location to be navigating too
        :param header: header of the page being navigated too
        :param location2: second level location to be navigating too

        Example
         - Navigation.navigate_to('myLocation', 'My Location')
         - Navigation.navigate_to('myLocation', 'My Location2', 'my-second-location')
        """
        if COM.is_visible(xpaths.common_xpaths.close_right_panel()):
            print('@@@@@@@ RIGHT_PANEL_OPEN-'+create_timestamp())
            take_screenshot('RIGHT_PANEL_OPEN-'+create_timestamp())
            COM.close_right_panel()
        if COM.is_visible(xpaths.common_xpaths.button_field('dialog-cancel')):
            print('@@@@@@@ DIALOG_LEFT_OPEN-'+create_timestamp())
            take_screenshot('DIALOG_LEFT_OPEN-'+create_timestamp())
            COM.cancel_confirm_dialog()
        if COM.is_visible(xpaths.common_xpaths.button_field('cancel')):
            # This is used on datasets permissions preset dialogs
            print('@@@@@@@ DIALOG_LEFT_OPEN-'+create_timestamp())
            take_screenshot('DIALOG_LEFT_OPEN-'+create_timestamp())
            COM.click_cancel_button()
        if COM.is_visible(xpaths.common_xpaths.button_field('close-error-dialog')):
            print('@@@@@@@ DIALOG_LEFT_OPEN-' + create_timestamp())
            take_screenshot('DIALOG_LEFT_OPEN-' + create_timestamp())
            COM.click_error_dialog_close_button()
            COM.click_button('close')
        if (COM.is_visible(xpaths.common_xpaths.any_header(header, 1)) is True) & (header != 'Dashboard'):
            cls.navigate_to_dashboard()
        COM.click_on_element(xpaths.common_xpaths.link_field(location + '-menu'))
        if location2 != "":
            WebUI.delay(0.2)
            COM.click_on_element(xpaths.common_xpaths.any_xpath(f'(//*[@data-test="link-{location2}"])[2]'))
        assert COM.assert_page_header(header)
        WebUI.delay(2)

    @classmethod
    def navigate_to_apps(cls) -> None:
        """
        This method navigates to the Dashboard page

        Example
         - Navigation.navigate_to_apps()
        """
        cls.navigate_to('apps', 'Installed')

    @classmethod
    def navigate_to_backup_credentials(cls) -> None:
        """
        This method navigates to the Shares page

        Example
         - Navigation.navigate_to_backup_credentials()
        """
        cls.navigate_to('credentials', 'Backup Credentials', 'backup-credentials')

    @classmethod
    def navigate_to_certificates(cls) -> None:
        """
        This method navigates to the Shares page

        Example
         - Navigation.navigate_to_certificates()
        """
        cls.navigate_to('credentials', 'Certificates', 'certificates')

    @classmethod
    def navigate_to_dashboard(cls) -> None:
        """
        This method navigates to the Dashboard page

        Example
         - Navigation.navigate_to_dashboard()
        """
        cls.navigate_to('dashboard', 'Dashboard')

    @classmethod
    def navigate_to_data_protection(cls) -> None:
        """
        This method navigates to the Data Protection page

        Example
         - Navigation.navigate_to_data_protection()
        """
        cls.navigate_to('data-protection', 'Data Protection')

    @classmethod
    def navigate_to_datasets(cls) -> None:
        """
        This method navigates to the Shares page

        Example
         - Navigation.navigate_to_datasets()
        """
        cls.navigate_to('datasets', 'Datasets')
        assert COM.assert_progress_bar_not_visible() is True

    @classmethod
    def navigate_to_directory_services(cls) -> None:
        """
        This method navigates to the Shares page

        Example
         - Navigation.navigate_to_directory_services()
        """
        cls.navigate_to('credentials', 'Directory Services', 'directory-services')

    @classmethod
    def navigate_to_local_groups(cls) -> None:
        """
        THis method navigates to the Local Groups page.

        Example
         - Navigation.navigate_to_local_groups()
        """
        cls.navigate_to('credentials', 'Groups', 'local-groups')

    @classmethod
    def navigate_to_local_users(cls) -> None:
        """
        THis method navigates to the Local Users page.

        Example
         - Navigation.navigate_to_local_users()
        """
        cls.navigate_to('credentials', 'Users', 'local-users')

    @classmethod
    def navigate_to_periodic_snapshots(cls) -> None:
        """
        THis method navigates to the Periodic Snapshots page.

        Example
         - Navigation.navigate_to_periodic_snapshots()
        """
        cls.navigate_to_data_protection()
        assert WebUI.wait_until_visible(xpaths.common_xpaths.link_field('snapshot-task-snapshots')) is True
        COM.click_link('snapshot-task-snapshots')
        assert COM.assert_page_header('Snapshots')

    @classmethod
    def navigate_to_shares(cls) -> None:
        """
        This method navigates to the Shares page

        Example
         - Navigation.navigate_to_shares()
        """
        cls.navigate_to('shares', 'Sharing')

    @classmethod
    def navigate_to_storage(cls) -> None:
        """
        THis method navigates to the Storage page.

        Example
         - Navigation.navigate_to_storage()
        """
        cls.navigate_to('storage', 'Storage')

    @classmethod
    def navigate_to_system_settings_advanced(cls) -> None:
        """
        This method navigates to the Advanced page under the System Settings panel.

        Example
         - Navigation.navigate_to_system_settings_services()
        """
        cls.navigate_to('system-settings', 'Advanced', 'advanced')

    @classmethod
    def navigate_to_system_settings_general(cls) -> None:
        """
        This method navigates to the General page under the System Settings panel.

        Example
         - Navigation.navigate_to_system_settings_general()
        """
        cls.navigate_to('system-settings', 'General', 'general')

    @classmethod
    def navigate_to_system_settings_services(cls) -> None:
        """
        This method navigates to the Services page under the System Settings panel.

        Example
         - Navigation.navigate_to_system_settings_services()
        """
        cls.navigate_to('system', 'Services', 'services')
