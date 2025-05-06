# Project Requirements Document (PRD)

## 1. Project Overview

**Paragraph 1**\
The Blog Post Creator API is a RESTful service that automates the generation of SEO-optimized blog content and accompanying images. It addresses the pain point of manually writing posts, crafting metadata, inserting images, and wiring up internal links. By exposing simple HTTP endpoints, it lets developers, SEO specialists, and automation tools (CLI scripts, Zapier workflows) trigger content clusters or one-off posts and receive fully formatted files on disk.

**Paragraph 2**\
This proof‐of‐concept is being built to validate a seamless, code-first approach to content production. Success means that clients can request images and blog posts via JSON, receive valid Markdown/MDX/TXT files with YAML frontmatter, and see correctly generated hero/supporting images—all saved under a slugified folder structure. Future goals include adding authentication, asynchronous scaling, and multi-tenant support, but the immediate objective is a rock-solid local file output workflow.

## 2. In-Scope vs. Out-of-Scope

### In-Scope (v1.0)

*   **Endpoints**

    *   `GET /metadata/config` – Returns supported languages, formats, and components.
    *   `POST /generate/image` – Generates hero/supporting images from a prompt.
    *   `POST /generate/blog` – Creates one or more SEO-ready blog posts.

*   **Local File Output**

    *   Files saved under a directory named by slugified content cluster (e.g., `how-to-consolidate-debt/`).
    *   Filenames and folder names are slugified titles.

*   **Configurable Frontmatter**

    *   YAML frontmatter fields: `title`, `meta_title`, `description`, `date`, `image`, `categories`, `featured`, `draft`.
    *   Format choice: `.md`, `.mdx`, or `.txt`.

*   **Image Generation**

    *   Hero image + multiple supporting images via OpenAI `gpt-image-1`.

*   **Text Generation & SEO**

    *   Content from OpenAI `gpt-4o-mini` with injected keywords, semantic headings, meta tags.
    *   Automatic internal linking (relative or domain-prefixed).

*   **Custom Rules & Components**

    *   User-supplied tone/style rules.
    *   Reusable components: `<Callout />`, `<FAQ />`, `<Image />`, `<Quote />`.

*   **Logging**

    *   Console logs at INFO and ERROR levels using Python’s logging module.

*   **Configuration Management**

    *   Secrets (OpenAI keys) via `.env` loaded with `python-dotenv`.

### Out-of-Scope (v1.0)

*   Authentication, API keys, or token-based access control
*   Database or persistent storage beyond local file system
*   Rate limiting or throttling middleware
*   Web or mobile UI
*   Multi-tenant isolation or billing
*   Full asynchronous processing (synchronous only, with hooks for future async)

## 3. User Flow

**Paragraph 1**\
A developer clones the repository or installs the package, ensures Python 3.11+ is available, and adds their OpenAI API key to a `.env` file. They start the FastAPI server (e.g., `uvicorn main:app --reload`) and watch the console for INFO logs. No authentication steps are needed in this proof-of-concept, making it easy to experiment or wire into a CLI script or Zapier action.

**Paragraph 2**\
Next, the developer calls `GET /metadata/config` to discover supported languages, file formats, and component tags. With that info, they craft a JSON payload for `POST /generate/image`, supply prompts and image counts, then receive filenames of saved images. Finally, they post to `POST /generate/blog` with keywords, formatting options, internal link rules, and image references. The API writes markdown or text files under a folder named after the slugified content cluster. At every step, meaningful console logs report success or errors, and the generated files are ready for review, CMS import, or static-site builds.

## 4. Core Features

*   **Metadata Discovery**

    *   `GET /metadata/config` returns supported `languages`, `formats`, and `components` in JSON.

*   **Hero Image Generation**

    *   `POST /generate/image` accepts `{ prompt, count }`.
    *   Uses `gpt-image-1` to create and save images with slugified filenames.

*   **Supporting Images**

    *   Generates multiple images per request, saved alongside the hero image.

*   **Blog Post Creation**

    *   `POST /generate/blog` accepts keywords, word count, language, format, frontmatter template, internal link config, custom rules.
    *   Uses `gpt-4o-mini` to produce SEO-optimized content with semantic HTML structure.

*   **Internal Linking**

    *   Auto-links related posts using relative paths by default or domain-prefixed URLs if configured.

*   **Formatting & Components**

    *   Output options: `.md`, `.mdx`, `.txt`.
    *   Embed `<Callout />`, `<FAQ />`, `<Image />`, `<Quote />` where requested.

*   **SEO Rules Injection**

    *   Inserts primary/secondary keywords into titles, headings, meta tags.
    *   Enforces H1–H3 hierarchy and proper keyword density.

*   **Custom Text Rules**

    *   Honors user-defined tone, style, or brand-voice constraints.

*   **Logging & Error Handling**

    *   Timestamps at INFO/ERROR levels in plain text.
    *   Simple console output, ready for extension to file or JSON logs.

## 5. Tech Stack & Tools

*   **Backend Framework**: FastAPI (Python 3.11+)

*   **AI Models**:

    *   Text: OpenAI `gpt-4o-mini`
    *   Images: OpenAI `gpt-image-1`

*   **File I/O**: Python `os` + `pathlib`

*   **Environment Management**: `python-dotenv` for `.env` variables

*   **Logging**: Python `logging` module

*   **Server**: Uvicorn ASGI server

*   **IDE / Plugins**: Cursor (AI-powered coding), with potential GPT-4o or Claude support for code assist

*   **Integration**: Compatible with CLI tools, Zapier-style workflows, custom Python scripts

## 6. Non-Functional Requirements

*   **Performance**

    *   `GET /metadata/config`: <200 ms
    *   `POST /generate/image`: depends on OpenAI, aim <10 s for up to 3 images
    *   `POST /generate/blog`: aim <5 s per 500 words

*   **Security**

    *   Secrets strictly via environment variables
    *   No user data persisted beyond local files

*   **Scalability**

    *   Synchronous design now, structured for future FastAPI middleware (rate limiting, async)

*   **Usability**

    *   Clear console logs with timestamps and log levels
    *   Human-readable error messages

*   **Extensibility**

    *   Modular code to add new AI models, components, or output formats

## 7. Constraints & Assumptions

*   **Proof-of-Concept Scope**

    *   No authentication or authorization required in v1.0
    *   No database or cloud storage—local file system only

*   **AI Model Availability**

    *   Requires valid OpenAI API access to `gpt-image-1` and `gpt-4o-mini`

*   **Filesystem Permissions**

    *   Write access to the output directory

*   **Single-Tenant Use**

    *   Only one client context per server instance

*   **Environment**

    *   Python 3.11+ on a Unix/Windows machine or Docker container

## 8. Known Issues & Potential Pitfalls

*   **OpenAI Rate Limits**

    *   May trigger 429 errors; design should catch and retry with backoff.

*   **Image Generation Latency**

    *   Large image batches could block synchronous flow; consider async endpoints later.

*   **Slug Collisions**

    *   Two posts with identical titles could overwrite; implement unique suffix or timestamp if needed.

*   **Disk Space Management**

    *   Repeated runs can bloat local storage; recommend a cleanup utility or TTL policy.

*   **MDX Component Validation**

    *   Invalid component usage could break downstream renderers; consider lightweight syntax checks.

*   **Logging Scalability**

    *   Console logs may not scale; later switch to rotating file handlers or structured JSON logs.

This PRD is the single source of truth for the Blog Post Creator API v1.0. All subsequent technical documents (Tech Stack, Backend Structure, Implementation Plan, etc.) should draw directly from these specifications without ambiguity.
