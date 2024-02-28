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
    def setup_test(self, data):
        """
        This fixture creates a dataset for the test class.
        """
        if data['type'] == 'cert':
            ca_data = get_data_list('certificates')[1]
            API_POST.create_certificate_authority(ca_data)

    @pytest.fixture(scope="function", autouse=True)
    def tear_down_test(self, data):
        """
        This fixture deletes the datasets created by and for the test class.
        """
        yield
        if data['type'] == 'ca':
            API_DELETE.delete_certificate_authority(data['name'])
        else:
            API_DELETE.delete_certificate(data['name'])
            if data['type'] == 'cert':
                ca_data = get_data_list('certificates')[1]
                API_DELETE.delete_certificate_authority(ca_data['name'])

    @pytest.mark.parametrize('data', get_data_list('certificates')[2:3])
    def test_creating_a_certificate(self, data):
        # Navigate to the Certificates page
        Navigation.navigate_to_certificates()
        assert Certificates.assert_certificates_page_header() is True

        # Click on the Add button on the Certificate Authorities card
        assert Certificates.assert_certificates_card_visible() is True
        Certificates.click_certificates_add_button()
        assert Certificates.assert_add_certificate_side_panel_visible() is True

        # Fill the Identifier and Type step form and clink on the next button
        assert Common.assert_step_header_is_open('Identifier and Type') is True
        Certificates.set_name(data['name'])
        Certificates.select_certificates_type_option(data['option_type'])
        Certificates.select_profile_option(data['profile_option'])
        Certificates.click_identifier_and_type_next_button()

        # Fill the Certificate Options step form and clink on the next button
        assert Common.assert_step_header_is_open('Certificate Options') is True
        Certificates.select_signing_certificate_authority_option(data['signing_certificate_authority'])
        Certificates.select_key_type_option(data['key_type'])
        Certificates.select_ec_curve_option(data['ec_curve'])
        Certificates.select_digest_algorithm_option(data['algorithm'])
        Certificates.set_lifetime(int(data['lifetime']))
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
        Certificates.set_path_length(int(data['path_length']))
        Certificates.select_basic_constraints_config_option(data['config_option'])
        Certificates.set_authority_key_identifier_checkbox()
        Certificates.set_critical_extension()
        Certificates.click_extra_constraints_next_button()

        # Verify the Confirm Options step form and clink on the submit button
        assert Common.assert_step_header_is_open('Confirm Options') is True
        Certificates.assert_confirm_name_option_value(data['name'])
        Certificates.assert_confirm_type_option_value(data['confirm_type'])
        Certificates.assert_confirm_profile_option_value(data['confirm_profile'])
        Certificates.assert_confirm_signing_certificate_authority_option_value(data['confirm_sca'])
        Certificates.assert_confirm_key_type_option_value(data['confirm_key_type'])
        Certificates.assert_confirm_ec_curve_option_value(data['confirm_ec_curve'])
        Certificates.assert_confirm_digest_algorithm_option_value(data['confirm_digest_algorithm'])
        Certificates.assert_confirm_lifetime_option_value(data['lifetime'])
        Certificates.assert_confirm_san_option_value(data['san'])
        Certificates.assert_confirm_common_name_option_value(data['common_name'])
        Certificates.assert_confirm_email_option_value(data['email'])
        Certificates.assert_confirm_subject_option_value(data['confirm_subject'])
        Certificates.assert_confirm_basic_constraints_option_value(data['confirm_basic_constraints'])
        Certificates.assert_confirm_path_length_option_value(data['path_length'])
        Certificates.assert_confirm_authority_key_identifier_option_value(data['confirm_authority_key_id'])
        Certificates.assert_confirm_extended_key_usage_option_value(data['confirm_extended_key_usage'])
        Certificates.assert_confirm_critical_extension_option_value(data['confirm_critical_extension'])
        Certificates.assert_confirm_key_usage_option_value(data['confirm_key_usage'])
        Common.click_save_button_and_wait_for_progress_bar()

        # Verify the created certificate details are visible on the Certificates page
        assert Certificates.assert_certificate_name(data['card'], data['name']) is True
        assert Certificates.assert_certificate_issuer(data['card'], data['certificate_issuer']) is True
        assert Certificates.assert_certificate_cn(data['card'], data['common_name']) is True
        assert Certificates.assert_certificate_san(data['card'], data['san']) is True

    @pytest.mark.parametrize('data', get_data_list('certificates')[1:2])
    def test_creating_a_certificate_authority(self, data):
        """
        This test creates a Certificate Authority with the given data
        and verify the created certificate details are visible on the Certificates page.
        """
        # Navigate to the Certificates page
        Navigation.navigate_to_certificates()
        assert Certificates.assert_certificates_page_header() is True

        # Click on the Add button on the Certificate Authorities card
        assert Certificates.assert_certificate_authorities_card_visible() is True
        Certificates.click_certificate_authorities_add_button()
        assert Certificates.assert_add_certificate_authority_side_panel_visible() is True

        # Fill the Identifier and Type step form and clink on the next button
        assert Common.assert_step_header_is_open('Identifier and Type') is True
        Certificates.set_name(data['name'])
        Certificates.select_certificates_type_option(data['option_type'])
        Certificates.select_profile_option(data['profile_option'])
        Certificates.click_identifier_and_type_next_button()

        # Fill the Certificate Options step form and clink on the next button
        assert Common.assert_step_header_is_open('Certificate Options') is True
        Certificates.select_key_type_option(data['key_type'])
        Certificates.select_ec_curve_option(data['ec_curve'])
        Certificates.select_digest_algorithm_option(data['algorithm'])
        Certificates.set_lifetime(int(data['lifetime']))
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
        Certificates.set_path_length(int(data['path_length']))
        Certificates.set_authority_key_identifier_checkbox()
        Certificates.select_authority_key_config_option(data['authority_key_config'])
        Certificates.set_critical_extension()
        Certificates.click_extra_constraints_next_button()

        # Verify the Confirm Options step form and clink on the submit button
        assert Common.assert_step_header_is_open('Confirm Options') is True
        Certificates.assert_confirm_name_option_value(data['name'])
        Certificates.assert_confirm_type_option_value(data['confirm_type'])
        Certificates.assert_confirm_profile_option_value(data['confirm_profile'])
        Certificates.assert_confirm_key_type_option_value(data['confirm_key_type'])
        Certificates.assert_confirm_ec_curve_option_value(data['confirm_ec_curve'])
        Certificates.assert_confirm_digest_algorithm_option_value(data['confirm_digest_algorithm'])
        Certificates.assert_confirm_lifetime_option_value(data['lifetime'])
        Certificates.assert_confirm_san_option_value(data['san'])
        Certificates.assert_confirm_common_name_option_value(data['common_name'])
        Certificates.assert_confirm_email_option_value(data['email'])
        Certificates.assert_confirm_subject_option_value(data['confirm_subject'])
        Certificates.assert_confirm_basic_constraints_option_value(data['confirm_basic_constraints'])
        Certificates.assert_confirm_path_length_option_value(data['path_length'])
        Certificates.assert_confirm_authority_key_identifier_option_value(data['confirm_authority_key_id'])
        Certificates.assert_confirm_extended_key_usage_option_value(data['confirm_extended_key_usage'])
        Certificates.assert_confirm_critical_extension_option_value(data['confirm_critical_extension'])
        Certificates.assert_confirm_key_usage_option_value(data['confirm_key_usage'])
        Common.click_save_button_and_wait_for_progress_bar()

        # Verify the new Certificate Authority information after the creation.
        assert Certificates.assert_certificate_name(data['card'], data['name']) is True
        assert Certificates.assert_certificate_issuer(data['card'], data['certificate_issuer']) is True
        assert Certificates.assert_certificate_cn(data['card'], data['common_name']) is True
        assert Certificates.assert_certificate_san(data['card'], data['san']) is True

    @pytest.mark.parametrize('data', get_data_list('certificates')[0:1])
    def test_creating_a_certificate_signing_requests(self, data):
        """
        This test creates a Certificate Signing Request with the given data
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


