import allure
import pytest

from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


@allure.tag("Apps", "WebDAV")
@allure.epic("Apps")
@allure.feature("Apps-Edit")
class Test_Edit_Webdav:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        """
        This method sets up Dataset and WebDAV app for test
        """
        API_POST.create_dataset('tank/webdav')
        assert Apps.verify_app_installed('WebDAV') is True

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This method clears any Apps and Datasets after test is run for a clean environment
        """
        yield
        # Clean up environment.
        Apps.delete_app('WebDAV')
        assert Apps.is_app_installed('WebDAV') is False
        API_DELETE.delete_dataset('tank/webdav')

    @allure.tag("Update")
    @allure.story("Edit App WebDAV values")
    def test_edit_webdav_app(self):
        """
        This method verifies the webdav app can be edited
        """
        # edit app initial values
        Apps.edit_app('WebDAV')
        COM.unset_checkbox('http')
        COM.set_checkbox('https')
        COM.set_input_field('certificate-id', "")
        COM.click_on_element('//*[contains(text(),"\'truenas_default\' Certificate")]')
        COM.set_input_field('https-port', '30035')
        COM.click_save_button()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WebDAV') is True

        # verify edited app values
        Apps.edit_app('WebDAV')
        assert not COM.is_checked('http') is True
        assert COM.is_checked('https') is True
        assert COM.get_input_property('certificate-id') == "'truenas_default' Certificate"
        assert COM.get_input_property('https-port') == '30035'
        COM.click_link('breadcrumb-applications')
