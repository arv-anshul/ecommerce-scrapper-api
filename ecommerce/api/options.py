from enum import Enum


class WebsiteOptions(Enum):
    flipkart = "flipkart"
    amazon = "amazon"


class CurlTypeOptions(Enum):
    searchPage = "searchPage"
    productPage = "productPage"
