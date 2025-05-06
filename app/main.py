import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import metadata, image, blog
import app.logging_config  # Ensure logging is configured
import app.config

app = FastAPI()
app.include_router(metadata.router)
app.include_router(image.router)
app.include_router(blog.router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.getLogger(__name__).error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    ) 