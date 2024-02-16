import xpaths
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
    def click_identifier_and_type_next_button(cls) -> None:
        """
        This method clicks on Identifier and Type Next button.

        Example:
            - Certificates.click_identifier_and_type_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 1))
        WebUI.delay(0.1)

    @classmethod
    def click_certificate_subject_next_button(cls):
        """
        This method clicks on Certificate Subject Next button.

        Example:
            - Certificates.click_certificate_subject_next_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('next', 3))
        WebUI.delay(0.1)

    @classmethod
    def click_certificate_subject_back_button(cls):
        """
        This method clicks on Certificate Subject Back button.

        Example:
            - Certificates.click_certificate_subject_back_button()
        """
        Common.click_on_element(xpaths.common_xpaths.button_field_by_row('back', 2))
        WebUI.delay(0.1)

    @classmethod
    def select_certificate_authority_profile_option(cls, option: str) -> None:
        """
        This method click on Certificate Authority Profile and select an option.
        :param option: Is an option from these values: ['select', 'ca']

        Example:
            - Certificates.select_certificate_authority_profile_option('ca')
        """
        Common.select_option('profile', f'profile-{option}')

    @classmethod
    def select_certificate_authority_type_option(cls, option: str) -> None:
        """
        This method click on Certificate Authority Type and select an option.
        :param option: The option to select from these values:
            ['internal-ca', 'intermediate-ca', 'import-ca']

        Example:
            - Certificates.select_certificate_authority_type_option('internal-ca')
        """
        Common.select_option('create-type', f'create-type-{option}')

    @classmethod
    def select_certificates_type_option(cls, option: str) -> None:
        """
        This method clicks on Certificates Type and select an option.
        :param option: The option to select from the certificates type list.

        Example:
            - Certificates.select_certificates_type_option('select')
        """
        Common.select_option('create-type', f'create-type{option}')

    @classmethod
    def select_country_option(cls, country: str) -> None:
        """
        This method click on Country and select an option.
        :param country: The name of the country all characters are lower case with dash for spaces like 'united-states'.

        Example:
            - Certificates.select_country_option('united-states')
        """
        Common.select_option('country', f'country-{country}')

    @classmethod
    def select_csr_type_option(cls, option: str) -> None:
        """
        This method click on CSR Type and select an option.
        :param option: The option to select these values:
            ['certificate-signing-request', 'import-certificate-signing-request']

        Example:
            - Certificates.select_csr_type_option('certificate-signing-request')
        """
        Common.select_option('create-type', f'create-type-{option}')

    @classmethod
    def select_digest_algorithm_option(cls, option: str):
        """
        This method click on Digest Algorithm and select an option.
        :param option: The option to select from these values:
            ['sha-1', 'sha-224', 'sha-256', 'sha-384', 'sha-512']

        Example:
            - Certificates.select_digest_algorithm_option('sha-256')
        """
        Common.select_option('digest-algorithm', f'digest-algorithm-{option}')

    @classmethod
    def select_ec_curve_option(cls, option: str):
        """
        This method click on EC Curve and select an option.
        :param option: The option to select from these values:
            ['secp-256-r-1', 'secp-384-r-1', 'secp-521-r-1', 'ed-25519']

        Example:
            - Certificates.select_ec_curve_option('ed-25519')
        """
        Common.select_option('ec-curve', f'ec-curve-{option}')

    @classmethod
    def select_key_length_option(cls, option: str):
        """
        This method click on Key Length and select an option.
        :param option: The option to select from these values: ['1024', '2048', '4096']

        Example:
            - Certificates.select_key_length_option('2048')
        """
        Common.select_option('key-length', f'key-length-{option}')

    @classmethod
    def select_key_type_option(cls, option: str):
        """
        This method click on Key Type and select an option.
        :param option: The option to select from these values: ['rsa', 'ec']

        Example:
            - Certificates.select_key_type_option('rsa')
        """
        Common.select_option('key-type', f'key-type-{option}')

    @classmethod
    def select_profile_option(cls, option: str) -> None:
        """
        This method click on Profile and select an option.
        :param option: The option to select from these values:
            ['select', 'https-rsa-certificate', 'https-ecc-certificate']

        Example:
            - Certificates.select_profile_option('https-rsa-certificate')
        """
        Common.select_option('profile', f'profile-{option}')

    @classmethod
    def select_signing_certificate_authority_option(cls, option: str):
        """
        This method click on Signing Certificate Authority and select an option
        :param option: The name of a Certificate Authority are all lower case.

        Example:
            - Certificates.select_signing_certificate_authority_option('letsencrypt')
        """
        Common.select_option('signing', f'signing-{option}')

    @classmethod
    def set_add_to_trusted_store_checkbox(cls):
        """
        This method click on Add to Trusted Store checkbox.

        Example:
            - Certificates.set_add_to_trusted_store_checkbox()
        """
        Common.set_checkbox('add-to-trusted-store')

    @classmethod
    def set_basic_constraints(cls):
        Common.set_checkbox_by_row('enabled', 1)

    @classmethod
    def unset_basic_constraints(cls) -> None:
        """
        This method unsets the basic constraint's checkbox.

        Example:
            - Certificates.unset_basic_constraints()
        """
        Common.unset_checkbox_by_row('enabled', 1)

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
    def set_email(cls, email) -> None:
        """
        This method sets the email of the certificate input field.
        :param email: Enter the email address of the person responsible for the Certificate.

        Example:
            - Certificates.set_email('me@example.com')
        """
        Common.set_input_field('email', email)

    @classmethod
    def set_lifetime(cls, number: int):
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
    def set_name(cls, name: str) -> None:
        """
        This method sets the name of the certificate input field.
        :param name: The name of the certificate.

        Example:
            - Certificates.set_name('test')
        """
        Common.set_input_field('name', name)

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
    def unset_add_to_trusted_store_checkbox(cls):
        """
        This method unclick on Add to Trusted Store checkbox.

        Example:
            - Certificates.unset_add_to_trusted_store_checkbox()
        """
        Common.unset_checkbox('add-to-trusted-store')
