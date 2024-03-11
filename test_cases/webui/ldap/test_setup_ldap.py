import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.directory_services import Directory_Services as DS


@pytest.mark.parametrize('ldap', get_data_list('ldap_credentials'), scope='class')
class Test_Setup_LDAP:

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
    def verify_ldap_values(ldap) -> None:
        """
        This test verifies the setup values of ldap
        """
        assert DS.assert_ldap_card()
        assert COM.get_label_value('Status:') == 'HEALTHY'
        assert COM.get_label_value('Hostname:') == ldap['domain']
        assert COM.get_label_value('Base DN:') == ldap['basedn']
        assert COM.get_label_value('Bind DN:') == ldap['binddn']

    @pytest.fixture(scope='class', autouse=True)
    def teardown_class(self) -> None:
        """
        This test removes the ldap
        """
        # reset the change
        DS.remove_ldap()
