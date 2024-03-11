import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.directory_services import Directory_Services as DS


@pytest.mark.parametrize('ldap', get_data_list('ldap_credentials'), scope='class')
class Test_Disable_LDAP:

    @staticmethod
    def test_setup_ldap(ldap) -> None:
        """
        This test verifies ldap can be setup
        """
        DS.click_configure_ldap_button()
        assert DS.assert_ldap_card()
        COM.set_input_field('hostname', ldap['domain'])
        COM.set_input_field('basedn', ldap['basedn'])
        COM.set_input_field('binddn', ldap['binddn'])
        COM.set_input_field('bindpw', ldap['bindpassword'])
        COM.set_checkbox('enable')
        COM.click_save_button()
        assert DS.assert_directory_services_page_header()

    @staticmethod
    def verify_ldap_disabled(ldap) -> None:
        """
        This test verifies the ldap is disabled
        """
        DS.click_ldap_settings_button()
        COM.unset_checkbox('enable')
        COM.click_save_button()
        assert COM.is_card_not_visible('LDAP')
        assert COM.is_visible('//*[@data-test="button-configure-ldap"]')

    @pytest.fixture(scope='class', autouse=True)
    def teardown_class(self) -> None:
        """
        This test removes the ldap
        """
        # reset the change
        DS.remove_ldap()
