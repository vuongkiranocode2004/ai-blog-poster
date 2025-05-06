import logging
from typing import List
from pathlib import Path
from app.utils.slugify import slugify
from app.services.openai_client import client
import base64
import os

logger = logging.getLogger(__name__)

def generate_images(prompt: str, count: int, size: str = "1024x1024", output_compression: int = 100, output_format: str = "webp", output_dir: str = None, output_filename: str = None) -> List[str]:
    logger.info(f"Generating {count} images for prompt: {prompt} with size: {size}, output_compression: {output_compression}, output_format: {output_format}")
    if output_dir:
        image_dir = Path(output_dir)
    else:
        slug = slugify(prompt)[:50]  # Truncate to 50 chars
        image_dir = Path(f"./content/images/{slug}")
    image_dir.mkdir(parents=True, exist_ok=True)
    file_paths = []
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set, using dummy images.")
        for i in range(count):
            if output_filename:
                file_path = image_dir / (output_filename if count == 1 else f"{output_filename}_{i+1}.{output_format}")
            else:
                file_path = image_dir / f"image_{i+1}.{output_format}"
            file_path.write_bytes(b"fake image data")
            file_paths.append(str(file_path))
        return file_paths
    try:
        b64_images = client.generate_image(prompt, n=count, size=size, output_compression=output_compression, output_format=output_format)
        for i, b64_img in enumerate(b64_images):
            if output_filename:
                file_path = image_dir / (output_filename if count == 1 else f"{output_filename}_{i+1}.{output_format}")
            else:
                file_path = image_dir / f"image_{i+1}.{output_format}"
            image_bytes = base64.b64decode(b64_img)
            file_path.write_bytes(image_bytes)
            file_paths.append(str(file_path))
    except Exception as e:
        logger.error(f"OpenAI image generation failed: {e}")
        # Fallback to dummy
        for i in range(count):
            if output_filename:
                file_path = image_dir / (output_filename if count == 1 else f"{output_filename}_{i+1}.{output_format}")
            else:
                file_path = image_dir / f"image_{i+1}.{output_format}"
            file_path.write_bytes(b"fake image data")
            file_paths.append(str(file_path))
    return file_paths 