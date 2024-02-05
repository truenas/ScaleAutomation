import xpaths
from keywords.webui.common import Common as COM


class NFS:

    @classmethod
    def assert_error_nfs_share_path_nonexistant(cls):
        """
        This method returns True if 'This path does not exist.' error message is visible, otherwise it returns False.

        :return: True if 'This path does not exist.' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This path does not exist.'))
