import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.certificates import Certificates
from keywords.webui.navigation import Navigation


class Test_Deleting_Certificate:
    """
    Test class for deleting certificate.
    """

    @pytest.fixture(scope='function', autouse=True)
    def setup_and_teardown_test(self, data):
        """
        This method will be called once before all tests
        """
        if data['type'] == 'csr':
            API_POST.create_certificate_signing_requests(data)
        elif data['type'] == 'ca':
            API_POST.create_certificate_authority(data)
        else:
            ca_data = get_data_list('certificates')[1]
            ca_id = API_POST.create_certificate_authority(ca_data).json()['id']
            API_POST.create_certificate(data, ca_id)

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, data):
        yield
        if data['type'] == 'cert':
            ca_data = get_data_list('certificates')[1]
            API_DELETE.delete_certificate_authority(ca_data['name'])

    @pytest.mark.parametrize('data', get_data_list('certificates')[0:3])
    def test_deleting_certificate(self, data):
        """
        This method will delete the given certificate.
        """
        Navigation.navigate_to_certificates()
        assert Certificates.assert_certificates_page_header() is True
        assert Certificates.assert_certificate_name(data['card'], data['name']) is True
        Certificates.delete_certificate_by_name(data['type'], data['name'])
        assert Certificates.assert_certificate_name_deleted(data['card'], data['name']) is True
