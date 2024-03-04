import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.api.delete import API_DELETE
from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


@allure.tag("Apps")
@allure.epic("Apps")
@allure.feature("Apps-General")
@pytest.mark.parametrize('app_data', get_data_list('apps'), scope='class')
class Test_App:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, app_data):
        """
        This test finds the given app and installs it

        :param app_data: test data listing different apps to iterate through
        """
        assert Apps.verify_app_installed(app_data['app-name']) is True

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, app_data):
        """
        This method deletes any Apps and Datasets after test is run for a clean environment
        """
        yield
        # Clean up environment.
        Apps.delete_app(app_data['app-name'])
        assert Apps.is_app_installed(app_data['app-name']) is False
        if app_data['setup-name'] == 'webdav':
            API_DELETE.delete_dataset(f'{app_data["pool"]}/{app_data["setup-name"]}')

    @allure.tag("Create", "Install")
    @allure.story("Install App")
    def test_install_app(self, app_data):
        """
        This method verifies the app can be installed
        """
        # install app
        if Apps.is_app_installed(app_data['app-name']) is True:
            Apps.delete_app(app_data['app-name'])
        Apps.click_discover_apps()
        COM.set_search_field(app_data['app-name'])
        Apps.click_app(app_data['app-name'])
        Apps.click_install_app(app_data['app-name'])
        Apps.set_app_values(app_data['app-name'])
        COM.click_save_button()
        Apps.handle_docker_limit_dialog()
        assert COM.assert_page_header('Installed', shared_config['LONG_WAIT']) is True
        assert Apps.is_app_installed(app_data['app-name']) is True

    @allure.tag("Delete", "Uninstall")
    @allure.story("Uninstall App")
    def test_uninstall_app(self, app_data):
        """
        This method verifies the app can be uninstalled
        """
        # uninstall app
        Apps.delete_app(app_data['app-name'])
        assert Apps.is_app_installed(app_data['app-name']) is False

    @allure.tag("Update", "Stop")
    @allure.story("Stop App")
    def test_stop_app(self, app_data):
        """
        This method verifies the app can be stopped
        """
        # stop app
        assert Apps.assert_start_app(app_data['app-name']) is True
        assert Apps.assert_stop_app(app_data['app-name']) is True

    @allure.tag("Update", "Start")
    @allure.story("Start App")
    def test_start_app(self, app_data):
        """
        This method verifies the app can be started
        """
        # start app
        assert Apps.assert_stop_app(app_data['app-name']) is True
        assert Apps.assert_start_app(app_data['app-name']) is True
