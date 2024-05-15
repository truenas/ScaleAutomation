import allure
import pytest

from keywords.webui.dashboard import Dashboard


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('CPU Card')
class Test_Verify_CPU_Card_Text:

    @allure.tag("Read")
    @allure.story('CPU Card Text and Graph')
    def test_verifying_cpu_load_and_cpu_load_graph_text(self):
        """
        This test verifies CPU Card Info
        """
        # verify cpu load text
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_cpu_card_visible() is True
        assert Dashboard.assert_cpu_card_load_text(1, "Cores") is True
        assert Dashboard.assert_cpu_card_load_text(2, "Highest Usage") is True
        assert Dashboard.assert_cpu_card_load_text(3, "Hottest") is True

        # Verify CPU load graph
        assert Dashboard.assert_cpu_card_load_graph_text() is True
        assert Dashboard.assert_cpu_card_load_graph_ui() is True
