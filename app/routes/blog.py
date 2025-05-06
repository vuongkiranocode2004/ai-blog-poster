from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.services.blog_service import generate_blog

router = APIRouter()

class BlogRequest(BaseModel):
    keywords: List[str]
    language: str
    word_count: int
    format: str
    frontmatter_schema: Dict[str, str]
    components: List[str]
    custom_rules: Dict[str, Any]
    image_style: str
    image_type: str = "webp"
    image_size: str = Field(
        default="1536x1024",
        description="The size of the generated images. Must be one of: 1024x1024, 1536x1024 (landscape), 1024x1536 (portrait), or 'auto' (default value) for gpt-image-1."
    )
    image_url_suffix: str = "./"
    output_compression: int = 100

class BlogResponse(BaseModel):
    file_path: str
    image_path: str

@router.post("/generate/blog", response_model=BlogResponse)
def generate_blog_endpoint(request: BlogRequest):
    file_path, image_path = generate_blog(
        request.keywords,
        request.language,
        request.word_count,
        request.format,
        request.frontmatter_schema,
        request.components,
        request.custom_rules,
        request.image_style,
        request.image_type,
        request.image_size,
        request.image_url_suffix,
        request.output_compression
    )
    return BlogResponse(file_path=file_path, image_path=image_path) 