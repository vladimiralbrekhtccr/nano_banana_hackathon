# API Reference

## Gemini Client Configuration

### Basic Client Setup

```python
from google import genai
import os

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

## Content Generation

### generate_content()

Generate content using the Gemini 2.5 Flash Image model.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt, image],
    config=GenerateContentConfig(...)
)
```

**Parameters:**

- `model` (str): Model identifier - "gemini-2.5-flash-image-preview"
- `contents` (list): List containing prompt text and image objects
- `config` (GenerateContentConfig): Configuration object

## Configuration Options

### GenerateContentConfig

```python
from google.genai.types import GenerateContentConfig

config = GenerateContentConfig(
    temperature=0.7,          # Controls creativity (0.0-2.0)
    top_p=0.95,              # Nucleus sampling (0.1-1.0)
    top_k=20,                # Top-k sampling (1-40)
    max_output_tokens=1024,  # Maximum response length
    candidate_count=1,       # Number of response variants
    seed=42                  # For reproducible results
)
```

#### Parameters Explained

| Parameter | Range | Description |
|-----------|-------|-------------|
| `temperature` | 0.0-2.0 | Higher values = more creative/random output |
| `top_p` | 0.1-1.0 | Nucleus sampling threshold |
| `top_k` | 1-40 | Consider only top K tokens |
| `max_output_tokens` | 1-8192 | Maximum tokens in response |
| `candidate_count` | 1-8 | Number of response variants |
| `seed` | int | Seed for reproducible results |

## Response Processing

### Handling Response Parts

```python
for part in response.candidates[0].content.parts:
    if part.text is not None:
        # Text response
        print(part.text)
    elif part.inline_data is not None:
        # Image response
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("output.png")
```

## Image Processing

### Loading Images

```python
from PIL import Image

# Load from file
image = Image.open("path/to/image.png")

# Load from bytes
from io import BytesIO
image = Image.open(BytesIO(image_data))
```

### Supported Formats

- PNG
- JPEG
- WebP
- GIF (static frames)