import pytest
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


class Test_Dataset_Encryption:

    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self):
        """
        This setup fixture creates all datasets needed for the test class.
        """
        assert API_POST.create_encrypted_dataset('tank/tree').status_code == 200
        assert API_POST.create_inherit_encrypted_dataset('tank/tree/child').status_code == 200
        assert API_POST.create_encrypted_dataset('tank/tree/child/grandchild').status_code == 200

    def test_dataset_tree_encryption(self):
        """
        Verify that the dataset tree is expanded and the encryption icon is visible.
        """

        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

        assert Datasets.has_encryption('tank') is False
        Datasets.is_dataset_visible('tank-', 'tree')
        assert Datasets.has_encryption('tree') is True
        assert Common.assert_tree_is_expanded('tank-tree') is True
        Datasets.is_dataset_visible('tank-tree-', 'child')
        assert Datasets.has_encryption('child') is True
        assert Common.assert_tree_is_expanded('tank-tree-child') is True
        Datasets.is_dataset_visible('tank-tree-child-', 'grandchild')
        assert Datasets.has_encryption('grandchild') is True
        Datasets.lock_dataset('grandchild')
        Common.assert_tree_is_expanded('tank-tree')
        Common.assert_tree_is_expanded('tank-tree-child')

        assert Datasets.is_locked('tree') is False
        assert Datasets.is_locked('child') is False
        assert Datasets.is_locked('grandchild') is True

        Datasets.unlock_dataset('grandchild', 'encryption')

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test_class(self):
        """
        This teardown fixture deletes all datasets created for the test class.
        """
        yield
        assert API_DELETE.delete_dataset('tank/tree', recursive=True, force=True).status_code == 200
