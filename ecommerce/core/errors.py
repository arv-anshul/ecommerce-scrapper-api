from typing import Type


def RaiseWithExtraMsg(
    c__: Exception,
    e__: Type[Exception],
    msg__: object,
    /,
) -> Exception:
    """
    Raise caught exception extra message.

    Args:
        c__: Caught exception.
        e__: New exception to be raise.
        msg__: Extra message.

    Return:
        `e__` exception with extra message in it.
        It also contains message from caught exception.
    """

    return e__(
        {
            "message": msg__,
            "mainErrorDetail": {
                "type": c__.__class__.__name__,
                "message": str(c__),
            },
        }
    )


class PaginationError(ValueError):
    """Exception for pagination."""


class SearchPageError(Exception):
    """Exception for SearchPages of websites."""


class ReviewPageError(Exception):
    """Exception for ReviewPages of websites."""
