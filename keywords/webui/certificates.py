import re
import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common


class Certificates:
    @classmethod
    def assert_acme_dns_authenticators_card_visible(cls) -> bool:
        """
        This method verifies that the ACME DNS-Authenticators card is visible.
        :return: True if the ACME DNS-Authenticators card is visible, otherwise it returns False.

        Example:
            - Certificates.assert_acme_dns_authenticators_card_visible()
        """
        return Common.is_card_visible('ACME DNS-Authenticators')

    @classmethod
    def assert_add_certificate_authority_side_panel_visible(cls) -> bool:
        """
        This method verifies that the Add Certificate Authority side panel is visible.
        :return: True if the Add Certificate Authority side panel is visible, otherwise it returns False.

        Example:
            - Certificates.assert_add_certificate_authority_side_panel_visible()
        """
        return Common.assert_right_panel_header('Add Certificate Authority')

    @classmethod
    def assert_add_certificate_side_panels_visible(cls) -> bool:
        """
        This method verifies that the Add Certificate side panels are visible.
        :return: True if the Add Certificate side panels are visible, otherwise it returns False.

        Example:
            - Certificates.assert_add_certificate_side_panels_visible()
        """
        return Common.assert_right_panel_header('Add Certificate')

    @classmethod
    def assert_add_create_acme_certificate_side_panel_visible(cls) -> bool:
        """
        This method verifies that the Create ACME Certificate side panel is visible.
        :return: True if the Create ACME Certificate side panel is visible, otherwise it returns False.

        Example:
            - Certificates.assert_add_create_acme_certificate_side_panel_visible()
        """
        return Common.assert_right_panel_header('Create ACME Certificate')

    @classmethod
    def assert_add_csr_side_panel_visible(cls) -> bool:
        """
        This method verifies that the Add CSR side panel is visible.
        :return: True if the Add CSR side panel is visible, otherwise it returns False.

        Example:
            - Certificates.assert_add_csr_side_panel_visible()
        """
        return Common.assert_right_panel_header('Add CSR')

    @classmethod
    def assert_add_dns_authenticator_side_panel_visible(cls) -> bool:
        """
        This method verifies that the Add DNS Authenticator side panel is visible.
        :return: True if the Add DNS Authenticator side panel is visible, otherwise it returns False.

        Example:
            - Certificates.assert_add_dns_authenticator_side_panel_visible()
        """
        return Common.assert_right_panel_header('Add DNS Authenticator')

    @classmethod
    def assert_certificate_authorities_card_visible(cls) -> bool:
        """
        This method verifies that the Certificate Authorities card is visible.
        :return: True if the Certificate Authorities card is visible, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_authorities_card_visible()
        """
        return Common.is_card_visible('Certificate Authorities')

    @classmethod
    def assert_certificate_cn(cls, card_tile: str, cn) -> bool:
        """
        This method verifies that the given certificate CN is visible in the card.
        :param card_tile: The card tile name.
        :param cn: The CN of the certificate.
        :return: True if the given certificate CN is visible in the card, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_cn('Certificate Authorities', 'test')
        """
        return Common.is_visible(xpaths.common_xpaths.card_label_and_value(card_tile, 'CN:', cn))

    @classmethod
    def assert_certificate_issuer(cls, card_tile: str, issuer: str) -> bool:
        """
        This method verifies that the given certificate issuer is visible in the card.
        :param card_tile: The card tile name.
        :param issuer: The issuer of the certificate.
        :return: True if the given certificate issuer is visible in the card, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_issuer('Certificate Authorities', 'test')
        """
        return Common.is_visible(xpaths.common_xpaths.card_label_and_value(card_tile, 'Issuer:', issuer))

    @classmethod
    def assert_certificate_signing_requests_card_visible(cls) -> bool:
        """
        This method verifies that the Certificate Signing Requests card is visible.
        :return: True if the Certificate Signing Requests card is visible, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_signing_requests_card_visible()
        """
        return Common.is_card_visible('Certificate Signing Requests')

    @classmethod
    def assert_certificates_card_visible(cls) -> bool:
        """
        This method verifies that the Certificates card is visible.
        :return: True if the Certificates card is visible, otherwise it returns False.

        Example:
            - Certificates.assert_certificates_card_visible()
        """
        return Common.is_card_visible('Certificates')

    @classmethod
    def assert_certificates_page_header(cls) -> bool:
        """
        This method verifies that the Certificates page header is visible.
        :return: True if the Certificates page header is visible, otherwise it returns False.

        Example:
            - Certificates.assert_certificates_page_header()
        """
        return Common.assert_page_header('Certificates')

    @classmethod
    def assert_certificate_name(cls, card_tile: str, name: str) -> bool:
        """
        This method verifies that the given certificate name is visible in the card.
        :param card_tile: The card tile name.
        :param name: The name of the certificate.
        :return: True if the given certificate name is visible in the card, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_name('Certificate Authorities', 'test')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.card_label_and_value(card_tile, 'Name:', name))

    @classmethod
    def assert_certificate_name_deleted(cls, card_tile: str, name: str) -> bool:
        """
        This method verifies that the given certificate name is not visible in the card.
        :param card_tile: The card tile name.
        :param name: The name of the certificate
        :return: True if the given certificate name is not visible in the card, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_name_deleted('Certificate Authorities', 'test')
        """
        return Common.is_visible(xpaths.common_xpaths.card_label_and_value(card_tile, 'Name:', name))

    @classmethod
    def assert_certificate_san(cls, card_tile: str, san) -> bool:
        """
        This method verifies that the given certificate SAN is visible in the card.
        :param card_tile: The card tile name.
        :param san: The SAN of the certificate.
        :return: True if the given certificate SAN is visible in the card, otherwise it returns False.

        Example:
            - Certificates.assert_certificate_san('Certificate Authorities', 'test')
        """
        return Common.is_visible(xpaths.common_xpaths.card_label_and_value(card_tile, 'SAN:', san))

    @classmethod
    def assert_confirm_authority_key_identifier_option_value(cls, identifier: str) -> bool:
        """
        This method verifies that the Authority Key Identifier value is correct.
        :param identifier: The Authority Key Identifier value.
        :return: True if the Authority Key Identifier value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_authority_key_identifier_option_value('key_identifier')
        """
        return Common.assert_label_and_value_exist('Authority Key Identifier:', identifier)

    @classmethod
    def assert_confirm_basic_constraints_option_value(cls, constraints: str) -> bool:
        """
        This method verifies that the Basic Constraints value is correct.
        :param constraints: The Basic Constraints value.
        :return: True if the Basic Constraints value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_basic_constraints_option_value('basic_constraints')
        """
        return Common.assert_label_and_value_exist('Basic Constraints:', constraints)

    @classmethod
    def assert_confirm_critical_extension_option_value(cls, critical_extension: str) -> bool:
        """
        This method verifies that the Critical Extension value is correct.
        :param critical_extension: The Critical Extension value.
        :return: True if the Critical Extension value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_critical_extension_option_value('critical_extension')
        """
        return Common.assert_label_and_value_exist('Critical Extension:', critical_extension)

    @classmethod
    def assert_confirm_digest_algorithm_option_value(cls, algorithm: str) -> bool:
        """
        This method verifies that the Digest Algorithm value is correct.
        :param algorithm: The Digest Algorithm value.
        :return: True if the Digest Algorithm value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_digest_algorithm_option_value('digest_algorithm')
        """
        return Common.assert_label_and_value_exist('Digest Algorithm:', algorithm)

    @classmethod
    def assert_confirm_ec_curve_option_value(cls, ec_curve: str) -> bool:
        """
        This method verifies that the EC Curve value is correct.
        :param ec_curve: The EC Curve value.
        :return: True if the EC Curve value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_ec_curve_option_value('ec_curve')
        """
        return Common.assert_label_and_value_exist('EC Curve:', ec_curve)

    @classmethod
    def assert_confirm_email_option_value(cls, email: str) -> bool:
        """
        This method verifies that the Email value is correct.
        :param email: The Email value.
        :return: True if the Email value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_email_option_value('email')
        """
        return Common.assert_label_and_value_exist('Email:', email)

    @classmethod
    def assert_confirm_extended_key_usage_option_value(cls, extended: str) -> bool:
        """
        This method verifies that the Extended Key Usage value is correct.
        :param extended: The Extended Key Usage value.
        :return: True if the Extended Key Usage value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_extended_key_usage_option_value('extended_key_usage')
        """
        return Common.assert_label_and_value_exist('Subject:', extended)

    @classmethod
    def assert_confirm_key_length_option_value(cls, key_type: int) -> bool:
        """
        This method verifies that the Key Length value is correct.
        :param key_type: The Key Length value.
        :return: True if the Key Length value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_key_length_option_value('key_length')
        """
        return Common.assert_label_and_value_exist('Key Length:', str(key_type))

    @classmethod
    def assert_confirm_key_type_option_value(cls, key_type: str) -> bool:
        """
        This method verifies that the Key Type value is correct.
        :param key_type: The Key Type value.
        :return: True if the Key Type value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_key_type_option_value('key_type')
        """
        return Common.assert_label_and_value_exist('Key Type:', key_type)

    @classmethod
    def assert_confirm_key_usage_option_value(cls, key_usage: str) -> bool:
        """
        This method verifies that the Key Usage value is correct.
        :param key_usage: The Key Usage value.
        :return: True if the Key Usage value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_key_usage_option_value('key_usage')
        """
        return Common.assert_label_and_value_exist('Key Usage:', key_usage)

    @classmethod
    def assert_confirm_lifetime_option_value(cls, days: int) -> bool:
        """
        This method verifies that the Lifetime value is correct.
        :param days: The certificate lifetime value.
        :return: True if the Lifetime value is correct, otherwise it returns False.
        """
        return Common.assert_label_and_value_exist('Lifetime:', str(days))

    @classmethod
    def assert_confirm_name_option_value(cls, name: str) -> bool:
        """
        This method verifies that the Name value is correct.
        :param name: The certificate name value.
        :return: True if the Name value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_name_option_value('name')
        """
        return Common.assert_label_and_value_exist('Name:', name)

    @classmethod
    def assert_confirm_path_length_option_value(cls, length: int) -> bool:
        """
        This method verifies that the Path Length value is correct.
        :param length: The Path Length value.
        :return: True if the Path Length value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_path_length_option_value('path_length')
        """
        return Common.assert_label_and_value_exist('Path Length:', str(length))

    @classmethod
    def assert_confirm_profile_option_value(cls, profile: str) -> bool:
        """
        This method verifies that the Profile value is correct.
        :param profile: The Profile value.
        :return: True if the Profile value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_profile_option_value('profile')
        """
        return Common.assert_label_and_value_exist('Profile:', profile)

    @classmethod
    def assert_confirm_san_option_value(cls, san: str) -> bool:
        """
        This method verifies that the SAN value is correct.
        :param san: The SAN value.
        :return: True if the SAN value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_san_option_value('san')
        """
        return Common.assert_label_and_value_exist('SAN:', san)

    @classmethod
    def assert_confirm_signing_certificate_authority_option_value(cls, sca: str) -> bool:
        """
        This method verifies that the Signing Certificate Authority value is correct.
        :param sca: The Signing Certificate Authority value.
        :return: True if the Signing Certificate Authority value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_signing_certificate_authority_option_value('signing_certificate_authority')
        """
        return Common.assert_label_and_value_exist('Signing Certificate Authority:', sca)

    @classmethod
    def assert_confirm_subject_option_value(cls, subject: str) -> bool:
        """
        This method verifies that the Subject value is correct.
        :param subject: The Subject value.
        :return: True if the Subject value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_subject_option_value('subject')
        """
        return Common.assert_label_and_value_exist('Subject:', subject)

    @classmethod
    def assert_confirm_type_option_value(cls, cert_type: str) -> bool:
        """
        This method verifies that the Type value is correct.
        :param cert_type: The certificate type value.
        :return: True if the Type value is correct, otherwise it returns False.

        Example:
            - Certificates.assert_confirm_type_option_value('cert_type')
        """
        return Common.assert_label_and_value_exist('Type:', cert_type)

    @classmethod
    def assert_sign_csr_dialog_visible(cls) -> bool:
        """
        This method verifies that the Sign CSR dialog is visible.
        :return: True if the Sign CSR dialog is visible, otherwise it returns False.

        Example:
            - Certificates.assert_sign_csr_dialog_visible()
        """
        return Common.assert_dialog_visible('Sign CSR')

    @classmethod
    def click_acme_dns_authenticators_add_button(cls) -> None:
        """
        This method clicks on ACME DNS-Authenticators Add button.

        Example:
            - Certificates.click_acme_dns_authenticators_add_button()
        """
        Common.click_button('acme-dns-authenticator')

    @classmethod
    def click_certificates_add_button(cls) -> None:
        """
        This method clicks on Certificates Add button.

        Example:
            - Certificates.click_certificates_add_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('add-certificate', 1))

    @classmethod
    def click_certificate_options_back_button(cls) -> None:
        """
        This method clicks on Certificate Options Back button.

        Example:
            - Certificates.click_certificate_options_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 1))
        WebUI.delay(0.1)

    @classmethod
    def click_certificate_authorities_add_button(cls) -> None:
        """
        This method clicks on Certificate Authorities Add button.

        Example:
            - Certificates.click_certificate_authorities_add_button()
        """
        Common.click_button('add-certificate-authority')

    @classmethod
    def click_certificate_options_next_button(cls) -> None:
        """
        This method clicks on Certificate Options Next button.

        Example:
            - Certificates.click_certificate_options_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 2))
        WebUI.delay(0.1)

    @classmethod
    def click_certificate_signing_requests_add_button(cls) -> None:
        """
        This method clicks on Certificate Signing Requests Add button.

        Example:
            - Certificates.click_certificate_signing_requests_add_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('add-certificate', 2))

    @classmethod
    def click_certificate_subject_next_button(cls) -> None:
        """
        This method clicks on Certificate Subject Next button.

        Example:
            - Certificates.click_certificate_subject_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 3))
        WebUI.delay(0.1)

    @classmethod
    def click_certificate_subject_back_button(cls) -> None:
        """
        This method clicks on Certificate Subject Back button.

        Example:
            - Certificates.click_certificate_subject_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 2))
        WebUI.delay(0.1)

    @classmethod
    def click_confirm_options_back_button(cls) -> None:
        """
        This method clicks on Confirm Options Back button.

        Example:
            - Certificates.click_confirm_options_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 4))
        WebUI.delay(0.1)

    @classmethod
    def click_extra_constraints_back_button(cls) -> None:
        """
        This method clicks on Extra Constraints Back button.

        Example:
            - Certificates.click_extra_constraints_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 3))
        WebUI.delay(0.1)

    @classmethod
    def click_extra_constraints_next_button(cls) -> None:
        """
        This method clicks on Extra Constraints Next button.

        Example:
            - Certificates.click_extra_constraints_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 4))
        WebUI.delay(0.1)

    @classmethod
    def click_identifier_and_type_next_button(cls) -> None:
        """
        This method clicks on Identifier and Type Next button.

        Example:
            - Certificates.click_identifier_and_type_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 1))
        WebUI.delay(0.1)

    @classmethod
    def click_import_certificate_back_button(cls) -> None:
        """
        This method clicks on Import Certificate Back button.

        Example:
            - Certificates.click_import_certificate_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 1))
        WebUI.delay(0.1)

    @classmethod
    def click_import_certificate_next_button(cls) -> None:
        """
        This method clicks on Import Certificate Next button.

        Example:
            - Certificates.click_import_certificate_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 2))
        WebUI.delay(0.1)

    @classmethod
    def click_import_confirm_options_back_button(cls) -> None:
        """
        This method clicks on Import Confirm Options Back button.

        Example:
            - Certificates.click_import_confirm_options_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 2))
        WebUI.delay(0.1)

    @classmethod
    def click_sign_csr_button(cls) -> None:
        """
        This method clicks on Sign CSR button.

        Example:
            - Certificates.click_sign_csr_button()
        """
        Common.click_button('sign-csr')
        Common.assert_please_wait_not_visible()

    @classmethod
    def click_the_acme_dns_authenticators_delete_button_by_name(cls, authenticators_name: str) -> None:
        """
        This method clicks on the ACME DNS Authenticators Delete button by name and confirm the dialog.
        :param authenticators_name: The name of the ACME DNS Authenticators.

        Example:
            - Certificates.click_the_acme_dns_authenticators_delete_button_by_name('ada_name')
        """
        cls.delete_certificate_by_name('acme-dns-authenticator', authenticators_name)

    @classmethod
    def click_the_certificate_authorities_delete_button_by_name(cls, ca_name: str) -> None:
        """
        This method clicks on the CA Delete button by name and confirm the dialog.
        :param ca_name: The name of the Certificate Authorities.

        Example:
            - Certificates.click_the_certificate_authorities_delete_button_by_name('ca_name')
        """
        cls.delete_certificate_by_name('ca', ca_name)

    @classmethod
    def click_the_certificate_authorities_download_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Certificate Authorities Download button by name.
        :param certificate_name: The name of the Certificate Authorities.

        Example:
            - Certificates.click_the_certificate_authorities_download_button_by_name('ca_name')
        """
        cls.click_the_field_button_by_card_certificate_name('ca', certificate_name, 'mdi-download')

    @classmethod
    def click_certificate_authorities_revoke_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Revoke button in the row of the certificate.
        :param certificate_name: The name of the Certificate Authorities.

        Example:
            - Certificates.click_certificate_authorities_revoke_button_by_name('ca_name')
        """
        cls.click_the_field_button_by_card_certificate_name('ca', 'mdi-undo', certificate_name)

    @classmethod
    def click_certificate_authorities_sign_csr_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Sign CSR button in the row of the certificate.
        :param certificate_name: The name of the Certificate Authorities.

        Example:
            - Certificates.click_certificate_authorities_sign_csr_button_by_name('ca_name')
        """
        cls.click_the_field_button_by_card_certificate_name('ca', 'beenhere', certificate_name)

    @classmethod
    def click_the_certificates_delete_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Certificate Delete button by name and confirm the dialog.
        :param certificate_name: The name of the Certificate.

        Example:
            - Certificates.click_the_certificates_delete_button_by_name('cert_name')
        """
        cls.delete_certificate_by_name('cert', certificate_name)

    @classmethod
    def click_the_certificates_download_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Certificate Download button by name.
        :param certificate_name: The name of the Certificate.

        Example:
            - Certificates.click_the_certificates_download_button_by_name('cert_name')
        """
        cls.click_the_field_button_by_card_certificate_name('cert', certificate_name, 'mdi-download')

    @classmethod
    def click_the_csr_delete_button_by_name(cls, csr_name: str) -> None:
        """
        This method clicks on the Certificate Signing Requests Delete button by name and confirm the dialog.
        :param csr_name: The name of the Certificate Signing Requests.

        Example:
            - Certificates.click_the_csr_delete_button_by_name('csr_name')
        """
        cls.delete_certificate_by_name('csr', csr_name)

    @classmethod
    def click_the_csr_download_button_by_name(cls, certificate_name: str) -> None:
        """
        This method clicks on the Certificate Signing Requests Download button by name.
        :param certificate_name: The name of the Certificate Signing Requests.

        Example:
            - Certificates.click_the_csr_download_button_by_name('csr_name')
        """
        cls.click_the_field_button_by_card_certificate_name('cert', certificate_name, 'mdi-download')

    @classmethod
    def click_the_field_button_by_card_certificate_name(cls, card: str, cert_name: str, field: str) -> None:
        """
        This method clicks on the button in the row of the certificate by card and certificate name.
        :param card: the card name from these values:
            'ACME DNS Authenticators': `acme-dns-authenticator`, 'Certificate Authorities': 'ca',
            'Certificate Signing Requests': 'csr' or 'Certificates': 'cert'.
        :param cert_name: The name of the certificate
        :param field: The field name from these values: 'edit', 'delete', 'download',

        Example:
            - Certificates.click_the_field_button_by_card_certificate_name('acme-dns-authenticator', 'test', 'delete')
        """
        # data-test="button-cert-truenas-default-delete-row-action"
        # data-test="button-csr-test-delete-row-action"
        # replace spaces and underscores with hyphens.
        certification_name = re.sub(r'([ _])', '-', cert_name.lower())
        Common.click_button(f'{card}-{certification_name}-{field}-row-action')

    @classmethod
    def delete_certificate_by_name(cls, card: str, certificate_name: str) -> None:
        """
        This method clicks on the delete button in the row of the certificate and confirm the dialog.
        :param card: the card name from these values:
            'ACME DNS Authenticators': `acme-dns-authenticator`, 'Certificate Authorities': 'ca',
            'Certificate Signing Requests': 'csr' or 'Certificates': 'cert'.
        :param certificate_name: The name of the certificate.

        Example:
            - Certificates.delete_certificate_by_name('acme-dns-authenticator', 'test')
        """
        cls.click_the_field_button_by_card_certificate_name(card, certificate_name, 'delete')
        if WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field('force'), shared_config['SHORT_WAIT']):
            Common.set_checkbox('force')
            Common.click_button('delete')
        if WebUI.wait_until_clickable(xpaths.common_xpaths.checkbox_field('confirm')):
            Common.assert_confirm_dialog()

    @classmethod
    def select_acme_first_domain_option(cls, option: str) -> None:
        """
        This method click on ACME First Domain and select an option.
        :param option: The domain name.

        Example:
            - Certificates.select_acme_first_domain_option('test.com')
        """
        # TODO: This will will be replaced by select_Field when the data-test get fix
        Common.click_on_element('//*[@data-test="select"]')
        Common.click_on_element(xpaths.common_xpaths.option_field(option))

    @classmethod
    def select_acme_second_domain_option(cls, domain_id: str) -> None:
        """
        This method click on ACME Second Domain and select an option.
        :param domain_id: The domain id in the list.

        Example:
            - Certificates.select_acme_second_domain_option('www.test.com')
        """
        Common.select_option('1', f'1-{domain_id}')

    @classmethod
    def select_acme_server_directory_uri_option(cls, option: str) -> None:
        """
        This method click on ACME Server Directory URI and select an option.
        :param option: The option to select from these values:
            ['lets-encrypt-staging-directory', 'lets-encrypt-production-directory']

        Example:
            - Certificates.select_acme_server_directory_uri_option('lets-encrypt-staging-directory')
        """
        Common.select_option('acme-directory-uri', f'acme-directory-uri-{option}')

    @classmethod
    def select_authenticator_option(cls, option: str) -> None:
        """
        This method click on Authenticator and select the given option.
        :param option: The option to select from these values:
            ['cloudflare', 'route-53', 'ovh', 'shell']

        Example:
            - Certificates.select_authenticator_option('cloudflare')
        """
        Common.select_option('authenticator', f'authenticator-{option}')

    @classmethod
    def select_authority_key_config_option(cls, option: str) -> None:
        """
        This method click on Authority Key Config and select the given option.
        :param option: The option to select from these values:
            ['select', 'authority-cert-issuer', 'critical-extension']

        Example:
            - Certificates.select_authority_key_config_option('authority-cert-issuer')
        """
        Common.select_option('authority-key-identifier', f'authority-key-identifier-{option}')
        # required to close select option dropdown
        Common.click_on_element(xpaths.common_xpaths.overlay_container)

    @classmethod
    def select_basic_constraints_config_option(cls, option: str) -> None:
        """
        This method click on Basic Constraints Config and select the given option.
        :param option: The option to select from these values:
            ['select', 'ca', 'critical-extension']

        Example:
            - Certificates.select_basic_constraints_config_option('ca')
        """
        Common.select_option('basic-constraints', f'basic-constraints-{option}')
        # required to close select option dropdown
        Common.click_on_element(xpaths.common_xpaths.overlay_container)

    @classmethod
    def select_certificate_authority_profile_option(cls, option: str) -> None:
        """
        This method click on Certificate Authority Profile and select the given option.
        :param option: Is an option from these values: ['select', 'ca']

        Example:
            - Certificates.select_certificate_authority_profile_option('ca')
        """
        Common.select_option('profile', f'profile-{option}')

    @classmethod
    def select_certificate_authority_type_option(cls, option: str) -> None:
        """
        This method click on Certificate Authority Type and select the given option.
        :param option: The option to select from these values:
            ['internal-ca', 'intermediate-ca', 'import-ca']

        Example:
            - Certificates.select_certificate_authority_type_option('internal-ca')
        """
        Common.select_option('create-type', f'create-type-{option}')

    @classmethod
    def select_certificates_type_option(cls, option: str) -> None:
        """
        This method clicks on Certificates Type and select the given option.
        :param option: The option to select from the certificates type list.

        Example:
            - Certificates.select_certificates_type_option('select')
        """
        Common.select_option('create-type', f'create-type{option}')

    @classmethod
    def select_country_option(cls, country: str) -> None:
        """
        This method click on Country and select the given option.
        :param country: The name of the country all characters are lower case with dash for spaces like 'united-states'.

        Example:
            - Certificates.select_country_option('united-states')
        """
        Common.select_option('country', f'country-{country}')

    @classmethod
    def select_csr_type_option(cls, option: str) -> None:
        """
        This method click on CSR Type and select the given option.
        :param option: The option to select these values:
            ['certificate-signing-request', 'import-certificate-signing-request']

        Example:
            - Certificates.select_csr_type_option('certificate-signing-request')
        """
        Common.select_option('create-type', f'create-type-{option}')

    @classmethod
    def select_csrs_option(cls, csr_id: str) -> None:
        """
        This method click on CSRs and select an option.
        :param csr_id: Is the name of the CSR all characters are lower case and replace underscore with dash.

        Example:
            - Certificates.select_csrs_option('csr-id-1')
        """
        Common.select_option('csr-cert-id', f'csr-cert-id-{csr_id}')

    @classmethod
    def select_digest_algorithm_option(cls, option: str) -> None:
        """
        This method click on Digest Algorithm and select the given option.
        :param option: The option to select from these values:
            ['sha-1', 'sha-224', 'sha-256', 'sha-384', 'sha-512']

        Example:
            - Certificates.select_digest_algorithm_option('sha-256')
        """
        Common.select_option('digest-algorithm', f'digest-algorithm-{option}')

    @classmethod
    def select_ec_curve_option(cls, option: str) -> None:
        """
        This method click on EC Curve and select the given option.
        :param option: The option to select from these values:
            ['secp-256-r-1', 'secp-384-r-1', 'secp-521-r-1', 'ed-25519']

        Example:
            - Certificates.select_ec_curve_option('ed-25519')
        """
        Common.select_option('ec-curve', f'ec-curve-{option}')

    @classmethod
    def select_key_length_option(cls, option: str) -> None:
        """
        This method click on Key Length and select the given option.
        :param option: The option to select from these values: ['1024', '2048', '4096']

        Example:
            - Certificates.select_key_length_option('2048')
        """
        Common.select_option('key-length', f'key-length-{option}')

    @classmethod
    def select_key_type_option(cls, option: str) -> None:
        """
        This method click on Key Type and select the given option.
        :param option: The option to select from these values: ['rsa', 'ec']

        Example:
            - Certificates.select_key_type_option('rsa')
        """
        Common.select_option('key-type', f'key-type-{option}')

    @classmethod
    def select_key_usage_config_option(cls, option: str) -> None:
        """
        This method click on Key Usage Config and select the given option.
        :param option: The option to select from these values:
            ['digital-signature', 'content-commitment', 'key-encipherment', 'data-encipherment', 'key-agreement',
             'key-cert-sign', 'crl-sign', 'encipher-only', 'decipher-only', 'critical-extension']

        Example:
            - Certificates.select_key_usage_config_option('key-cert-sign')
        """
        Common.select_option('key-usage', f'key-usage-{option}')
        # required to close select option dropdown
        Common.click_on_element(xpaths.common_xpaths.overlay_container)

    @classmethod
    def select_profile_option(cls, option: str) -> None:
        """
        This method click on Profile and select the given option.
        :param option: The option to select from these values:
            ['select', 'https-rsa-certificate', 'https-ecc-certificate']

        Example:
            - Certificates.select_profile_option('https-rsa-certificate')
        """
        Common.select_option('profile', f'profile-{option}')

    @classmethod
    def select_signing_certificate_authority_option(cls, option: str) -> None:
        """
        This method click on Signing Certificate Authority and select the given option.
        :param option: The name of a Certificate Authority are all lower case.

        Example:
            - Certificates.select_signing_certificate_authority_option('letsencrypt')
        """
        Common.select_option('signing', f'signing-{option}')

    @classmethod
    def select_usages_option(cls, option: str) -> None:
        """
        This method click on Usages and select the given option.
        :param option: The option to select from these values:
            ['any-extended-key-usage', 'certificate-transparency', 'client-auth', 'code-signing', 'email-protection',
             'ipsec-ike', 'kerberos-pkinit-kdc', 'ocsp-signing', 'server-auth', 'smartcard-logon', 'time-stamping']

        Example:
            - Certificates.select_usages_option('any-extended-key-usage')
        """
        Common.select_option('usages', f'key-usage-{option}')
        # required to close select option dropdown
        Common.click_on_element(xpaths.common_xpaths.overlay_container)

    @classmethod
    def set_access_key_id(cls, key_id: str) -> None:
        """
        This method sets the access key id input field.
        :param key_id: The access key id.

        Example:
            - Certificates.set_access_key_id('my-access-key-id')
        """
        Common.set_input_field('access-key-id', key_id)

    @classmethod
    def set_acme_certificate_identifier(cls, name: str) -> None:
        """
        This method sets the acme certificate identifier input field.
        :param name: The name of the certificate.

        Example:
            - Certificates.set_acme_certificate_identifier('test')
        """
        cls.set_name(name)

    @classmethod
    def set_add_to_trusted_store_checkbox(cls) -> None:
        """
        This method click on Add to Trusted Store checkbox.

        Example:
            - Certificates.set_add_to_trusted_store_checkbox()
        """
        Common.set_checkbox('add-to-trusted-store')

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """
        This method sets the api key input field.
        :param api_key: The api key.

        Example:
            - Certificates.set_api_key('my-api-key')
        """
        Common.set_input_field('api-key', api_key)

    @classmethod
    def set_api_token(cls, api_token: str) -> None:
        """
        This method sets the api token input field.
        :param api_token: The api token.

        Example:
            - Certificates.set_api_token('my-api-token')
        """
        Common.set_input_field('api-token', api_token)

    @classmethod
    def set_authenticator_script(cls, script: str) -> None:
        """
        This method sets the authenticator script input field.
        :param script: The authenticator script.

        Example:
            - Certificates.set_authenticator_script('my-authenticator-script')
        """
        Common.set_input_field('script', script)

    @classmethod
    def set_authority_key_identifier_checkbox(cls) -> None:
        """
        This method sets the authority key identifier's checkbox.

        Example:
            - Certificates.set_authority_key_identifier_checkbox()
        """
        Common.set_checkbox_by_row('enabled', 2)

    @classmethod
    def set_basic_constraints(cls) -> None:
        """
        This method sets the basic constraint's checkbox.

        Example:
            - Certificates.set_basic_constraints()
        """
        Common.set_checkbox_by_row('enabled', 1)

    @classmethod
    def set_certificate(cls, certificate: str) -> None:
        """
        This method sets the certificate of the certificate textarea field.
        :param certificate: The certificate in PEM format.

        Example:
            - Certificates.set_certificate('certificate')
        """
        Common.set_textarea_field('certificate', certificate)

    @classmethod
    def set_cloudflare_email(cls, email: str) -> None:
        """
        This method sets the cloudflare email input field.
        :param email: The cloudflare email.

        Example:
            - Certificates.set_cloudflare_email('me@example.com')
        """
        Common.set_input_field('cloudflare-email', email)

    @classmethod
    def set_common_name(cls, common) -> None:
        """
        This method sets the common name of the certificate input field.
        :param common: The fully-qualified hostname (FQDN) of the system.
            This name must be unique within a certificate chain.

        Example:
            - Certificates.set_common_name('example.com')
        """
        Common.set_input_field('common', common)

    @classmethod
    def set_confirm_passphrase(cls, passphrase) -> None:
        """
        This method sets the confirmation passphrase input field for the certificate.
        :param passphrase: The confirmation passphrase for the certificate.

        Example:
            - Certificates.set_confirm_passphrase('passphrase')
        """
        Common.set_input_field('passphrase-2', passphrase)

    @classmethod
    def set_critical_extension(cls) -> None:
        """
        This method sets the critical extension's checkbox.

        Example:
            - Certificates.set_critical_extension()
        """
        Common.set_checkbox('extension-critical')

    @classmethod
    def set_csr_exists_on_this_system(cls) -> None:
        """
        This method sets the CSR exists on this system's checkbox.

        Example:
            - Certificates.set_csr_exists_on_this_system()
        """
        Common.set_checkbox('csr-exists-on-system')

    @classmethod
    def set_email(cls, email) -> None:
        """
        This method sets the email of the certificate input field.
        :param email: Enter the email address of the person responsible for the Certificate.

        Example:
            - Certificates.set_email('me@example.com')
        """
        Common.set_input_field('email', email)

    @classmethod
    def set_extended_key_usage(cls) -> None:
        """
        This method sets the extended key usage's checkbox.

        Example:
            - Certificates.set_extended_key_usage()
        """
        Common.set_checkbox_by_row('enabled', 3)

    @classmethod
    def set_key_usage(cls) -> None:
        """
        This method sets the key usage's checkbox.

        Example:
            - Certificates.set_key_usage()
        """
        Common.set_checkbox_by_row('enabled', 4)

    @classmethod
    def set_lifetime(cls, number: int) -> None:
        """
        This method sets the lifetime of the certificate input field.
        :param number: The nuber of days for the lifetime for the certificate.

        Example:
            - Certificates.set_lifetime(365)
        """
        Common.set_input_field('lifetime', str(number))

    @classmethod
    def set_locality(cls, city) -> None:
        """
        This method sets the locality of the certificate input field.
        :param city: The locality of the certificate.

        Example:
            - Certificates.set_locality('City')
        """
        Common.set_input_field('city', city)

    @classmethod
    def set_name(cls, name: str) -> None:
        """
        This method sets the name of the certificate input field.
        :param name: The name of the certificate.

        Example:
            - Certificates.set_name('test')
        """
        Common.set_input_field('name', name)

    @classmethod
    def set_organization(cls, organization) -> None:
        """
        This method sets the organization of the certificate input field.
        :param organization: The name of the company or organization.

        Example:
            - Certificates.set_organization('Company')
        """
        Common.set_input_field('organization', organization)

    @classmethod
    def set_organizational_unit(cls, organizational_unit) -> None:
        """
        This method sets the organizational unit of the certificate input field.
        :param organizational_unit: The organizational unit of the entity.

        Example:
            - Certificates.set_organizational_unit('test')
        """
        Common.set_input_field('organizational-unit', organizational_unit)

    @classmethod
    def set_ovh_application_key(cls, app_key: str) -> None:
        """
        This method sets the application key input field.
        :param app_key: The application key.

        Example:
            - Certificates.set_ovh_application_key('my-application-key')
        """
        Common.set_input_field('application-key', app_key)

    @classmethod
    def set_ovh_consumer_key(cls, consumer_key: str) -> None:
        """
        This method sets the consumer key input field.
        :param consumer_key: The consumer key.

        Example:
            - Certificates.set_ovh_consumer_key('my-consumer-key')
        """
        Common.set_input_field('consumer-key', consumer_key)

    @classmethod
    def set_ovh_endpoint(cls, endpoint: str) -> None:
        """
        This method sets the endpoint input field.
        :param endpoint: The endpoint.

        Example:
            - Certificates.set_ovh_endpoint('my-endpoint')
        """
        Common.set_input_field('endpoint', endpoint)

    @classmethod
    def set_passphrase(cls, passphrase: str) -> None:
        """
        This method sets the passphrase input field for the certificate.
        :param passphrase: The passphrase for the certificate.

        Example:
            - Certificates.set_passphrase('passphrase')
        """
        Common.set_input_field('passphrase', passphrase)

    @classmethod
    def set_path_length(cls, length: int) -> None:
        """
        This method sets the path length of the certificate input field.
        :param length: The path length of the certificate.

        Example:
            - Certificates.set_path_length(1)
        """
        Common.set_input_field('path-length', str(length))

    @classmethod
    def set_private_key(cls, private_key: str) -> None:
        """
        This method sets the private key of the certificate textarea field.
        :param private_key: The private key.

        Example:
            - Certificates.set_private_key('private_key')
        """
        Common.set_textarea_field('privatekey', private_key)

    @classmethod
    def set_propagation_delay(cls, delay: int) -> None:
        """
        This method sets the propagation delay input field.
        :param delay: The propagation delay.

        Example:
            - Certificates.set_propagation_delay('10')
        """
        Common.set_input_field('delay', str(delay))

    @classmethod
    def set_renew_certificate_days(cls, days: int) -> None:
        """
        This method sets the renew certificate days input field.
        :param days: The numbers of days to renew the certificate.

        Example:
            - Certificates.set_renew_certificate_days('10')
        """
        Common.set_input_field('timeout', str(days))

    @classmethod
    def set_running_user(cls, user: str) -> None:
        """
        This method sets the running user input field.
        :param user: The running username.

        Example:
            - Certificates.set_running_user('username')
        """
        Common.set_input_field('user', user)

    @classmethod
    def set_secret_access_key(cls, secret: str) -> None:
        """
        This method sets the secret access key of the certificate input field.
        :param secret: The secret access key.

        Example:
            - Certificates.set_secret_access_key('my-secret-access-key')
        """
        Common.set_input_field('secret-access-key', secret)

    @classmethod
    def set_sign_csr_identifier(cls, name: str) -> None:
        """
        This method sets the signing csr identifier of the certificate input field.
        :param name: The name of the certificate.

        Example:
            - Certificates.set_sign_csr_identifier('test')
        """
        cls.set_name(name)

    @classmethod
    def set_signing_request(cls, csr: str) -> None:
        """
        This method sets the signing request of the certificate textarea field.
        :param csr: The certificate signing request.

        Example:
            - Certificates.set_signing_request('csr')
        """
        Common.set_textarea_field('csr', csr)

    @classmethod
    def set_state(cls, state) -> None:
        """
        This method sets the state of the certificate input field.
        :param state:  The state or province of the organization

        Example:
            - Certificates.set_state('New Brunswick')
        """
        Common.set_input_field('state', state)

    @classmethod
    def set_subject_alternative_name(cls, san) -> None:
        """
        This method sets the subject alternative name of the certificate input field.
        :param san: The Multi-domain support. Enter additional domains to secure.
             Separate domains by pressing Enter For example, if the primary domain is example.com,
             entering www.example.com secures both addresses.

        Example:
            - Certificates.set_subject_alternative_name('www.example.com')
        """
        Common.set_input_field('san', san)

    @classmethod
    def set_terms_of_service_checkbox(cls) -> None:
        """
        This method sets the terms of service checkbox.

        Example:
            - Certificates.set_terms_of_service_checkbox()
        """
        Common.set_checkbox('tos')

    @classmethod
    def set_timeout(cls, timeout: int) -> None:
        """
        This method sets the timeout input field.
        :param timeout: The timeout.

        Example:
            - Certificates.set_timeout('10')
        """
        Common.set_input_field('timeout', str(timeout))

    @classmethod
    def unset_add_to_trusted_store_checkbox(cls) -> None:
        """
        This method unclick on Add to Trusted Store checkbox.

        Example:
            - Certificates.unset_add_to_trusted_store_checkbox()
        """
        Common.unset_checkbox('add-to-trusted-store')

    @classmethod
    def unset_authority_key_identifier_checkbox(cls) -> None:
        """
        This method unsets the authority key identifier's checkbox.

        Example:
            - Certificates.unset_authority_key_identifier_checkbox()
        """
        Common.unset_checkbox_by_row('enabled', 2)

    @classmethod
    def unset_basic_constraints(cls) -> None:
        """
        This method unsets the basic constraint's checkbox.

        Example:
            - Certificates.unset_basic_constraints()
        """
        Common.unset_checkbox_by_row('enabled', 1)

    @classmethod
    def unset_critical_extension(cls) -> None:
        """
        This method unsets the critical extension's checkbox.

        Example:
            - Certificates.unset_critical_extension()
        """
        Common.unset_checkbox('extension-critical')

    @classmethod
    def unset_csr_exists_on_this_system(cls) -> None:
        """
        This method unsets the CSR exists on this system's checkbox.

        Example:
            - Certificates.unset_csr_exists_on_this_system()
        """
        Common.unset_checkbox('csr-exists-on-system')

    @classmethod
    def unset_extended_key_usage(cls) -> None:
        """
        This method unsets the extended key usage's checkbox.

        Example:
            - Certificates.unset_extended_key_usage()
        """
        Common.unset_checkbox_by_row('enabled', 3)

    @classmethod
    def unset_key_usage(cls) -> None:
        """
        This method unsets the key usage's checkbox.

        Example:
            - Certificates.unset_key_usage()
        """
        Common.unset_checkbox_by_row('enabled', 4)

    @classmethod
    def unset_terms_of_service_checkbox(cls) -> None:
        """
        This method unsets the terms of service checkbox.

        Example:
            - Certificates.unset_terms_of_service_checkbox()
        """
        Common.unset_checkbox('tos')
