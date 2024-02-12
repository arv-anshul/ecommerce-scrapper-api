from typing import Any

from pydantic import BaseModel, field_validator


class AnalyticsData(BaseModel):
    category: str
    subCategory: str | None = None
    superCategory: str
    vertical: str | None = None


class Availability(BaseModel):
    displayState: str
    intent: str
    MessageIntent: str
    showMessage: bool


class Video(BaseModel):
    videoId: str
    videoProvider: str
    videoType: str


class Media(BaseModel):
    images: list
    videos: list[Video] | None = None

    @field_validator("images")
    @classmethod
    def extract_image_urls(cls, v: list) -> list[str]:
        urls = []
        for d in v:
            url = (
                d["url"]
                .replace("{@width}/{@height}", "1000/1000")
                .replace("{@quality}", "100")
            )
            urls.append(url)
        return urls


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
    discount: int | None
    downpaymentRate: int
    downpaymentRequired: bool
    name: str
    priceType: str
    value: int


class Pricing(BaseModel):
    discountAmount: int | None = None
    finalPrice: FinalPrice
    mrp: Mrp
    prices: list[Price]
    totalDiscount: int
    type: str


class Rating(BaseModel):
    average: float
    base: int
    breakup: list[int]
    count: int
    histogramBaseCount: int
    reviewCount: int
    roundOffCount: str | None = None
    type: str


class Titles(BaseModel):
    newTitle: str | None = None
    subtitle: str | None = None
    superTitle: str | None = None
    title: str


class FlipkartSearchPageProductSummaryModel(BaseModel):
    analyticsData: AnalyticsData
    availability: Availability
    baseUrl: str
    dataId: str
    elementId: str
    id: str
    itemId: str
    keySpecs: list[str] | None = None
    listingId: str
    media: Media
    minKeySpecs: list[str] | None = None
    parentId: int
    pricing: Pricing
    productBrand: str
    rating: Rating
    smartUrl: str
    tags: list[str]
    titles: Titles
    type: str
    vertical: str
    warrantySummary: str | None = None

    @field_validator("baseUrl")
    @classmethod
    def validate_baseUrl(cls, v: str) -> str:
        if v is None:
            raise TypeError("baseUrl must be str type.")
        if not v.startswith("/"):
            raise ValueError("baseUrl must startswith '/'.")
        return "https://www.flipkart.com" + v


class FlipkartSearchPageItemList(BaseModel):
    pid: str
    name: str | None = None
    url: str | None = None
