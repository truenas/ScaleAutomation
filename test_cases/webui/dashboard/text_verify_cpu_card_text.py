from keywords.webui.dashboard import Dashboard


class Test_Verify_CPU_Card_Text:
    @staticmethod
    def on_the_dashboard_verify_cpu_load_text():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_cpu_card_visible()
        assert Dashboard.assert_cpu_card_load_text(1, "Cores")
        assert Dashboard.assert_cpu_card_load_text(2, "Highest Usage")
        assert Dashboard.assert_cpu_card_load_text(3, "Hottest")

    @staticmethod
    def then_verify_cpu_load_graph():
        assert Dashboard.assert_cpu_card_load_graph_text()
        assert Dashboard.assert_cpu_card_load_graph_ui()
