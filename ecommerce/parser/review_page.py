from abc import ABC, abstractmethod


class BaseReviewPageHTMLParser(ABC):
    @abstractmethod
    async def get_html_pages(self):
        ...

    @abstractmethod
    async def get_reviews(self):
        ...

    @abstractmethod
    async def parse_all_reviews(self):
        ...
