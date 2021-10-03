from typing import Optional


class UserPromotionChannels:
    """
    Represents a user's promotion channels.

    Attributes:
        facebook: A link to the user's Facebook profile.
        twitter: A Twitter handle.
        youtube: A link to the user's YouTube channel.
        twitch: A link to the user's Twitch channel.
    """

    def __init__(self, data: dict):
        self.facebook: Optional[str] = data["facebook"]
        self.twitter: Optional[str] = data["twitter"]
        self.youtube: Optional[str] = data["youtube"]
        self.twitch: Optional[str] = data["twitch"]