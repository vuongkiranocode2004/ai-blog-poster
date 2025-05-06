import os
import base64
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def generate_image(prompt: str, n: int = 1, size: str = "1024x1024", model: str = "gpt-image-1", output_compression: int = 80, output_format: str = "png"):
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        logger.info(f"Calling OpenAI image API: model={model}, prompt={prompt}, n={n}, size={size}, output_compression={output_compression}, output_format={output_format}")
        if model == "gpt-image-1":
            response = client.images.generate(
                model=model,
                prompt=prompt,
                n=n,
                size=size,
                output_compression=output_compression,
                output_format=output_format
            )
        else:
            response = client.images.generate(
                model=model,
                prompt=prompt,
                n=n,
                size=size,
                response_format="b64_json"
            )
        return [img.b64_json for img in response.data]

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def generate_blog(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 8024):
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        logger.info(f"Calling OpenAI chat API: model={model}, prompt={prompt}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def generate_image_prompt(title: str, description: str, style: str, direct: bool = False, model: str = "gpt-4o-mini", max_tokens: int = 524):
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        logger.info(f"Calling OpenAI chat API for image prompt: model={model}, title={title}, description={description}, style={style}, direct={direct}")
        if direct:
            prompt = (
                f"Write a short, direct prompt for an AI image generator to create a hero image for the following blog post. "
                f"Title: {title}. Description: {description}. Style: {style}. Output only the prompt."
            )
        else:
            prompt = (
                f"Create an appropriate hero image for this blog post title: {title} "
                f"and description: {description} in the style of {style}."
            )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

client = OpenAIClient() 