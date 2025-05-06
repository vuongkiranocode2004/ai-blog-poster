from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/metadata/config")
def get_metadata_config():
    return JSONResponse({
        "languages": ["en", "es", "fr"],
        "formats": ["md", "mdx", "txt"],
        "components": ["image", "table", "code"]
    }) 