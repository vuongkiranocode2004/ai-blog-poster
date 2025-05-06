# BlogPostWriter API

A powerful FastAPI-based application that automates the generation of SEO-optimized blog content and images, saving them locally in an organized directory structure.

## 🚀 Overview

BlogPostWriter API leverages the OpenAI API to generate high-quality blog content and images based on user-specified parameters. The application creates a structured content directory with:

- SEO-optimized blog posts in markdown, MDX, or text format
- Custom-generated images that match your content
- YAML frontmatter with configurable fields
- Organized directory structure based on slugified post titles

## ✨ Features

- **Content Generation**: Create complete blog posts with customizable word count and format
- **Image Generation**: Generate matching images with configurable styles and formats
- **Flexible Formatting**: Support for Markdown, MDX, and plain text
- **Customizable Components**: Include quotes, FAQs, and other content components
- **Dynamic Frontmatter**: Configure YAML frontmatter structure via API request
- **Local Storage**: All content saved in an organized directory structure
- **Custom Rules**: Apply specific editorial rules to guide content generation
- **Error Handling**: Built-in retry logic for API rate limits

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/EmpoweredLeader/ai-blog-poster
   cd BlogPostWriter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # MacOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Running the Application

1. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`

3. Access the interactive API documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`

## 📝 API Endpoints

### Generate Blog Post

`POST /generate/blog`

Generates a blog post and an accompanying image based on the provided parameters.

#### Request Body Example:

```json
{
  "keywords": ["AI", "Automation", "Content Creation"],
  "language": "en",
  "word_count": 300,
  "format": "md",
  "frontmatter_schema": {
    "title": "string",
    "meta_title": "string",
    "description": "string",
    "date": "datetime",
    "image": "string",
    "categories": "list[string]",
    "featured": "bool",
    "draft": "bool"
  },
  "components": ["quote", "faq"],
  "custom_rules": {
    "plain_language": "Use simple, direct language",
    "seo_friendly": "Ensure proper keyword usage and heading structure"
  },
  "image_style": "Minimalist illustration with blue tones",
  "image_type": "webp",
  "image_size": "1024x1024",
  "image_url_suffix": "/images/blog/"
}
```

### Get Metadata Configuration

`GET /metadata/config`

Returns supported languages, formats, and components.

## 🧪 Testing

The project includes a sample test script `test_blog.py` that demonstrates how to use the API. You can modify this script to test different parameters:

```bash
python test_blog.py
```

> Note: You can modify the `test_blog.py` file to test different parameters and configurations according to your specific needs.

## 📁 Project Structure

```
BlogPostWriter/
├── .env                  # Environment variables (create this file)
├── app/                  # Main application directory
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration settings
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── content/              # Generated content directory
├── requirements.txt      # Python dependencies
└── test_blog.py          # Example test script
```

## 📝 Customization

### Custom Rules

You can add custom editorial rules in your API request to control the tone, style, and content of generated blog posts.

### Image Styles

Customize the image generation by providing detailed style descriptions in the `image_style` parameter.

### Frontmatter Schema

Define the structure of your YAML frontmatter to match your content management system's requirements.

## 🔑 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 