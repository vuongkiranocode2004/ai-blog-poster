# Implementation plan

## Phase 1: Environment Setup

1. **Prevalidation**: Check if current directory contains a Python project (look for `pyproject.toml`, `requirements.txt`, or `main.py`); if found, skip project initialization (Step Rules: Prevalidation).
2. Initialize a Git repository in project root if `.git` is not present by running `git init` (Important Considerations: Scaling).
3. Create a Python 3.11 virtual environment at project root by running:
   ```bash
   python3.11 -m venv .venv
   ```
   (Tech Stack: Backend).
4. **Validation**: Activate the virtual environment and run `python --version` to confirm Python 3.11+ (Tech Stack: Backend).
5. Create an empty `requirements.txt` file at project root (App Structure and Flow: Configuration).
6. Install dependencies by running:
   ```bash
   pip install fastapi==0.100.0 uvicorn[standard]==0.23.1 python-dotenv==1.0.0 openai==0.27.0
   ```
   (Tech Stack: Backend; Image Generation; Text Generation).
7. **Validation**: Run `pip freeze > requirements.txt` and confirm the exact versions are recorded (Tech Stack: Backend).
8. Create a `.env` file at project root with placeholders for secrets:
   ```dotenv
   OPENAI_API_KEY=
   LOG_LEVEL=INFO
   ```
   (Important Considerations: Secrets Management).

## Phase 2: Frontend Development

_No dedicated UI—this project exposes only a REST API. (Project Goal Section)_

## Phase 3: Backend Development

9. Create the FastAPI application entrypoint at `/app/main.py` with:
   ```python
   from fastapi import FastAPI
   app = FastAPI()
   ```
   (Tech Stack: Backend).
10. **Validation**: Run `uvicorn app.main:app --reload` and confirm a 404 response at `/` (App Structure and Flow: Configuration).
11. Create `/app/config.py` to load environment variables using `python-dotenv`:
    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```
    (Important Considerations: Secrets Management).
12. Implement the metadata route in `/app/routes/metadata.py` with `GET /metadata/config` returning supported `languages`, `formats`, and `components` from a hard-coded dict (Core Features: Metadata Discovery).
13. Include the metadata router in `/app/main.py` via `app.include_router(...)` (Core Features: Metadata Discovery).
14. **Validation**: Execute `curl http://localhost:8000/metadata/config` and verify JSON keys `languages`, `formats`, `components` (App Structure and Flow: Metadata Retrieval).
15. Create `/app/services/image_service.py` with a function `generate_images(prompt: str, count: int) -> List[str]` that calls OpenAI `gpt-image-1` and saves images under `./content/images/<slug>/` (Core Features: Image Generation).
16. Implement `/app/routes/image.py` with `POST /generate/image` to accept `{ prompt, count }`, invoke `generate_images`, and return saved file paths (Core Features: Image Generation).
17. **Validation**: Run:
    ```bash
    curl -X POST http://localhost:8000/generate/image \
      -H "Content-Type: application/json" \
      -d '{"prompt":"example","count":1}'
    ```
    and confirm an image file appears in `./content/images/` (App Structure and Flow: Image Generation).
18. Create `/app/services/blog_service.py` that defines `generate_blog(...) -> str`, which calls OpenAI `gpt-4o-mini`, builds YAML frontmatter, injects internal links, applies SEO rules and custom rules, and saves output to `./content/<slug>/post.<ext>` (Core Features: Blog Post Creation).
19. Implement `/app/routes/blog.py` with `POST /generate/blog` to accept `{ keywords, language, word_count, format, frontmatter, internal_linking, components, custom_rules }`, call `generate_blog`, and return the file path (Core Features: Blog Post Creation).
20. **Validation**: Run:
    ```bash
    curl -X POST http://localhost:8000/generate/blog \
      -H "Content-Type: application/json" \
      -d '{"keywords":["seo"],"language":"en","word_count":500,"format":"md","frontmatter":{"title":"Test"},"internal_linking":{"type":"relative"},"components":[],"custom_rules":{}}'
    ```
    and confirm `./content/test/post.md` exists (App Structure and Flow: Blog Post Generation).
21. Add logging configuration in `/app/logging_config.py` to set up Python `logging` with `LOG_LEVEL` from `.env`, timestamped plaintext format (Tech Stack: Logging).
22. In each service module, initialize `logger = logging.getLogger(__name__)` and add `logger.info()` / `logger.error()` calls at key steps (Tech Stack: Logging).
23. **Validation**: Insert a deliberate error in `/app/services/image_service.py` and confirm an ERROR log appears in console (App Structure and Flow: Error Handling).
24. In `/app/main.py`, add FastAPI exception handlers with `@app.exception_handler` to return JSON error responses and log the exception (Important Considerations: Error Handling).
25. **Validation**: Send an invalid payload to `/generate/blog` and verify a structured JSON error response plus an error log (App Structure and Flow: Error Handling).
26. Create `/app/utils/slugify.py` with a `slugify(text: str) -> str` utility using regex to generate folder and file slugs (Important Considerations: File Organization).
27. Update both `generate_images` and `generate_blog` to use `pathlib.Path` and `slugify` to ensure output directories exist before writing (Important Considerations: File Organization).

## Phase 4: Integration

28. Configure CORS in `/app/main.py` using `fastapi.middleware.cors.CORSMiddleware` to allow all origins (`*`) for CLI and automation platforms (Target Users Section).
29. **Validation**: From a different origin, run `curl http://localhost:8000/metadata/config` with `Origin: http://example.com` and confirm CORS headers in response (App Flow: Metadata Retrieval).

## Phase 5: Deployment

30. Create a `Dockerfile` at project root:
    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```
    (Important Considerations: Scaling).
31. **Validation**: Run `docker build -t blog-api .` and `docker run -p 8000:8000 blog-api`, then verify `/metadata/config` returns 200 (App Flow: Metadata Retrieval).
32. Create `docker-compose.yml` with a service `api` using:
    ```yaml
    version: '3.8'
    services:
      api:
        build: .
        ports:
          - "8000:8000"
    ```
    (Important Considerations: Scaling).
33. **Validation**: Run `docker-compose up --build` and confirm the API starts without errors and endpoints respond (App Flow: Metadata Retrieval).

---

*Total Steps: 33*