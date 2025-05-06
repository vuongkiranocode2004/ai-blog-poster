from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.image_service import generate_images

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str
    count: int
    size: str = "1024x1024"
    output_compression: int = 80
    output_format: str = "png"

class ImageResponse(BaseModel):
    file_paths: List[str]

@router.post("/generate/image", response_model=ImageResponse)
def generate_image_endpoint(request: ImageRequest):
    file_paths = generate_images(
        request.prompt,
        request.count,
        request.size,
        request.output_compression,
        request.output_format
    )
    return ImageResponse(file_paths=file_paths) 