import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Permission:
    @classmethod
    def set_dataset_owner(cls, owner: str) -> None:
        """
        This method sets the ACL Owner for the share on the Edit ACL page
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner'))
        COM.set_input_field('owner', owner, True)

    @classmethod
    def set_dataset_owner_group(cls, group: str) -> None:
        """
        This method sets the ACL group for the share on the Edit ACL page
        """
        COM.is_visible(xpaths.common_xpaths.input_field('owner-group'))
        COM.set_input_field('owner-group', group, True)

