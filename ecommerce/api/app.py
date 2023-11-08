from fastapi import FastAPI

from .routes import curl, flipkart

app = FastAPI()


@app.get("/")
async def root():
    return {
        "running": True,
    }


app.include_router(curl.curl_router)
app.include_router(flipkart.flipkart_router)
