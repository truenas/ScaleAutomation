import pytest
from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET


@pytest.mark.parametrize('app_data', get_data_list('apps'), scope='class')
class Test_Start_App:

    @staticmethod
    def verify_app_installed(app_data) -> None:
        """
        This method verifies the given app is installed

        :param app_data: test data listing different apps to iterate through
        """
        if Apps.is_app_installed(app_data['app-name']) is False:
            Apps.click_discover_apps()
            COM.set_search_field(app_data['app-name'])
            Apps.click_app(app_data['app-name'])
            Apps.click_install_app(app_data['app-name'])
            Apps.set_app_values(app_data['app-name'])
            COM.click_save_button()
            assert COM.assert_page_header('Installed', shared_config['LONG_WAIT'])
        assert Apps.is_app_installed(app_data['app-name']) is True
        assert Apps.is_app_deployed(app_data['app-name']) is True

    @staticmethod
    def verify_start_app(app_data) -> None:
        """
        This method verifies the given app is started

        :param app_data: test data listing different apps to iterate through
        """
        assert Apps.assert_stop_app(app_data['app-name'])
        assert Apps.assert_start_app(app_data['app-name'])

    @staticmethod
    def verify_teardown(app_data):
        """
        This method removes the given app

        :param app_data: test data listing different apps to iterate through
        """
        # reset the change
        Apps.delete_app(app_data['app-name'])
        assert Apps.is_app_installed(app_data['app-name']) is False
        if app_data['setup-name'] == 'webdav':
            DATASET.delete_dataset_by_api(f'{app_data['pool']}/{app_data['setup-name']}')

