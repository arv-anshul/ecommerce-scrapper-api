import functools
from ast import literal_eval
from asyncio import iscoroutinefunction
from typing import Any

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ecommerce.logger import get_logger

logger = get_logger(__name__)


class _APIExceptionResponder:
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

    def update(self, status_code: int, content: Any = None) -> None:
        self.status_code = status_code
        self.content = content

    def reset(self) -> None:
        """Reset the class variables to its default values."""
        self.status_code = 400
        self.content = None

    def better_api_error_response(self, func):
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
                        self.content
                        if self.content
                        else {
                            "message": self.__validate_error_msg(e),
                            "errorType": e.__class__.__name__,
                        }
                    ),
                    status_code=self.status_code,
                )
                return response
            finally:
                self.reset()

        return wrapper

    def __validate_error_msg(self, msg: Exception, /) -> Any:
        try:
            return literal_eval(str(msg))
        except (ValueError, SyntaxError):
            return str(msg)


APIExceptionResponder = _APIExceptionResponder()
