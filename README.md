# AI Blog Poster 🚀

![GitHub release](https://img.shields.io/github/release/vuongkiranocode2004/ai-blog-poster.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-orange)

Welcome to the **AI Blog Poster** repository! This project provides a RESTful API that helps you automatically generate SEO-optimized blog posts and AI-generated hero images using OpenAI models. 

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **SEO Optimization**: Automatically generate blog posts that are optimized for search engines.
- **AI-Generated Images**: Create hero images for your blog posts using OpenAI models.
- **Metadata Configuration**: Easily configure metadata for each blog post.
- **Frontmatter Customization**: Customize the frontmatter in your markdown files.
- **Markdown Formatting**: Output structured local files in markdown format.
- **FastAPI Integration**: Built with FastAPI for fast and efficient API handling.

## Technologies Used

This project utilizes several technologies to ensure a smooth and efficient experience:

- **Python**: The primary programming language used for development.
- **FastAPI**: A modern web framework for building APIs with Python.
- **OpenAI**: For generating content and images.
- **Markdown**: For formatting blog posts.
- **YAML**: For managing frontmatter in a structured way.

## Installation

To get started with **AI Blog Poster**, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/vuongkiranocode2004/ai-blog-poster.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ai-blog-poster
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your OpenAI API key. Create a `.env` file in the root directory and add your API key:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

To run the API, use the following command:

```bash
uvicorn main:app --reload
```

Once the server is running, you can access the API at `http://127.0.0.1:8000`.

## API Endpoints

### Generate Blog Post

- **Endpoint**: `/generate-blog`
- **Method**: `POST`
- **Request Body**:

```json
{
  "title": "Your Blog Title",
  "keywords": ["keyword1", "keyword2"],
  "length": "long",
  "metadata": {
    "author": "Your Name",
    "date": "2023-10-01"
  }
}
```

- **Response**:

```json
{
  "content": "Generated blog post content...",
  "metadata": {
    "title": "Your Blog Title",
    "author": "Your Name",
    "date": "2023-10-01"
  }
}
```

### Generate Hero Image

- **Endpoint**: `/generate-image`
- **Method**: `POST`
- **Request Body**:

```json
{
  "description": "Description for the image"
}
```

- **Response**:

```json
{
  "image_url": "https://link-to-generated-image.com"
}
```

## Configuration

You can customize the configuration by modifying the `config.yaml` file. This file allows you to set default values for metadata, keywords, and other parameters.

### Example `config.yaml`

```yaml
default:
  author: "Your Name"
  keywords:
    - "keyword1"
    - "keyword2"
  length: "medium"
```

## Example Output

After generating a blog post, you will receive a markdown file with the following structure:

```markdown
---
title: "Your Blog Title"
author: "Your Name"
date: "2023-10-01"
keywords: ["keyword1", "keyword2"]
---

# Your Blog Title

Generated blog post content...

![Hero Image](https://link-to-generated-image.com)
```

## Contributing

We welcome contributions to the **AI Blog Poster** project. If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, feel free to reach out:

- GitHub: [vuongkiranocode2004](https://github.com/vuongkiranocode2004)
- Email: your-email@example.com

For the latest releases, visit the [Releases](https://github.com/vuongkiranocode2004/ai-blog-poster/releases) section.

Thank you for checking out **AI Blog Poster**! We hope it helps you streamline your blogging process.