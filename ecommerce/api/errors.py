import functools
from asyncio import iscoroutinefunction
from typing import Any

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ecommerce.logger import get_logger

logger = get_logger(__name__)


class APIExceptionResponder:
    """
    Default `status_code` is **400**.

    Change `status_code` while raising a exception explicitly.

    Example
    -------
    >>> try:
    >>>     # Do something... 👍
    >>> except:
    >>>     APIExceptionResponder.status_code = 422
    >>>     raise ValueError("Some Error Occurred! 🙏")
    >>> # This sends the http response with "422" status code.

    `NOTE`
        After sending the errored response the `status_code` will be resets to **400**.
    """

    status_code: int = 400
    content: Any = None

    @classmethod
    def update_variables(cls, status_code: int, content: Any = None) -> None:
        cls.status_code = status_code
        cls.content = content

    @classmethod
    def reset_variables(cls) -> None:
        """Reset the class variables to its default values."""
        cls.status_code = 400
        cls.content = None

    @classmethod
    def better_api_error_response(cls, func):
        """
        Catches all errors and return them as `fastapi.response.JSONResponse`
        with **400** status code.

        >>> JSONResponse(
        ...     content={"message": str(e), "errorType": e.__class__.__name__},
        ...     status_code=cls.status_code,
        ... )
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{e.__class__.__name__!r}: {e}")
                logger.exception(e)
                if isinstance(e, HTTPException):
                    raise
                response = JSONResponse(
                    content=(
                        cls.content
                        if cls.content
                        else {"message": str(e), "errorType": e.__class__.__name__}
                    ),
                    status_code=cls.status_code,
                )
                cls.reset_variables()
                return response

        return wrapper
