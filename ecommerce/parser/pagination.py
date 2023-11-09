from typing import Iterator, Sequence

from ecommerce import types
from ecommerce.core.errors import PaginationError


def _is_continuous(seq: Sequence, /) -> bool:
    """Returns True if the passed sequence is continuous, False otherwise.

    Args:
      seq: A sequence of numbers.

    Returns:
      A boolean value indicating whether the sequence is continuous.
    """
    prev = seq[0]
    for item in seq[1:]:
        if item != prev + 1:
            return False
        prev = item
    return True


class Pagination:
    def __init__(self, pages: types.PagesLike = range(1, 6), /) -> None:
        self.__validate_pages_arg(pages)
        self.pages = list(pages)

    def __validate_pages_arg(self, pages) -> None:
        if any(i for i in pages if i < 0):
            error_msg = "Pages must be positive."
        elif 0 in pages:
            error_msg = "0 is prohibited."
        elif not pages:
            error_msg = "Please pass at least 1 page."
        elif pages[0] > pages[-1]:
            error_msg = "Pages must be in ascending order."
        elif _is_continuous(pages) is False:
            error_msg = "Pages must be continuous."
        else:
            error_msg = None
        if error_msg:
            raise PaginationError(error_msg)

    def __str__(self) -> str:
        return (
            f"OnePage[1]({self.pages[0]})"
            if len(self.pages) == 1
            else f"PageRange[{len(self.pages)}]({self.pages[0]}, {self.pages[-1]})"
        )

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator[int]:
        for i in self.pages:
            yield i

    def __len__(self) -> int:
        return len(self.pages)

    def update_pages(self, pages: types.PagesLike) -> None:
        if _is_continuous(pages) is False:
            raise PaginationError("Pages must be continuous.")
        self.pages = list(pages)

    def remove_first_n(self, n: int, /) -> None:
        new_pages = self.pages[n:]
        if not new_pages:
            raise PaginationError(
                f"{self.__class__.__name__!r} object must not be empty."
            )
        self.pages = new_pages

    def remove_last_n(self, n: int, /) -> None:
        new_pages = self.pages[:-n]
        if not new_pages:
            raise PaginationError(
                f"{self.__class__.__name__!r} object must not be empty."
            )
        self.pages = new_pages

    def add_next_n_pages(self, n: int, /) -> None:
        self.pages.extend([self.pages[-1] + i for i in range(1, n + 1)])

    def add_prev_n_pages(self, n: int, /) -> None:
        new_pages = [self.pages[0] - i for i in range(1, n + 1)][::-1]
        if any([i for i in new_pages if i < 0]):
            raise PaginationError("Pages must be positive.")
        self.pages = new_pages + self.pages
