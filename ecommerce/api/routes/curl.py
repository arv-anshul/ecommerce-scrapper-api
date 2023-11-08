import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ecommerce.api.options import CurlTypeOptions, WebsiteOptions
from ecommerce.logger import get_logger

curl_router = APIRouter(prefix="/curl", tags=["curl"])
logger = get_logger(__name__)


class StoreCurlCommand(BaseModel):
    curlType: CurlTypeOptions
    website: WebsiteOptions
    command: str


@curl_router.get("/")
async def get_curl_command(
    curlType: CurlTypeOptions, website: WebsiteOptions
) -> StoreCurlCommand:
    path = f"configs/curl/{website.value}.{curlType.value}"
    if not os.path.exists(path):
        raise HTTPException(
            404,
            detail={
                "message": "curl command not found.",
                "query": {"curlType": curlType.value, "website": website.value},
            },
        )

    with open(path) as f:
        command = f.read()
        return StoreCurlCommand(curlType=curlType, website=website, command=command)


@curl_router.post("/")
def store_curl_command(data: StoreCurlCommand):
    path = Path("configs/curl") / f"{data.website.value}.{data.curlType.value}"
    if not path.parent.exists():
        logger.info(f"Making directory at {path.parent!r}")
        path.parent.mkdir(parents=True)

    logger.info(f"Writing curl command into {path!r}")
    path.write_text(data.command)
    return {
        "path": str(path),
        "store": True,
    }


@curl_router.get("/check")
async def check_curl_command_exists(curlType: CurlTypeOptions, website: WebsiteOptions):
    path = f"configs/curl/{website.value}.{curlType.value}"
    content = {"path": path, "exists": False}
    if os.path.exists(path):
        content["exists"] = True
    return content


@curl_router.get("/check/all")
async def list_all_curl_commands():
    data: dict = {"parentPath": "config/curl", "commands": {}}
    for _, _, filenames in os.walk("configs/curl"):
        for fname in filenames:
            website, page_name = fname.split(".")
            if website not in data["commands"]:
                data["commands"][website] = [page_name]
            else:
                data["commands"][website].append(page_name)
    return data
