import allure
import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.certificates import Certificates
from keywords.webui.navigation import Navigation


@allure.tag("Signing Certificate")
@allure.epic("Credentials")
@allure.feature("Certificates")
class Test_Signing_Certificates:

    @pytest.fixture(scope="function", autouse=True)
    def setup_test(self, data):
        """
        This fixture create the certificate authority and CSR for the test.
        """
        API_POST.create_certificate_authority(data)
        csr_data = get_data_list('certificates')[0]
        API_POST.create_certificate_signing_requests(csr_data)

    @pytest.fixture(scope="function", autouse=True)
    def tear_down_test(self, data):
        """ This fixture delete the certificate authority and CSR after the test."""
        yield
        API_DELETE.delete_certificate(data['csr_indentifier'])
        API_DELETE.delete_certificate_authority(data['name'])
        csr_data = get_data_list('certificates')[0]
        API_DELETE.delete_certificate(csr_data['name'])

    @pytest.mark.parametrize('data', get_data_list('certificates')[1:2])
    @allure.tag("Create")
    @allure.story("Sign A Certificate Authorities With A CSR")
    def test_sign_a_certificate_authorities_with_a_csr(self, data):
        """
        This test creates a certificate by signing a Certificate Authority with a CSR.
        """
        # Navigate to the Certificates page
        Navigation.navigate_to_certificates()
        Certificates.assert_certificates_page_header()

        # On a Certificate Authority, click on Sign CSR button.
        assert Certificates.assert_certificate_authorities_card_visible() is True
        Certificates.click_certificate_authorities_sign_csr_button_by_name(data['name'])

        # On the Sign CSR dialog, fill in the details and click on Sign CSR.
        assert Certificates.assert_sign_csr_dialog_visible() is True
        WebUI.delay(1)
        Certificates.select_csrs_option(data['csr_id'])
        Certificates.set_sign_csr_identifier(data['csr_indentifier'])
        Certificates.click_sign_csr_button()

        # Verify the created certificate details are visible on the Certificates page.
        assert Certificates.assert_certificate_name('Certificates', data['csr_indentifier']) is True
        assert Certificates.assert_certificate_issuer('Certificates', data['name']) is True
        assert Certificates.assert_certificate_cn('Certificates', data['common_name']) is True
        assert Certificates.assert_certificate_san('Certificates', data['san']) is True
