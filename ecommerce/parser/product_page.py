from abc import ABC, abstractmethod


class BaseProductPageHTMLParser(ABC):
    @abstractmethod
    async def get_html_page(self):
        ...

    @staticmethod
    @abstractmethod
    async def get_ProductInfo():
        ...

    @staticmethod
    @abstractmethod
    async def batch_products_info():
        ...
