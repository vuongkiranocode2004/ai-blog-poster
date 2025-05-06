# Backend Structure Document

This document outlines the backend setup for the Blog Post Creator API. It explains how everything fits together, from the overall architecture to security, so anyone can understand how the backend is built and maintained.

## 1. Backend Architecture

Overall, the backend is a modular RESTful service built with FastAPI (Python 3.11+). It follows a simple, clear design to keep it maintainable and scalable:

- **Framework**: FastAPI for quick development, built-in validation, and automatic docs (OpenAPI).
- **Design Pattern**: “Router → Service → Utility”:
  - **Routers** define HTTP endpoints and input/output models.
  - **Services** contain the core logic (e.g., calling OpenAI, formatting files).
  - **Utilities** handle cross-cutting concerns (file I/O, logging, environment config).
- **Dependency Injection**: Used for configuration (API keys, file paths) and for swapping implementations in the future (e.g., local storage → cloud storage).

How it supports key goals:

- **Scalability**: Modular code makes it easy to add async endpoints or distribute services across containers.
- **Maintainability**: Separation of concerns keeps routes, logic, and utilities decoupled.
- **Performance**: FastAPI’s async support allows efficient handling of I/O-bound tasks (like network calls to OpenAI).

## 2. Database Management

There is no traditional database. Instead, content is stored as files in a structured directory layout:

- **Storage Type**: Local file system
- **Tools**: Python’s built-in `os` and `pathlib` modules
- **Data Organization**:
  - Top-level `output/` folder
  - Subfolders by content cluster (slugified titles)
  - Files named by slugified post titles with extensions `.md`, `.mdx`, or `.txt`
- **Data Practices**:
  - Ensure write permissions on the output directory
  - Use atomic writes (write to a temp file, then rename) to avoid partial files
  - Clean up or archive old clusters if needed

## 3. Database Schema (File Structure)

Although we’re not using SQL or NoSQL, here’s a clear view of how files are organized:

- output/
  - how-to-consolidate-debt/
    - how-to-consolidate-debt.md
    - hero-image.png
    - supporting-image-1.png
    - supporting-image-2.png
  - another-cluster-slug/
    - another-post.md
    - hero-image.png

Each markdown file starts with a YAML frontmatter block:
```
---
title: "..."
meta_title: "..."
description: "..."
date: 2025-05-01T05:00:00Z
image: "/images/blogs/...png"
categories: ["..."]
featured: false
draft: false
---
```

## 4. API Design and Endpoints

The API uses a RESTful style. All endpoints live under `/metadata` or `/generate`:

### 4.1 GET /metadata/config
- **Purpose**: Tell clients what options are available.
- **Response**:
  - `languages`: ["en", "fr", "de", "es"]
  - `formats`: ["md", "mdx", "txt"]
  - `components`: ["Callout", "FAQ", "Image", "Quote"]
- **Performance Goal**: < 200 ms

### 4.2 POST /generate/image
- **Purpose**: Generate one or more images.
- **Request Body**:
  - `prompt`: text prompt for image
  - `count`: number of images
- **Response**:
  - `filenames`: list of generated image file names
- **Performance Goal**: < 10 seconds

### 4.3 POST /generate/blog
- **Purpose**: Generate blog posts with SEO and formatting options.
- **Request Body**:
  - `keywords`: list of target keywords
  - `num_posts`: how many posts to create
  - `language`: e.g., "en"
  - `format`: "md" | "mdx" | "txt"
  - `components`: which special blocks to include
  - `link_style`: "relative" or full domain prefixed
  - Custom YAML frontmatter fields
- **Response**:
  - `file_paths`: list of generated file paths
- **Performance Goal**: < 5 seconds per 500 words

## 5. Hosting Solutions

- **Environment**: Cloud VPS or container platform (e.g., AWS EC2, DigitalOcean Droplet, or Kubernetes cluster).
- **Benefits**:
  - **Reliability**: Standard cloud hosting with Uptime SLAs.
  - **Scalability**: Vertical scaling (bigger instance) or horizontal (more instances behind a load balancer).
  - **Cost-Effectiveness**: Pay-as-you-go plans, idle autoscaling for low-traffic times.

## 6. Infrastructure Components

- **Load Balancer** (for multi-instance setups)
  - Distributes incoming HTTP requests evenly
- **Reverse Proxy** (e.g., Nginx or Traefik)
  - Handles SSL termination
  - Routes traffic to FastAPI application
- **Caching**
  - In-memory cache (e.g., Redis) for metadata responses if needed
- **CDN** (optional)
  - Serve static images if offloaded from local storage
- **File Storage**
  - Local disk for POC
  - Future: S3 or other object storage for durability and easy scaling

## 7. Security Measures

Even though this POC doesn’t require authentication yet, it’s built with security in mind:

- **Environment Variables**
  - All secrets (OpenAI keys) live in a `.env` file and are loaded via `python-dotenv`
- **Input Validation**
  - FastAPI’s Pydantic models ensure requests have correct data types and formats
- **Error Handling**
  - 422 for invalid requests
  - 500 for internal errors (OpenAI failures, file I/O issues)
- **Data Encryption**
  - SSL/TLS enforced at the load balancer or reverse proxy
- **Future Auth**
  - Structure in place to add OAuth2 or API keys when ready

## 8. Monitoring and Maintenance

- **Logging**
  - Python `logging` module at `INFO` and `ERROR` levels
  - Timestamps included for tracing
- **Health Checks**
  - `/health` endpoint that returns 200 OK if the app and disk are writable
- **Performance Monitoring**
  - Integrate with tools like Prometheus/Grafana or a hosted APM (Datadog, New Relic)
- **Maintenance**
  - Rolling restarts for updates
  - Backup strategy for output files (e.g., daily sync to object storage)
  - Automated tests run on CI for every PR

## 9. Conclusion and Overall Backend Summary

This backend is a focused, modular service that:

- Uses FastAPI and clear design patterns for maintainability.
- Stores generated content in a predictable file structure.
- Exposes simple, well-documented REST endpoints to generate images and blog posts.
- Is ready to scale by adding async support, distributed storage, or authentication layers when needed.
- Includes security, logging, and monitoring best practices out of the box.

Together, these components deliver a reliable, high-performing API for automated, SEO-friendly blog content creation.