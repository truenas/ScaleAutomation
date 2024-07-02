import allure
from helper.webui import WebUI
from keywords.webui.navigation import Navigation
from keywords.webui.storage import Storage


@allure.tag('Storage Dashboard', 'Percy')
@allure.epic('Storage Dashboard')
@allure.feature('Storage Dashboard UI Verification')
class Test_Storage_Dashboard:

    @allure.tag('Read', 'Percy')
    @allure.story("Take Percy Snapshot of Storage Dashboard UI")
    def test_take_storage_dashboard_snapshot(self):
        """
        This method takes snapshot of storage dashboard UI.
        1. Navigate to storage dashboard
        2. Verify the tank pool exists in the storage dashboard
        3. Take a snapshot of storage dashboard UI
        """
        Navigation.navigate_to_storage()
        assert Storage.is_pool_name_header_visible('tank') is True
        WebUI.take_percy_snapshot('Storage Dashboard UI')
