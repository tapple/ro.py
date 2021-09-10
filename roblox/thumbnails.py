from enum import Enum
from typing import Optional, List
from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject


class ThumbnailState(Enum):
    """
    The current state of the thumbnail.
    """

    completed = "Completed"
    in_review = "InReview"
    pending = "Pending"
    error = "Error"
    moderated = "Moderated"
    blocked = "Blocked"


class ThumbnailReturnPolicy(Enum):
    """
    The return policy for place/universe thumbnails.
    """

    place_holder = "PlaceHolder"
    auto_generated = "AutoGenerated"
    force_auto_generated = "ForceAutoGenerated"


class ThumbnailFormat(Enum):
    """
    Format returned by the endpoint.
    """

    png = "Png"
    jpeg = "Jpeg"


class AvatarThumbnailType(Enum):
    """
    Type of avatar thumbnail.
    """

    full_body = 1
    headshot = 2
    bust = 3


class Thumbnail:
    """
    Represents a Roblox thumbnail as returned by almost all endpoints on https://thumbnails.roblox.com/.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The data form the request.
        target_id: The id of the target of the image.
        state: The current state of the image.
        image_url: Url of the image.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.target_id: int = data["targetId"]
        self.state: ThumbnailState = ThumbnailState(data["state"])
        self.image_url: Optional[str] = data["imageUrl"]


class UniverseThumbnails:
    """
    Represents a universe's thumbnails as returned by https://thumbnails.roblox.com/v1/games/multiget/thumbnails.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The data form the request.
        universe_id: The id of the target of the image.
        error: The errors you got.
        thumbnails: List of thumbnails.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data
        # todo add base universe maby
        self.universe_id: int = data["universeId"]
        self.error: Optional[str] = data["error"]
        self.thumbnails: List[Thumbnail] = [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in data["thumbnails"]
        ]


class ThumbnailProvider:
    """
    The ThumbnailProvider is an object that represents https://thumbnails.roblox.com/ and provides multiple functions for generating user thumbnails.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject):
        """
        Arguments:
            shared: Shared object.
        """
        self._shared: ClientSharedObject = shared

    async def get_asset_thumbnails(
            self,
            asset_ids: List[int],
            return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
            # TODO MAKE SIZE ENUM
            size: str = "30x30",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns asset thumbnails for the asset ID passed.

        Arguments:
            asset_ids: Id of the asset you want the thumbnails of.
            return_policy: How you want it returns look at enum.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/assets"),
            params={
                "assetIds": asset_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_asset_thumbnail_3d(self, asset_id: int) -> Thumbnail:
        """
        Returns a 3d asset thumbnail for the user ID passed.

        Arguments:
            asset_id: Id of the asset you want the thumbnails of.

        Returns:
            A Thumbnail.
        """
        thumbnail_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/assets-thumbnail-3d"
            ),
            params={"assetId": asset_id},
        )
        thumbnail_data = thumbnail_response.json()
        return Thumbnail(shared=self._shared, data=thumbnail_data)

    async def get_badge_icons(
            self,
            badge_ids: List[int],
            size: str = "150x150",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns badge icons for each badge ID passed.

        Arguments:
            badge_ids: Id of the badge you want the thumbnails of.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/badges/icons"),
            params={
                "badgeIds": badge_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_bundle_thumbnails(
            self,
            bundle_ids: List[int],
            size: str = "150x150",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns bundle thumbnails for each bundle ID passed.

        Arguments:
            badge_ids: Id of the badge you want the thumbnails of.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/bundles/thumbnails"
            ),
            params={
                "bundleIds": bundle_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_gamepass_icons(
            self,
            gamepass_ids: List[int],
            # TODO Make size enum
            size: str = "150x150",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns gamepass icons for each gamepass ID passed.

        Arguments:
            gamepass_ids: Id of the gamepass you want the thumbnails of.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/game-passes"),
            params={
                "gamePassIds": gamepass_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_universe_icons(
            self,
            universe_ids: List[int],
            return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
            size: str = "50x50",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns universe icons for each universe ID passed.

        Arguments:
            universe_ids: Id of the universe you want the thumbnails of.
            return_policy: How you want it returns look at enum.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/games/icons"),
            params={
                "universeIds": universe_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_universe_thumbnails(
            self,
            universe_ids: List[int],
            size: str = "768x432",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
            count_per_universe: int = None,
            defaults: bool = None,
    ) -> List[UniverseThumbnails]:
        """
        Returns universe thumbnails for each universe ID passed.

        Arguments:
            universe_ids: Id of the universe you want the thumbnails of.
            size: size of the image.
            format: Format of the image.
            count_per_universe: Unknown.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/games/multiget/thumbnails"
            ),
            params={
                "universeIds": universe_ids,
                "countPerUniverse": count_per_universe,
                "defaults": defaults,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            UniverseThumbnails(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_group_icons(
            self,
            group_ids: List[int],
            size: str = "150x150",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns icons for each group ID passed.

        Arguments:
            group_ids: Id of the groups you want the thumbnails of.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/groups/icons"),
            params={
                "groupIds": group_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_place_icons(
            self,
            place_ids: List[int],
            return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
            size: str = "50x50",
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns icons for each place ID passed.

        Arguments:
            place_ids: Id of the places you want the thumbnails of.
            return_policy: How you want it returns look at enum.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.
        Returns:
            A List of Thumbnails.
        """
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/places/gameicons"),
            params={
                "placeIds": place_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_user_avatars(
            self,
            user_ids: List[int],
            type: AvatarThumbnailType = AvatarThumbnailType.full_body,
            size: str = None,
            format: ThumbnailFormat = ThumbnailFormat.png,
            is_circular: bool = False,
    ) -> List[Thumbnail]:
        """
        Returns avatars for each user ID passed.

        Arguments:
            user_ids: Id of the users you want the thumbnails of.
            type: Type of avatar thumbnail you want look at enum.
            size: size of the image.
            format: Format of the image.
            is_circular: if the image is a circle yes or no.

        Returns:
            A List of Thumbnails.
        """
        uri: str
        if type == AvatarThumbnailType.full_body:
            uri = "avatar"
            size = size or "30x30"
        elif type == AvatarThumbnailType.bust:
            uri = "avatar-bust"
            size = size or "48x48"
        elif type == AvatarThumbnailType.headshot:
            uri = "avatar-headshot"
            size = size or "48x48"
        else:
            raise ValueError("Avatar type is invalid.")

        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", f"v1/users/{uri}"),
            params={
                "userIds": user_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )

        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_user_avatar_3d(self, user_id: int) -> Thumbnail:
        """
        Returns the user's thumbnail in 3d.
        TODO: Add special 3d features

        Arguments:
            user_id: Id of the user you want the 3d thumbnail of.

        Returns:
            A Thumbnail.
        """
        thumbnail_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/users/avatar-3d"),
            params={"userId": user_id},
        )
        thumbnail_data = thumbnail_response.json()
        return Thumbnail(shared=self._shared, data=thumbnail_data)
