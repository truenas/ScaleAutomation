import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.put import API_PUT
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('role', get_data_list('datasets-roles')[:3], scope='class')
class Test_Dataset_Roles_Information:
    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset_by_role(role):
        """
        Create smb share or ix-applications dataset.
        """
        if role['dataset'] == "smb_share":
            assert Datasets.assert_share_role_dataset_exists() is True
        elif role['dataset'] == "ix-applications":
            assert API_PUT.set_app_pool('tank').status_code == 200

    @staticmethod
    def on_the_datasets_page_verify_dataset_role_information(role):
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(role['dataset'])
        assert Common.assert_text_is_visible(role['role name']) is True
        assert Common.assert_text_is_visible(role['role text']) is True
        assert Common.assert_text_is_visible(role['link text']) is True

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset_and_shares(role):
        """
        Delete smb share or ix-applications dataset.
        """
        yield
        if role['dataset'] == "smb_share":
            API_DELETE.delete_share('smb', 'smb_share')
            API_DELETE.delete_dataset('tank/smb_share')
        if role['dataset'] == "ix-applications":
            API_DELETE.delete_dataset('tank/ix-applications', recursive=True)
