from abc import ABC, abstractmethod


class BaseSearchPageHTMLParser(ABC):
    @property
    @abstractmethod
    def urls(self):
        ...

    @abstractmethod
    async def get_html_pages(self):
        ...

    @staticmethod
    @abstractmethod
    async def get_ProductSummary():
        ...

    @abstractmethod
    async def parse_all_PageData(self):
        ...

    @abstractmethod
    async def parse_all_ProductSummary(self):
        ...
