import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.directory_services import Directory_Services as DS


@pytest.mark.parametrize('ldap', get_data_list('ldap_credentials'), scope='class')
class Test_Disable_LDAP:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, ldap) -> None:
        """
        This test verifies ldap can be setup
        """
        DS.click_configure_ldap_button()
        assert DS.assert_ldap_edit_panel() is True
        COM.set_input_field('hostname', ldap['domain'])
        COM.set_input_field('basedn', ldap['basedn'])
        COM.set_input_field('binddn', ldap['binddn'])
        COM.set_input_field('bindpw', ldap['bindpassword'])
        COM.set_checkbox('enable')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_dialog_not_visible('Setting up LDAP') is True
        assert DS.assert_directory_services_page_header() is True
        # verify the values of ldap
        assert DS.assert_ldap_card() is True
        assert COM.get_label_value('Status:') == 'HEALTHY'
        assert COM.get_label_value('Hostname:') == ldap['domain']
        assert COM.get_label_value('Base DN:') == ldap['basedn']
        assert COM.get_label_value('Bind DN:') == ldap['binddn']

    @staticmethod
    def verify_ldap_disabled() -> None:
        """
        This test verifies the ldap is disabled
        """
        DS.click_ldap_settings_button()
        COM.unset_checkbox('enable')
        COM.click_save_button()
        assert COM.is_card_not_visible('LDAP') is True
        assert DS.is_ldap_configure_button_visible() is True

    @pytest.fixture(scope='function', autouse=True)
    def teardown_class(self) -> None:
        """
        This test removes the ldap
        """
        # reset the change
        yield
        DS.remove_ldap()
