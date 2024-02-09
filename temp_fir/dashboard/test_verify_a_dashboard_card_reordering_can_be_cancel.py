from keywords.webui.dashboard import Dashboard


class Test_Verify_A_Dashboard_Card_Reordering_Can_be_Cancel:

    @staticmethod
    def on_the_dashboard_move_the_help_card_to_cpu_card_position_and_cancel():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(2, 'help')
        assert Dashboard.assert_card_position(3, 'cpu')
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('help', 'cpu')
        assert Dashboard.assert_card_position(3, 'help')
        assert Dashboard.assert_card_position(2, 'cpu')
        Dashboard.click_the_cancel_reorder_button()

    @staticmethod
    def verify_the_system_the_help_card_to_cpu_card_position_did_not_change_after_the_cancellation():
        assert Dashboard.assert_card_position(2, 'help')
        assert Dashboard.assert_card_position(3, 'cpu')
