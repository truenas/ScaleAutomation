from keywords.webui.login_page_ui import Login_Page_Ui as LPU
from keywords.webui.common import Common as COM
from helper.global_config import private_config


def test_login_page_ui():
    COM.navigate_to_login_screen(private_config['IP'])
    assert COM.assert_copyright_text_is_correct() is True
    assert LPU.assert_password_visibility_button_toggles_off_to_on() is True
    assert LPU.assert_password_visibility_button_toggles_on_to_off() is True
    assert LPU.assert_text_doesnt_affect_password_visibility_button() is True
    assert LPU.assert_error_username_requirement_doesnt_display_on_page_load() is True
    assert LPU.assert_error_password_requirement_doesnt_display_on_page_load() is True
    assert LPU.assert_error_username_requirement_displays_after_deselection() is False
    assert LPU.assert_error_password_requirement_displays_after_deselection() is False
    assert LPU.assert_error_username_requirement_doesnt_display("admin") is True
    assert LPU.assert_error_password_requirement_doesnt_display("aaaa") is True
    assert LPU.assert_error_username_requirement_displays_after_login_attempt() is True
    assert LPU.assert_error_username_requirement_after_login_attempt_displays_after_reselection() is True
    assert LPU.assert_truenas_icon_displays() is True
    assert LPU.assert_ixsystems_icon_displays() is True
    assert LPU.assert_background_image_displays() is True
    assert LPU.assert_ixsystems_link_is_correct() is True
