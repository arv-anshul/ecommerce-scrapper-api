from datetime import date

from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    city: str
    state: str
    type: str


class _ProductDetails(BaseModel):
    baseUrl: str
    id: str
    itemId: str

    @field_validator("baseUrl")
    @classmethod
    def extract_productUrl(cls, v: str) -> str:
        return "https://www.flipkart.com" + v


class FlipkartProductReviews(BaseModel):
    author: str
    certifiedBuyer: bool
    created: str
    dateOfStoring: date = Field(default_factory=date.today)
    helpfulCount: int
    images: list
    location: Location
    rating: int
    text: str
    title: str
    totalCount: int
    url: str
    productDetails: _ProductDetails

    @field_validator("images")
    @classmethod
    def update_images(cls, v: list[dict]) -> list[str]:
        images = [i["value"]["imageURL"] for i in v]
        images = [
            i.replace("{@width}/{@height}", "1000/1000").replace("{@quality}", "100")
            for i in images
        ]
        return images
