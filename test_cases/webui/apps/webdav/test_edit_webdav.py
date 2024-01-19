import pytest

from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET


class Test_Edit_Webdav:

    @staticmethod
    def test_edit_app() -> None:
        """
        This method verifies the app can be edited
        """
        assert Apps.verify_app_installed('WebDAV')
        Apps.edit_app('WebDAV')
        COM.unset_checkbox('http')
        COM.set_checkbox('https')
        COM.set_input_field('certificate-id', "")
        COM.click_on_element('//*[contains(text(),"\'truenas_default\' Certificate")]')
        COM.set_input_field('https-port', '30035')
        COM.click_save_button()
        assert COM.assert_page_header('Installed')
        assert Apps.is_app_running('WebDAV')

    @staticmethod
    def verify_edit_values() -> None:
        """
        This test verifies the edited values of the app
        """
        Apps.edit_app('WebDAV')
        assert not COM.is_checked('http')
        assert COM.is_checked('https')
        assert COM.get_element_property('certificate-id') == "'truenas_default' Certificate"
        assert COM.get_element_property('https-port') == '30035'
        COM.click_link('breadcrumb-applications')

    @staticmethod
    def verify_teardown() -> None:
        """
        This test removes the given app
        """
        # reset the change
        Apps.delete_app('WebDAV')
        assert Apps.is_app_installed('WebDAV') is False
        DATASET.delete_dataset_by_api('tank/webdav')
