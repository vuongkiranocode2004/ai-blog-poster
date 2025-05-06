flowchart TD
  A[Client Request] --> B[Validate Request]
  B --> C{Request type}
  C -->|Get metadata| D[Fetch Supported Config]
  D --> E[Return JSON Response]
  C -->|Generate Image| F[Call OpenAI Image API]
  F --> G[Save Images Locally]
  G --> H[Return Image Filenames]
  C -->|Generate Blog| I[Call OpenAI Text API]
  I --> J[Process Content Frontmatter Components Links]
  J --> K[Save Files Locally]
  K --> L[Return File Paths]
  B --> M[Error Handling]
  F --> M
  I --> M
  M --> N[Log Error and Return Error Response]