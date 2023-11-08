from typing import Optional

from pydantic import BaseModel


class _ProductSchema(BaseModel):
    aggregateRating: dict
    brand: dict
    image: str
    name: str
    offers: dict


class _ProductOffers(BaseModel):
    """
    IDENTIFIER
    ----------
    `{"type": "OfferSummaryV3Group"}`

    POSITION
    --------
    `pageDataV4 > page > data > 10002 > InList > widget > data > `
    `offerGroups > renderableComponents > InList > value`
    """

    appliedOn: Optional[str] = None
    description: Optional[str] = None
    formattedText: str
    id: Optional[str] = None
    identifier: str
    tags: list[str]
    title: str


class _ProductSpecifications(BaseModel):
    """
    IDENTIFIER
    ----------
    `{"type": "ProductSpecificationValue"}`

    POSITION
    --------
    `pageDataV4 > page > data > 10003 > InList > widget > data > `
    `renderableComponents > InList > value > attributes`
    """

    specifications: list[dict]


class _ProductVariants:
    """
    IDENTIFIER
    ----------
    `{"type": "ProductSwatchValue"}`

    POSITION
    --------
    `pageDataV4 > page > data > 10002 > InList > widget > data > `
    `swatchComponent > value > attributeOptions > InList > InList`
    """


class FlipkartProductInfo(BaseModel):
    schemas: Optional[_ProductSchema]
    offers: Optional[list[_ProductOffers]]
    specs: Optional[list[_ProductSpecifications]]
    variants: Optional[dict[str, list[str]]]
