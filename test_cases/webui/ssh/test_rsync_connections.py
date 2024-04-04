import allure
import pytest

from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.ssh.common import Common_SSH as SSHCOM
from keywords.webui.common import Common as COM
from keywords.webui.common_replication import Common_Replication as COMREP
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.rsync import Rsync as RSYNC
from keywords.webui.ssh_connection import SSH_Connection as SSH


@allure.tag("Rsync_Connections")
@allure.epic("Data Protection")
@allure.feature("Rsync")
class Test_Rsync:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method sets up each test to start with datasets and services to execute Rsync functionality
        """
        # verify file does not exist in remote dataset
        SSH_Command_Line('sudo rm -rf /mnt/tank/rsync-enc/',
                         private_config['REP_DEST_IP'], 'sshuser', 'testing')
        response = SSH_Command_Line('ls -al /mnt/tank/rsync-enc/',
                                    private_config['REP_DEST_IP'], 'sshuser', 'testing')
        assert response.stdout.__contains__('newfile.txt') is False

        # delete task if already exists
        NAV.navigate_to_data_protection()
        if RSYNC.is_rsync_task_visible('/mnt/tank/rsync-enc') is True:
            RSYNC.delete_rsync_task_by_path('/mnt/tank/rsync-enc')
        if RSYNC.is_rsync_task_visible('/mnt/tank/rsync-non') is True:
            RSYNC.delete_rsync_task_by_path('/mnt/tank/rsync-non')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        this method clears any test ssh connections and keypairs after test is run for a clean environment
        """
        yield
        # Clean up environment.
        NAV.navigate_to_data_protection()
        RSYNC.delete_rsync_task_by_path('tank/rsync-enc')
        RSYNC.delete_rsync_task_by_path('tank/rsync-non')

    @allure.tag("Create")
    @allure.story("Create a Rsync Task from non-encrypted to encrypted-locked")
    def test_create_rsync_non_to_encrypted_locked(self) -> None:
        """
        This test verifies Rsync Task from non-encrypted to encrypted-locked fails
        """
        # add connection and key pair if they don't already exist
        API_POST.lock_remote_dataset('tank/rsync-enc')
        NAV.navigate_to_backup_credentials()
        assert SSH.assert_ssh_connection_exists('rsync-non-to-enc') is True

        NAV.navigate_to_data_protection()
        DP.click_add_rsync_button()

        RSYNC.set_path('/mnt/tank/rsync-non')
        RSYNC.set_rsync_mode_ssh()
        RSYNC.set_user(private_config["USERNAME"])
        RSYNC.set_connect_using_keychain()
        RSYNC.set_ssh_connection('rsync-non-to-enc')
        COMREP.set_direction_push()
        RSYNC.set_remote_path('/mnt/tank/rsync-enc')
        RSYNC.set_description('rsync-non-to-enc')
        RSYNC.set_schedule_weekly()
        COM.click_save_button()

        # add file to local dataset
        SSHCOM.add_test_file('/mnt/tank/rsync-non/newfile.txt', private_config['IP'],
                             'sshuser', 'testing')
        response = SSHCOM.list_directory('/mnt/tank/rsync-non', private_config['IP'],
                                         'sshuser', 'testing')
        assert response.__contains__('newfile.txt')

        # verify file does not exist on remote dataset
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc', private_config['REP_DEST_IP'],
                                         'sshuser', 'testing')
        assert not response.__contains__('newfile.txt')
        RSYNC.click_run_now_rsync_task_by_path('/mnt/tank/rsync-non')

        # verify task fails
        assert RSYNC.get_rsync_status('/mnt/tank/rsync-non') == 'FAILED'
        API_POST.unlock_remote_dataset('tank/rsync-enc')

    @allure.tag("Create")
    @allure.story("Create a Rsync Task from non-encrypted to encrypted-unlocked")
    def test_create_rsync_non_to_encrypted_unlocked(self) -> None:
        """
        This test verifies Rsync Task from non-encrypted to encrypted-unlocked passes
        """
        # add connection and key pair if they don't already exist
        NAV.navigate_to_backup_credentials()
        assert SSH.assert_ssh_connection_exists('rsync-non-to-enc') is True

        NAV.navigate_to_data_protection()
        DP.click_add_rsync_button()

        RSYNC.set_path('/mnt/tank/rsync-non')
        RSYNC.set_rsync_mode_ssh()
        RSYNC.set_user(private_config["USERNAME"])
        RSYNC.set_connect_using_keychain()
        RSYNC.set_ssh_connection('rsync-non-to-enc')
        COMREP.set_direction_push()
        RSYNC.set_remote_path('/mnt/tank/rsync-enc')
        RSYNC.set_description('rsync-non-to-enc')
        RSYNC.set_schedule_weekly()
        COM.click_save_button()

        # add file to local dataset
        SSHCOM.add_test_file('/mnt/tank/rsync-non/newfile.txt', private_config['IP'],
                             'sshuser', 'testing')
        response = SSHCOM.list_directory('/mnt/tank/rsync-non', private_config['IP'],
                                         'sshuser', 'testing')
        assert response.__contains__('newfile.txt')
        checksum = SSHCOM.get_file_checksum('/mnt/tank/rsync-non/newfile.txt', 'sshuser', 'testing')

        # verify file does not exist on remote dataset
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc', private_config['REP_DEST_IP'],
                                         'sshuser', 'testing')
        assert not response.__contains__('newfile.txt')
        RSYNC.click_run_now_rsync_task_by_path('/mnt/tank/rsync-non')
        assert RSYNC.get_rsync_status('/mnt/tank/rsync-non') == 'SUCCESS'
        # verify file does exist on remote dataset
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc/rsync-non', private_config['REP_DEST_IP'],
                                         'sshuser', 'testing')
        assert response.__contains__('newfile.txt')
        assert SSHCOM.get_remote_file_checksum('/mnt/tank/rsync-enc/rsync-non/newfile.txt', 'sshuser', 'testing') == checksum

    @allure.tag("Create")
    @allure.story("Create a Rsync Task from encrypted-locked to encrypted-unlocked")
    def test_create_rsync_encrypted_locked_to_encrypted_unlocked(self) -> None:
        """
        This test verifies Rsync Task from encrypted-locked to encrypted-unlocked passes
        """
        # add connection and key pair if they don't already exist
        NAV.navigate_to_backup_credentials()
        assert SSH.assert_ssh_connection_exists('rsync-non-to-enc') is True

        NAV.navigate_to_data_protection()
        DP.click_add_rsync_button()

        RSYNC.set_path('/mnt/tank/rsync-enc')
        RSYNC.set_rsync_mode_ssh()
        RSYNC.set_user(private_config["USERNAME"])
        RSYNC.set_connect_using_keychain()
        RSYNC.set_ssh_connection('rsync-non-to-enc')
        COMREP.set_direction_push()
        RSYNC.set_remote_path('/mnt/tank/rsync-enc')
        RSYNC.set_description('rsync-non-to-enc')
        RSYNC.set_schedule_weekly()
        COM.click_save_button()

        # add file to local dataset
        SSHCOM.add_test_file('/mnt/tank/rsync-enc/newfile.txt', private_config['IP'],
                             'sshuser', 'testing')
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc', private_config['IP'],
                                         'sshuser', 'testing')
        assert response.__contains__('newfile.txt')
        checksum = SSHCOM.get_file_checksum('/mnt/tank/rsync-enc/newfile.txt', 'sshuser', 'testing')

        # verify file does not exist on remote dataset
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc', private_config['REP_DEST_IP'],
                                         'sshuser', 'testing')
        assert not response.__contains__('newfile.txt')
        RSYNC.click_run_now_rsync_task_by_path('/mnt/tank/rsync-enc')
        assert RSYNC.get_rsync_status('/mnt/tank/rsync-enc') == 'SUCCESS'
        # verify file does on remote dataset
        response = SSHCOM.list_directory('/mnt/tank/rsync-enc/rsync-enc', private_config['REP_DEST_IP'],
                                         'sshuser', 'testing')
        assert response.__contains__('newfile.txt')
        assert SSHCOM.get_remote_file_checksum('/mnt/tank/rsync-enc/rsync-enc/newfile.txt', 'sshuser', 'testing') == checksum
