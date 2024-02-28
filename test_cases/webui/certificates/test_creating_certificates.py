import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.certificates import Certificates
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


class Test_Creating_Certificate:
    """
    Test class for creating certificates
    """

    @pytest.fixture(scope="function", autouse=True)
    def tear_down_test(self, data):
        """
        This fixture deletes the dataset created for the test class.
        """
        yield
        API_DELETE.delete_certificate(data['name'])

    @pytest.mark.parametrize('data', get_data_list('certificates')[0:1])
    def test_creating_a_certificate_signing_requests(self, data):
        """
        This method creates a Certificate Signing Request with the given data
        and verify the created certificate details are visible on the Certificates page.
        """
        # Navigate to the Certificates page
        Navigation.navigate_to_certificates()
        assert Certificates.assert_certificates_page_header() is True

        # Click on the Add button on the Certificate Signing Requests card
        assert Certificates.assert_certificate_signing_requests_card_visible() is True
        Certificates.click_certificate_signing_requests_add_button()
        assert Certificates.assert_add_csr_side_panel_visible() is True

        # Fill the Identifier and Type step form and clink on the next button
        Common.assert_step_header_is_open('Identifier and Type')
        Certificates.set_name(data['name'])
        Certificates.select_profile_option(data['profile_option'])
        Certificates.click_identifier_and_type_next_button()

        # Fill the Certificate Options step form and clink on the next button
        assert Common.assert_step_header_is_open('Certificate Options') is True
        Certificates.select_key_type_option(data['key_type'])
        Certificates.select_key_length_option(data['key_length'])
        Certificates.click_certificate_options_next_button()

        # Fill the Certificate Subject step form and clink on the next button
        assert Common.assert_step_header_is_open('Certificate Subject') is True
        Certificates.select_country_option(data['country'])
        Certificates.set_state(data['state'])
        Certificates.set_locality(data['city'])
        Certificates.set_organization(data['organization'])
        Certificates.set_organizational_unit(data['organizational_unit'])
        Certificates.set_email(data['email'])
        Certificates.set_common_name(data['common_name'])
        Certificates.set_subject_alternative_name(data['san'])
        Certificates.click_certificate_subject_next_button()

        # Fill the Extra Constraints step form and clink on the next button
        assert Common.assert_step_header_is_open('Extra Constraints') is True
        Certificates.set_path_length(data['path_length'])
        Certificates.select_basic_constraints_config_option(data['config_option'])
        Certificates.click_extra_constraints_next_button()

        # Verify the Confirm Options step form and clink on the submit button
        assert Common.assert_step_header_is_open('Confirm Options') is True
        assert Certificates.assert_confirm_name_option_value(data['name']) is True
        assert Certificates.assert_confirm_type_option_value(data['confirm_type']) is True
        assert Certificates.assert_confirm_profile_option_value(data['confirm_profile']) is True
        assert Certificates.assert_confirm_key_type_option_value(data['confirm_key_type']) is True
        assert Certificates.assert_confirm_key_length_option_value(data['key_length']) is True
        assert Certificates.assert_confirm_digest_algorithm_option_value(data['confirm_digest_algorithm']) is True
        assert Certificates.assert_confirm_san_option_value(data['san']) is True
        assert Certificates.assert_confirm_common_name_option_value(data['common_name']) is True
        assert Certificates.assert_confirm_email_option_value(data['email']) is True
        assert Certificates.assert_confirm_subject_option_value(data['confirm_subject']) is True
        assert Certificates.assert_confirm_basic_constraints_option_value(data['confirm_basic_constraints']) is True
        assert Certificates.assert_confirm_extended_key_usage_option_value(data['confirm_extended_key_usage']) is True
        assert Certificates.assert_confirm_critical_extension_option_value(data['confirm_critical_extension']) is True
        assert Certificates.assert_confirm_key_usage_option_value(data['confirm_key_usage']) is True
        Common.click_save_button_and_wait_for_progress_bar()

        # Verify the new CSR information after the creation.
        assert Certificates.assert_certificate_name(data['card'], data['name']) is True
        assert Certificates.assert_certificate_issuer(data['card'], data['certificate_issuer']) is True
        assert Certificates.assert_certificate_cn(data['card'], data['common_name']) is True
        assert Certificates.assert_certificate_san(data['card'], data['san']) is True


