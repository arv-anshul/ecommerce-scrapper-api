import os
import typing as t
from pathlib import Path

JSON: t.TypeAlias = dict[str, t.Any]
PathLike: t.TypeAlias = str | os.PathLike | Path
URLParams: t.TypeAlias = dict[str, str]
PagesLike: t.TypeAlias = list | range
