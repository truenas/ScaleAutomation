import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
@allure.tag("SMB", "UI")
@allure.epic("Shares")
@allure.feature("SMB-UI")
class Test_SMB_UI:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, smb_data) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Shadow Copy functionality
        """
        # Environment setup
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])
        API_POST.create_dataset(smb_data['path'], 'SMB')
        API_POST.create_share('smb', smb_data['name'], '/mnt/'+smb_data['path'])
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('smb')
        if COMSHARE.is_share_service_running('smb'):
            COMSHARE.stop_share_service_by_actions_menu('smb')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, smb_data) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        yield
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])

    @allure.tag("Read")
    @allure.story("Verify SMB Card UI")
    def test_smb_share_card_ui(self, smb_data) -> None:
        """
        This test verifies the SMB Card UI
        """
        # Set Share Description
        COMSHARE.click_edit_share('smb', smb_data['name'])
        COMSHARE.set_share_description(smb_data['description'])
        COM.click_save_button()
        if COM.is_visible('//*[@data-test="button-do-not-start"]'):
            COM.click_button('do-not-start')

        # Verify Share Card Elements
        assert COMSHARE.assert_share_card_displays('smb')
        assert COMSHARE.assert_share_card_status('smb') is True
        assert COMSHARE.assert_share_card_add_button('smb') is True
        assert COMSHARE.assert_share_card_actions_menu_button('smb') is True
        assert COMSHARE.assert_share_card_actions_menu_dropdown('smb')
        assert COMSHARE.assert_share_card_table_header('smb') is True
        assert COMSHARE.assert_share_name('smb', smb_data['name']) is True
        assert COMSHARE.assert_share_path('smb', smb_data['path']) is True
        assert COMSHARE.assert_share_description('smb', smb_data['description']) is True
        assert COMSHARE.assert_share_card_enabled_button_by_name('smb', smb_data['name'])
        assert COMSHARE.assert_share_card_action_button_by_name('smb', smb_data['name'], 'share') is True
        assert COMSHARE.assert_share_card_action_button_by_name('smb', smb_data['name'], 'security') is True
        assert COMSHARE.assert_share_card_action_button_by_name('smb', smb_data['name'], 'edit') is True
        assert COMSHARE.assert_share_card_action_button_by_name('smb', smb_data['name'], 'delete') is True
