from keywords.webui.common import Common as COM


class Common_Replication:

    @classmethod
    def set_direction(cls, direction: str) -> None:
        """
        This method sets the rsync direction

        :param direction: is the direction [push/pull]

        Example:
            - Common_Replication.set_direction('push')
        """
        COM.select_option('direction', 'direction-' + COM.convert_to_tag_format(direction))

    @classmethod
    def set_direction_pull(cls) -> None:
        """
        This method sets the rsync direction to pull

        Example:
            - Common_Replication.set_direction_pull()
        """
        cls.set_direction('pull')

    @classmethod
    def set_direction_push(cls) -> None:
        """
        This method sets the rsync direction to push

        Example:
            - Common_Replication.set_direction_push()
        """
        cls.set_direction('push')
