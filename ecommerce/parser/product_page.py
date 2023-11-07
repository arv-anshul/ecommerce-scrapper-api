from abc import ABC, abstractmethod


class BaseProductPageHTMLParser(ABC):
    @property
    @abstractmethod
    def get_cached_html_pages(self):
        ...

    @abstractmethod
    async def get_html_page(self):
        ...
