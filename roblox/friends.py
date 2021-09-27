from .utilities.shared import ClientSharedObject

from .users import User


class Friend(User):
    """
    Represents a friend.

    Attributes:
        is_online: Whether the user is currently online.
        presence_type: Their presence type. Don't use this.
        is_deleted: Whether the account is deleted.
        friend_frequent_rank: Unknown
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            data: The data we get back from the endpoint.
            shared: The shared object, which is passed to all objects this client generates.
        """
        super().__init__(shared=shared, data=data)

        self.is_online: bool = data["isOnline"]
        self.presence_type: int = data["presenceType"]
        self.is_deleted: bool = data["isDeleted"]
        self.friend_frequent_rank: int = data["friendFrequentRank"]