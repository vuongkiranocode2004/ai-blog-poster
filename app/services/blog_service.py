import logging
from typing import List, Dict, Any
from pathlib import Path
from app.utils.slugify import slugify
import yaml
from app.services.openai_client import client
import os
import re
from app.services.image_service import generate_images
import datetime
from fastapi import HTTPException
import collections

logger = logging.getLogger(__name__)

def extract_frontmatter_and_body(markdown: str) -> (dict, str):
    # Try YAML code block first
    codeblock_match = re.search(r'```yaml\s*\n(.*?)\n```', markdown, re.DOTALL | re.MULTILINE)
    if codeblock_match:
        yaml_str = codeblock_match.group(1)
        try:
            fm = yaml.safe_load(yaml_str)
            # Remove the code block from the markdown
            body = markdown[codeblock_match.end():].lstrip('\n')
            return fm, body
        except Exception as e:
            logger.error(f"YAML parsing error (code block): {e}\nYAML string: {yaml_str}")
            # Fallback: Try --- ... --- extraction if code block YAML fails
            fm_match = re.search(r'^---\s*\n(.*?)\n---', markdown, re.DOTALL | re.MULTILINE)
            if fm_match:
                yaml_str = fm_match.group(1)
                try:
                    fm = yaml.safe_load(yaml_str)
                except Exception as e:
                    logger.error(f"YAML parsing error (---): {e}\nYAML string: {yaml_str}")
                    fm = {}
                # Remove the frontmatter from the markdown
                body = markdown[fm_match.end():].lstrip('\n')
                return fm, body
            else:
                fm = {}
                body = markdown[codeblock_match.end():].lstrip('\n')
                return fm, body
    # Fallback: Try --- ... ---
    fm_match = re.search(r'^---\s*\n(.*?)\n---', markdown, re.DOTALL | re.MULTILINE)
    if fm_match:
        yaml_str = fm_match.group(1)
        try:
            fm = yaml.safe_load(yaml_str)
        except Exception as e:
            logger.error(f"YAML parsing error (---): {e}\nYAML string: {yaml_str}")
            fm = {}
        # Remove the frontmatter from the markdown
        body = markdown[fm_match.end():].lstrip('\n')
        return fm, body
    logger.error(f"No recognizable frontmatter found in model output. Output:\n{markdown}")
    return {}, markdown

def quote_string(s):
    if s is None:
        return '""'
    s = str(s)
    if not (s.startswith('"') and s.endswith('"')):
        s = f'"{s}"'
    return s

def quote_list(lst):
    return '[' + ', '.join(quote_string(x) for x in lst if x) + ']'

def extract_title_from_heading(body: str) -> str:
    match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ''

def generate_frontmatter_with_openai(schema: Dict[str, str], keywords: List[str], language: str, today: str) -> Dict[str, Any]:
    """
    Use OpenAI to generate a frontmatter dict based on the schema and context.
    """
    schema_str = ', '.join([f'{k}: {v}' for k, v in schema.items()])
    prompt = (
        f"Given the following blog metadata schema: {schema_str}.\n"
        f"Generate a YAML frontmatter object with realistic, relevant values for a blog post in {language} about these keywords: {', '.join(keywords)}.\n"
        f"For 'date', output an ISO 8601 datetime (e.g., 2025-05-04T00:09:02Z).\n"
        f"Today's date is {today}.\n"
        f"For 'categories', output only a single relevant category (not a list), if it is Finance, then use Personal Finance.\n"
        f"Draft and Featured should be false.\n"
        f"Do not wrap the YAML in code blocks or triple backticks. Output only valid YAML, no explanations."
    )
    fm_yaml = client.generate_blog(prompt)
    # Strip code block markers if present
    if fm_yaml.strip().startswith('```'):
        fm_yaml = re.sub(r'^```[a-zA-Z]*\s*', '', fm_yaml.strip())
        fm_yaml = re.sub(r'```$', '', fm_yaml.strip())
    try:
        fm = yaml.safe_load(fm_yaml)
        if not isinstance(fm, dict):
            raise ValueError("Frontmatter is not a dict")
        # Ensure 'categories' is a string (not a list)
        if 'categories' in fm:
            if isinstance(fm['categories'], list):
                fm['categories'] = fm['categories'][0] if fm['categories'] else ''
    except Exception as e:
        logger.error(f"YAML parsing error for generated frontmatter: {e}\nYAML string: {fm_yaml}")
        raise HTTPException(status_code=422, detail='Failed to generate valid frontmatter.')
    return fm

def quoted_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.SafeDumper.add_representer(str, quoted_str_representer)

def dump_frontmatter(frontmatter: dict) -> str:
    # Ensure categories is always a single-line list of double-quoted strings
    categories = frontmatter.get('categories', [])
    if not isinstance(categories, list):
        categories = [categories] if categories else []
    categories_str = '[{}]'.format(', '.join(f'"{c}"' for c in categories if c))
    # Ensure date is ISO 8601 string, unquoted
    date = frontmatter.get('date', '')
    if isinstance(date, (datetime.date, datetime.datetime)):
        date = date.isoformat()
    # Do NOT wrap date in double quotes
    # Escape double quotes in string values
    def esc(val):
        return str(val).replace('"', '\"')
    field_order = [
        ('categories', categories_str),
        ('date', date),  # unquoted
        ('description', f'"{esc(frontmatter.get("description", ""))}"'),
        ('draft', 'true' if frontmatter.get('draft', False) else 'false'),
        ('featured', 'true' if frontmatter.get('featured', False) else 'false'),
        ('image', f'"{esc(frontmatter.get("image", ""))}"'),
        ('meta_title', f'"{esc(frontmatter.get("meta_title", ""))}"'),
        ('title', f'"{esc(frontmatter.get("title", ""))}"'),
    ]
    lines = [f'{k}: {v}' for k, v in field_order]
    return '\n'.join(lines) + '\n'

def generate_blog(
    keywords: List[str],
    language: str,
    word_count: int,
    format: str,
    frontmatter_schema: Dict[str, str],
    components: List[str],
    custom_rules: Dict[str, Any],
    image_style: str,
    image_type: str = "webp",
    image_size: str = "1024x1024",
    image_url_suffix: str = "./",
    output_compression: int = 100
) -> (str, str):
    # Step 0: Get today's date
    now = datetime.datetime.utcnow().replace(microsecond=0)
    today = now.isoformat() + 'Z'

    # Step 1: Generate frontmatter using OpenAI
    frontmatter = generate_frontmatter_with_openai(frontmatter_schema, keywords, language, today)
    if 'date' not in frontmatter or not frontmatter['date']:
        frontmatter['date'] = today

    # Step 2: Slugify the title
    title = frontmatter.get('title', '').strip()
    if not title:
        logger.error(f"Frontmatter missing title: {frontmatter}")
        raise HTTPException(status_code=422, detail='Generated frontmatter missing title.')
    slug = slugify(title)

    # Step 3: Generate the blog body using OpenAI
    prompt = (
        f"Write only the blog post body in {format} format. "
        f"Use the following frontmatter as context (do not output it): {frontmatter}. "
        f"Target word count: {word_count} words. "
        f"Include the following components if relevant: {', '.join(components)}. "
        f"Output only valid {format}. Do not include explanations or extra text."
    )
    if custom_rules:
        rules_text = "\nEditorial/content rules to follow:\n" + "\n".join(f"- {v}" for v in custom_rules.values())
        prompt += rules_text
    blog_content = client.generate_blog(prompt)
    logger.error(f"Raw model output for debugging:\n{blog_content}")
    fm, blog_body = extract_frontmatter_and_body(blog_content)
    # Use the original frontmatter, but update with any new fields from the model
    if fm:
        frontmatter.update({k: v for k, v in fm.items() if v})
    # Step 4: Create an image prompt from the frontmatter and style
    description = frontmatter.get('description', '')
    image_prompt_gpt = (
        f"Write a short, direct, visual prompt for an AI image generator. Do not use instructions or explanations. Output only the prompt. "
        f"Title: {title}. Description: {description}."
    )
    image_prompt_result = client.generate_blog(image_prompt_gpt, model="gpt-4o-mini", max_tokens=64)
    image_prompt = f"{image_prompt_result.strip()} Style: {image_style}."

    # Step 5: Generate the image, save as slugified title
    blog_dir = Path(f"./content/{slug}")
    blog_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists before image generation
    image_filename = f'{slug}.{image_type}'
    image_paths = generate_images(
        image_prompt,
        count=1,
        size=image_size,
        output_compression=output_compression,
        output_format=image_type,
        output_dir=str(blog_dir),
        output_filename=image_filename
    )
    image_path = image_paths[0]

    # Step 6: Update the frontmatter with image link and any other final details
    frontmatter['image'] = f'{image_url_suffix}{image_filename}'
    if 'date' not in frontmatter or not frontmatter['date']:
        frontmatter['date'] = today

    # Step 7: Write the final blog file
    ext = format if format in ['md', 'mdx', 'txt'] else 'md'
    yaml_front = dump_frontmatter(frontmatter)
    content = f"---\n{yaml_front}---\n\n{blog_body}"
    file_path = blog_dir / f"{slug}.{ext}"
    file_path.write_text(content, encoding="utf-8")

    return str(file_path), str(image_path) 