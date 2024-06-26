import pytest

from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    API_POST.create_non_admin_user('sshuser', 'sshuser Full', 'testing')
    API_PUT.enable_user_all_sudo_commands_no_password('sshuser')
    API_PUT.enable_user_ssh_password('sshuser')
    API_POST.create_remote_non_admin_user('sshuser', 'sshuser Full', 'testing')

    API_DELETE.delete_dataset('tank/rsync-enc')
    API_DELETE.delete_dataset('tank/rsync-non')
    API_DELETE.delete_remote_dataset('tank/rsync-enc')
    WebUI.delay(2)
    API_POST.create_dataset('tank/rsync-non')
    API_POST.create_encrypted_dataset('tank/rsync-enc')
    API_POST.create_remote_encrypted_dataset('tank/rsync-enc')
    API_POST.set_dataset_permissions_user_and_group('tank/rsync-enc', 'sshuser', 'sshuser')
    API_POST.set_dataset_permissions_user_and_group('tank/rsync-non', 'sshuser', 'sshuser')
    API_POST.start_service('ssh')
    API_POST.start_remote_service('ssh')


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    API_DELETE.delete_user('sshuser')
    API_DELETE.delete_remote_user('sshuser')
    API_DELETE.delete_dataset('tank/rsync-enc')
    API_DELETE.delete_dataset('tank/rsync-non')
    API_DELETE.delete_remote_dataset('tank/rsync-enc')
    API_DELETE.delete_ssh_connection('rsync-non-to-enc')
    API_DELETE.delete_ssh_keypairs('rsync-non-to-enc')
    API_DELETE.delete_ssh_connection('rsync-loc-to-enc')
    API_DELETE.delete_ssh_keypairs('rsync-loc-to-enc')
