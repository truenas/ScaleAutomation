import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from helper.api import Response


class Common_Shares:
    @classmethod
    def assert_share_card_displays(cls, sharetype: str) -> bool:
        """
        This method returns True if the share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the share card is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//ix-{sharetype}-card'))

    @classmethod
    def assert_share_description(cls, sharetype: str, desc: str) -> bool:
        """
        This method sets the description for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param desc: description of the given share
        :return: True if the share description is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'description', desc))

    @classmethod
    def assert_share_name(cls, sharetype: str, name: str) -> bool:
        """
        This method sets the name for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'name', name))

    @classmethod
    def assert_share_path(cls, sharetype: str, path: str) -> bool:
        """
        This method sets the path for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'path', path))

    @classmethod
    def click_advanced_options(cls) -> None:
        """
        This method clicks the advanced options button.
        """
        assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-options'))
        COM.click_button('toggle-advanced-options')

    @classmethod
    def click_delete_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the delete share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-delete-row-action'
        WebUI.xpath(xpaths.common_xpaths.button_field(path)).click()

    @classmethod
    def click_edit_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the edit share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-edit-row-action'
        WebUI.xpath(xpaths.common_xpaths.button_field(path)).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit {sharetype.upper()}', 3))

    @classmethod
    def create_share_by_api(cls, sharetype: str, name: str, path: str) -> Response:
        """
        This method creates the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_POST.create_share(sharetype, name, "/mnt/"+path)

    @classmethod
    def delete_share_by_api(cls, sharetype: str, name: str) -> Response:
        """
        This method deletes the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_DELETE.delete_share(sharetype, name)

    @classmethod
    def is_share_enabled(cls, sharetype: str, name: str) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share is enabled otherwise it returns False.
        """
        return bool(WebUI.xpath(xpaths.common_xpaths.share_enabled_slider(sharetype, name)).get_property('ariaChecked'))

    @classmethod
    def is_share_visible(cls, sharetype: str, name: str) -> bool:
        """
        This method return True if the given share is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.data_test_field(f'text-name-card-{sharetype}-share-{name.lower()}-row-text'))

    @classmethod
    def set_share_description(cls, desc: str) -> None:
        """
        This method sets the description for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('comment'))
        COM.set_input_field('comment', desc)

    @classmethod
    def set_share_name(cls, name: str) -> None:
        """
        This method sets the name for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('name'))
        COM.set_input_field('name', name)

    @classmethod
    def set_share_path(cls, path: str) -> None:
        """
        This method sets the path for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('path'))
        COM.set_input_field('path', '/mnt/'+path)
