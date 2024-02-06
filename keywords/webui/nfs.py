import xpaths
from keywords.webui.common import Common as COM


class NFS:

    @classmethod
    def assert_error_nfs_share_path_duplicate(cls, sharepath: str):
        """
        This method returns True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.

        :param sharepath: The path of the share
        :return: True if 'ERROR - Export conflict.....' error message is visible, otherwise it returns False.
        """
        # TODO - Update with proper message when it is implemented.
        #   NAS-127220 - The Error Message For A Duplicate NFS Share Needs Clarification
        return COM.is_visible(xpaths.common_xpaths.any_text(f'ERROR - Export conflict. This share is exported to everybody and another share exports {sharepath} for'))

    @classmethod
    def assert_error_nfs_share_path_nonexistant(cls):
        """
        This method returns True if 'This path does not exist.' error message is visible, otherwise it returns False.

        :return: True if 'This path does not exist.' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('This path does not exist.'))

    @classmethod
    def assert_error_nfs_share_path_required(cls):
        """
        This method returns True if 'Path is required' error message is visible, otherwise it returns False.

        :return: True if 'Path is required' error message is visible, otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Path is required'))
