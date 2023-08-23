from typing import List, Optional
from pydantic import (
    AliasChoices,
    AliasPath,
    BaseModel,
    Field,
    field_validator,
    model_validator,
)

from shapely.geometry import Polygon, Point, LineString, LinearRing


class RectShape(BaseModel):
    """
    for normal rectangle shape gis data
    sw : south west
    ne : north east
    xmin : min longitude of rectangle, generally south west
    ymin : min latitude of rectangle, generally south west
    xmax : max longitude of rectangle, generally north east
    ymax : max latitude of rectangle, generally north east
    """

    ## 위도(lat) y축, 경도(lng) x축

    xmin: float = Field(
        AliasChoices("sw", AliasPath("bbox", 0)),
        description="min longitude of rectangle, generally south west",
    )
    ymin: float = Field(
        AliasChoices("sw", AliasPath("bbox", 1)),
        description="min latitude of rectangle, generally south west",
    )
    xmax: float = Field(
        AliasChoices("ne", AliasPath("bbox", 0)),
        description="max longitude of rectangle, generally north east",
    )
    ymax: float = Field(
        AliasChoices("ne", AliasPath("bbox", 1)),
        description="max latitude of rectangle, generally north east",
    )

    @model_validator(mode="after")
    def check_bbox(self, values):
        if self.xmin > 90 or self.xmin < -90:
            self.xmin, self.ymin = self.ymin, self.xmin  ## swap
        if self.xmax > 90 or self.xmax < -90:
            self.xmax, self.ymax = self.ymax, self.xmax
        if self.ymin > 180 or self.ymin < -180:
            raise ValueError("min latitude must be in range [-180, 180]")
        if self.ymax > 180 or self.ymax < -180:
            raise ValueError("max latitude must be in range [-180, 180]")


class CircleShape(BaseModel):
    """
    for circle shape gis data
    center : center of circle
    radius : radius of circle
    """

    x: Optional[float] = Field(
        validation_alias=AliasChoices("x", AliasPath("center", 0)),
        description="longitude",
    )
    y: Optional[float] = Field(
        validation_alias=AliasChoices("y", AliasPath("center", 1)),
        description="latitude",
    )
    radius: float = Field(description="radius of circle, unit is meter")

    @model_validator(mode="after")
    def check_center(self, values):
        if self.x >= 90 or self.x <= -90:  ## x = lng
            self.x, self.y = self.y, self.x  ## swap
        if self.y >= 180 or self.y <= -180:
            raise ValueError("longitude must be in range [-180, 180]")
        return self

    @property
    def polygon(self):
        return Point(self.x, self.y).buffer(self.radius)
