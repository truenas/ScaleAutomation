import allure
from keywords.webui.dashboard import Dashboard


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('CPU Card')
class Test_Verify_CPU_Card_Text:
    @allure.story('CPU Card Text and Graph')
    def test_verifying_cpu_load_and_cpu_load_graph_text(self):
        # verify cpu load text
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_cpu_card_visible()
        assert Dashboard.assert_cpu_card_load_text(1, "Cores")
        assert Dashboard.assert_cpu_card_load_text(2, "Highest Usage")
        assert Dashboard.assert_cpu_card_load_text(3, "Hottest")
        # Verify CPU load graph
        assert Dashboard.assert_cpu_card_load_graph_text()
        assert Dashboard.assert_cpu_card_load_graph_ui()
