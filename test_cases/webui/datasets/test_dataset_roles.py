import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('role', get_data_list('datasets-roles')[:3], scope='class')
class Test_Dataset_Roles:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, role):
        """
        Create smb share or ix-applications dataset.
        """
        if role['dataset'] == "smb_share":
            API_POST.create_dataset(f"tank/{role['dataset']}", 'SMB')
            API_POST.create_share("smb", "smb_share", f"/mnt/tank/{role['dataset']}")
        elif role['dataset'] == "ix-applications":
            assert API_PUT.set_app_pool('tank').status_code == 200

    def test_dataset_roles_information(self, role):
        """
        This test verifies the dataset roles information is visible.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(role['dataset'])

        # Verify the dataset roles information
        assert Common.assert_text_is_visible(role['role name']) is True
        assert Common.assert_text_is_visible(role['role text']) is True
        assert Common.assert_text_is_visible(role['link text']) is True

    def test_dataset_roles_manage_links(self, role):
        """
        This test verifies the manage role link opens the correct page.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(role['dataset'])

        # Verify the manage role link
        Datasets.click_manage_role_link(role['link'])
        assert Common.assert_page_header(role['page header']) is True

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_class(self, role):
        """
        This tear down fixture delete smb share or ix-applications dataset.
        """
        yield
        if role['dataset'] == "smb_share":
            API_DELETE.delete_share('smb', 'smb_share')
            API_DELETE.delete_dataset('tank/smb_share')
        if role['dataset'] == "ix-applications":
            API_DELETE.delete_dataset('tank/ix-applications', recursive=True)
