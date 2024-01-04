from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.common import Common


class Test_Verify_Links_On_The_TrueNAS_Help_Card:
    @classmethod
    def setup_class(cls):
        # Ensure we are on the dashboard.
        Navigation.navigate_to_dashboard()

    @staticmethod
    def on_the_dashboard_verify_the_truenas_help_card_copyright():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_truenas_help_card_visible()
        assert Common.assert_copyright_text_is_correct()

    @staticmethod
    def verify_all_links_on_the_truenas_help_card():
        assert Dashboard.assert_the_truenas_help_documentation_link() is True
        assert Dashboard.assert_the_truenas_help_truenas_community_forums_link() is True
        assert Dashboard.assert_the_truenas_help_truenas_newsletter_link() is True
        assert Dashboard.assert_the_truenas_help_open_source_link() is True
        assert Dashboard.assert_the_truenas_help_ixsystems_inc_link() is True
