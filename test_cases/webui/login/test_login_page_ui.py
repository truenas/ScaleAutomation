import allure
from helper.webui import WebUI
from keywords.webui.login_page_ui import Login_Page_Ui as LPU
from keywords.webui.common import Common as COM
from helper.global_config import private_config


class Test_Login_Page_UI:
    @classmethod
    def setup_class(cls):
        COM.logoff_truenas()

    @classmethod
    def teardown_class(cls):
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])

    @allure.tag('Read', 'Percy', "NAS-129711")
    @allure.issue('NAS-129860', 'NAS-129860')
    def test_login_page_ui(self):
        """
        This test asserts the UI of the login page
        """
        # Per https://ixsystems.atlassian.net/browse/NAS-129711, the copyright text should no-longer display.
        assert COM.assert_copyright_text_is_correct() is False
        WebUI.take_percy_snapshot('Login Page UI')
        assert LPU.assert_password_visibility_button_toggles_off_to_on() is True
        assert LPU.assert_password_visibility_button_toggles_on_to_off() is True
        assert LPU.assert_text_doesnt_affect_password_visibility_button() is True
        assert LPU.assert_error_username_requirement_doesnt_display_on_page_load() is True
        assert LPU.assert_error_password_requirement_doesnt_display_on_page_load() is True
        assert LPU.assert_error_username_requirement_displays_after_deselection() is False
        assert LPU.assert_error_password_requirement_displays_after_deselection() is False
        assert LPU.assert_error_username_requirement_doesnt_display("admin") is True
        assert LPU.assert_error_password_requirement_doesnt_display("aaaa") is True
        assert LPU.assert_error_username_requirement_displays_after_login_attempt() is False
        assert LPU.assert_error_username_requirement_after_login_attempt_displays_after_reselection() is False
        assert LPU.assert_truenas_icon_displays() is True
        assert LPU.assert_ixsystems_icon_displays() is True
        assert LPU.assert_background_image_displays() is True
        # Expected failure below: https://ixsystems.atlassian.net/browse/NAS-129860
        assert LPU.assert_ixsystems_link_is_correct() is True

