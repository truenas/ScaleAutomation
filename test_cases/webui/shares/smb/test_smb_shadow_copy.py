import allure
import pytest

from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.snapshots import Snapshots as SNAP
from keywords.webui.smb import SMB


@allure.tag("SMB", "Shadow Copy")
@allure.epic("Shares")
@allure.feature("SMB-Shadow-Copy")
class Test_SMB_Shadow_Copy:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Shadow Copy functionality
        """
        # Environment setup
        API_DELETE.delete_share('smb', 'SMBSHADOW')
        API_DELETE.delete_dataset('tank/SMBSHADOW')
        API_POST.create_non_admin_user('smbshadow', 'smbshadow Full', 'testing', 'True')
        API_POST.create_dataset('tank/SMBSHADOW', 'SMB')
        API_POST.create_share('smb', 'SMBSHADOW', '/mnt/tank/SMBSHADOW', True)
        NAV.navigate_to_local_users()
        LU.expand_user_by_full_name('smbshadow Full')
        LU.click_user_edit_button()
        LU.set_user_home_directory('/mnt/tank/SMBSHADOW')
        LU.set_user_create_home_directory_checkbox()
        COM.click_save_button_and_wait_for_progress_bar()
        API_POST.start_service('cifs')
        API_POST.start_service('ssh')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        yield
        API_POST.delete_all_dataset_snapshots("tank/SMBSHADOW")
        API_DELETE.delete_share('smb', "SMBSHADOW")
        API_DELETE.delete_dataset("tank/SMBSHADOW")
        API_DELETE.delete_user('smbshadow')

    @allure.tag("Update")
    @allure.story("Verify SMB Shadow Copy")
    def test_smb_user_can_shadow_copy(self) -> None:

        # setup test file and directory
        assert SMB.assert_user_can_put_file('keepme.txt', 'SMBSHADOW', 'smbshadow', 'testing') is True
        assert SMB.assert_user_can_put_directory('Documents', 'SMBSHADOW', 'smbshadow', 'testing') is True

        # Create Snapshot
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        SNAP.click_add_snapshot_button()
        SNAP.select_snapshot_dataset("tank/SMBSHADOW")
        COM.click_save_button()

        # Delete File and Directory
        assert SMB.assert_user_can_delete_file('keepme.txt', 'SMBSHADOW', 'smbshadow', 'testing') is True
        assert SMB.assert_user_can_delete_directory('Documents', 'SMBSHADOW', 'smbshadow', 'testing') is True

        # Verify File and Directory do not exist
        assert SMB.assert_file_exists('keepme.txt', 'SMBSHADOW', 'smbshadow', 'testing') is False
        assert SMB.assert_directory_exists('Documents', 'SMBSHADOW', 'smbshadow', 'testing') is False

        # Restore Snapshot - Shadow Copy
        SNAP.expand_snapshot_by_name('tank/SMBSHADOW')
        SNAP.click_rollback_button()
        SNAP.confirm_rollback_snapshot_dialog()
        COM.click_button('close')

        # Verify File and Directory exist (restored)
        assert SMB.assert_file_exists('keepme.txt', 'SMBSHADOW', 'smbshadow', 'testing') is True
        assert SMB.assert_directory_exists('Documents', 'SMBSHADOW', 'smbshadow', 'testing') is True
