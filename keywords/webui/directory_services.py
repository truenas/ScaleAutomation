import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from selenium.webdriver.common.keys import Keys


class Directory_Services:

    @classmethod
    def assert_directory_services_page_header(cls) -> bool:
        """
        This method returns True if the Directory Services page is displayed, otherwise False

        :return: is the name of the service to start
        """
        return COM.assert_page_header('Directory Services')

    @classmethod
    def assert_ldap_card(cls) -> bool:
        """
        This method returns True if the Directory Services page is displayed, otherwise False

        :return: is the name of the service to start
        """
        return COM.is_visible(xpaths.common_xpaths.any_header('LDAP', 3))

    @classmethod
    def click_configure_ldap_button(cls) -> None:
        """
        This method clicks the configure ldap button
        """
        COM.click_button('configure-ldap')

    @classmethod
    def click_ldap_settings_button(cls) -> None:
        """
        This method clicks the configure ldap button
        """
        COM.click_button('ldap-settings')

    @classmethod
    def remove_ldap(cls) -> None:
        """
        This method removes the existing ldap configuration
        """
        cls.click_ldap_settings_button()
        while COM.is_visible('//mat-chip-row//*[@name="cancel"]'):
            COM.delete_pill('//mat-chip-row')
        while COM.is_visible('//*[@name="mdi-close-circle"]'):
            COM.click_on_element('//*[@name="mdi-close-circle"]')
        COM.clear_input_field('bindpw')
        COM.unset_checkbox('enable')
        COM.click_save_button()
        assert COM.is_card_not_visible('LDAP')
        assert COM.is_visible('//*[@data-test="button-configure-ldap"]')
