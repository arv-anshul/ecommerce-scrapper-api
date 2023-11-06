from typing import Any, Optional

from pydantic import BaseModel, field_validator


class AnalyticsData(BaseModel):
    category: str
    subCategory: str
    superCategory: str
    vertical: str


class Availability(BaseModel):
    displayState: str
    intent: str
    MessageIntent: str
    showMessage: bool


class Image(BaseModel):
    aspectRatio: Any
    contentInfo: Any
    height: Any
    url: str
    width: Any


class Video(BaseModel):
    height: Any
    videoId: str
    videoProvider: str
    videoType: str
    width: Any


class Media(BaseModel):
    images: list[Image]
    videos: Optional[list[Video]] = None


class FinalPrice(BaseModel):
    additionalText: Any
    currency: str
    decimalValue: str
    discount: Any
    downpaymentRate: int
    downpaymentRequired: bool
    name: str
    value: int


class Mrp(BaseModel):
    additionalText: str
    currency: str
    decimalValue: str
    discount: Any
    downpaymentRate: int
    downpaymentRequired: bool
    name: str
    value: int


class Price(BaseModel):
    additionalText: Any
    currency: str
    decimalValue: str
    discount: Optional[int]
    downpaymentRate: int
    downpaymentRequired: bool
    name: str
    priceType: str
    value: int


class Pricing(BaseModel):
    discountAmount: Optional[int] = None
    finalPrice: FinalPrice
    mrp: Mrp
    prices: list[Price]
    totalDiscount: int
    type: str


class ProductCardImage(BaseModel):
    dynamicImageUrl: str
    height: int
    type: str
    width: int


class ProductCardTagDetail(BaseModel):
    image: ProductCardImage
    type: str


class Rating(BaseModel):
    average: float
    base: int
    breakup: list[int]
    count: int
    histogramBaseCount: int
    reviewCount: int
    roundOffCount: str
    type: str


class Titles(BaseModel):
    newTitle: str
    subtitle: Optional[str] = None
    superTitle: str
    title: str


class FlipkartSearchPageProductSummaryModel(BaseModel):
    analyticsData: AnalyticsData
    availability: Availability
    baseUrl: str
    dataId: str
    elementId: str
    id: str
    itemId: str
    keySpecs: list[str]
    listingId: str
    media: Media
    minKeySpecs: list[str]
    parentId: int
    pricing: Pricing
    productBrand: str
    productCardTagDetails: list[ProductCardTagDetail]
    rating: Rating
    smartUrl: str
    tags: list[str]
    titles: Titles
    type: str
    vertical: str
    warrantySummary: str

    @field_validator("baseUrl")
    @classmethod
    def validate_baseUrl(cls, v: str) -> str:
        if v is None:
            raise TypeError("baseUrl must be str type.")
        if not v.startswith("/"):
            raise ValueError("baseUrl must startswith '/'.")
        return "https://www.flipkart.com" + v
