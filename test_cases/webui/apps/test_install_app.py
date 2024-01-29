import pytest
from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET


@pytest.mark.parametrize('app_data', get_data_list('apps'), scope='class')
class Test_Install_App:

    @staticmethod
    def set_app_ready_for_install(app_data):
        """
        This test finds the given app and gets it ready to install

        :param app_data: test data listing different apps to iterate through
        """
        if Apps.is_app_installed(app_data['app-name']) is True:
            Apps.delete_app(app_data['app-name'])
        Apps.click_discover_apps()
        COM.set_search_field(app_data['app-name'])
        Apps.click_app(app_data['app-name'])

    @staticmethod
    def verify_install_app(app_data):
        """
        This test installs the given app and verifies it installed

        :param app_data: test data listing different apps to iterate through
        """
        Apps.click_install_app(app_data['app-name'])
        Apps.set_app_values(app_data['app-name'])
        COM.click_save_button()
        assert COM.assert_page_header('Installed', shared_config['LONG_WAIT'])
        assert Apps.is_app_installed(app_data['app-name']) is True

    @staticmethod
    def verify_teardown(app_data) -> None:
        """
        This test removes the given app

        :param app_data: test data listing different apps to iterate through
        """
        # reset the change
        Apps.delete_app(app_data['app-name'])
        assert Apps.is_app_installed(app_data['app-name']) is False
        if app_data['setup-name'] == 'webdav':
            DATASET.delete_dataset_by_api(f'{app_data["pool"]}/{app_data["setup-name"]}')
