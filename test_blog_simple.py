import requests
import sys

# Set API endpoints
BASE_URL = "http://127.0.0.1:8000"
METADATA_ENDPOINT = f"{BASE_URL}/metadata/config"
BLOG_ENDPOINT = f"{BASE_URL}/generate/blog"

# Test if server is running and healthy
print("Testing server connection...")
try:
    metadata_resp = requests.get(METADATA_ENDPOINT)
    if metadata_resp.status_code == 200:
        print(f"Server is running. Supported formats: {metadata_resp.json()}")
    else:
        print(f"Server returned unexpected status: {metadata_resp.status_code}")
        print(metadata_resp.text)
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to server. Make sure it's running on http://127.0.0.1:8000")
    sys.exit(1)

# Test blog generation
print("\nTesting blog generation with single keyword...")
blog_resp = requests.post(
    BLOG_ENDPOINT,
    json={
        "keywords": ["AI"],
        "language": "en",
        "word_count": 300,
        "format": "md",
        "frontmatter_schema": {
            "title": "string",
            "description": "string",
            "date": "datetime",
            "image": "string",
            "draft": "bool"
        },
        "components": ["quote"],
        "custom_rules": {
            "plain_direct_language": "Use short sentences and active voice."
        },
        "image_style": "Simple line drawing",
        "image_type": "webp",
        "image_size": "1024x1024",
        "image_url_suffix": "/images/blogs/"
    }
)

print(f"Blog endpoint response: {blog_resp.status_code}")
if blog_resp.status_code == 200:
    print("✅ SUCCESS! Blog generation completed.")
    data = blog_resp.json()
    print(f"File path: {data.get('file_path')}")
    print(f"Image path: {data.get('image_path')}")
else:
    print("❌ FAILED: Could not generate blog.")
    print(f"Error response: {blog_resp.text}")
    print("\nTroubleshooting steps:")
    print("1. Check if the server is running correctly")
    print("2. Verify your OpenAI API key is set correctly in .env")
    print("3. Check server logs for any additional errors") 