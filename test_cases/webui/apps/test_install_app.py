import pytest
from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.apps import Apps


@pytest.mark.parametrize('app_data', get_data_list('apps'))
def test_install_app(app_data) -> None:
    NAV.navigate_to_apps()
    if Apps.is_app_installed(app_data['app-name']) is True:
        Apps.delete_app(app_data['app-name'])
    Apps.click_discover_apps()
    COM.set_search_field(app_data['app-name'])
    Apps.click_app(app_data['app-name'])

    # Install App
    Apps.click_install_app(app_data['app-name'])
    Apps.set_app_values(app_data['app-name'])
    COM.click_save_button()
    assert COM.assert_page_header('Installed', shared_config['LONG_WAIT'])
    assert Apps.is_app_installed(app_data['app-name']) is True
