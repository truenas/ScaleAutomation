import pytest
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


class Test_Dataset_Tree:
    """
    Test class for dataset tree testing.
    """

    @pytest.fixture(scope='function')
    def setup_test_class(self):
        assert API_POST.create_dataset('tank/tree').status_code == 200
        assert API_POST.create_dataset('tank/tree/child').status_code == 200
        assert API_POST.create_dataset('tank/tree/child/grandchild').status_code == 200

    @pytest.fixture(scope='function')
    def setup_tree_role_test(self):
        API_POST.create_dataset('tank/smb_share', 'SMB')
        API_POST.create_share('smb', 'smb_share', '/mnt/tank/smb_share')
        assert API_PUT.set_app_pool('tank').status_code == 200

    def test_dataset_tree_expandable(self, setup_test_class, tear_down_class):
        """
        This test verify that the dataset tree is expandable.
        """
        # Navigate to the Datasets page
        Navigation.navigate_to_datasets()

        # Verify that the dataset tree is expandable
        assert Common.assert_tree_is_expanded('tank') is True
        assert Common.assert_tree_is_expanded('tank-tree') is True
        assert Common.assert_tree_is_expanded('tank-tree-child') is True

    def test_dataset_tree_list(self, setup_test_class, tear_down_class):
        """
        This test verify that the dataset is visible in the tree list.
        """
        # Navigate to the Datasets page
        Navigation.navigate_to_datasets()

        # Verify Dataset main pool (tank) is in list of Datasets
        assert Datasets.is_dataset_visible('', 'tank') is True
        # Verify Dataset 2nd pool (tree) is in list of Datasets
        assert Common.assert_tree_is_expanded('tank-tree') is True
        assert Datasets.is_dataset_visible('tank-', 'tree') is True
        # Verify Dataset child (child) is in list of Datasets
        assert Common.assert_tree_is_expanded('tank-tree-child') is True
        assert Datasets.is_dataset_visible('tank-tree-', 'child') is True
        # Verify Dataset grandchild (grandchild) is in list of Datasets
        assert Datasets.is_dataset_visible('tank-tree-child-', 'grandchild') is True

    def test_dataset_tree_roles(self, setup_tree_role_test, tear_down_tree_roles_test):
        """
        This test verify that the dataset roles are visible.
        """
        # Navigate to the Dataset page
        Navigation.navigate_to_datasets()
        assert Datasets.has_role_system('tank') is True
        assert Datasets.has_role_share('tank') is True
        assert Datasets.has_role_apps('ix-applications') is True
        assert Datasets.has_role_smb_share('smb_share') is True

    def test_dataset_tree_storage(self):
        Navigation.navigate_to_datasets()

        assert Datasets.get_dataset_size_usage_by_type('tank', 'USED') != ""
        assert Datasets.get_dataset_size_usage_by_type('tank', 'AVAILABLE') != ""

    @pytest.fixture(scope='function')
    def tear_down_class(self):
        """
        This teardown fixture deletes all datasets created for the test class.
        """
        yield
        assert API_DELETE.delete_dataset('tank/tree', recursive=True, force=True).status_code == 200

    @pytest.fixture(scope='function')
    def tear_down_tree_roles_test(self):
        """
        This teardown fixture deletes smb share and ix-applications dataset.
        """
        yield
        API_DELETE.delete_share('smb', 'smb_share')
        API_DELETE.delete_dataset('tank/smb_share')
        API_DELETE.delete_dataset('tank/ix-applications', recursive=True)
