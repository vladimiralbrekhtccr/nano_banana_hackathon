# Examples

## Basic Image Generation

### Video Frame Continuation

This example shows how to generate the next frame in a video sequence:

```python
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from PIL import Image
from io import BytesIO

load_dotenv()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

prompt = "You received a frame from video. Generate the next frame"
image = Image.open("input_frame.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt, image],
    config=GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=20,
        max_output_tokens=1024,
        seed=42
    )
)

# Process response
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        next_frame = Image.open(BytesIO(part.inline_data.data))
        next_frame.save("next_frame.png")
```

## Advanced Examples

### Character Consistency

Create consistent characters across multiple images:

```python
prompt = """
Generate the next frame showing the same character continuing their action.
Maintain consistent appearance, lighting, and style.
"""

config = GenerateContentConfig(
    temperature=0.3,  # Lower temperature for consistency
    seed=42          # Fixed seed for reproducibility
)
```

### Style Transfer

Apply artistic styles to images:

```python
prompt = """
Transform this image to match the style of a watercolor painting
while preserving the main subject and composition.
"""

config = GenerateContentConfig(
    temperature=0.8,  # Higher creativity for artistic effects
    top_k=30
)
```

### Batch Processing

Process multiple frames:

```python
def process_video_frames(frame_paths, base_prompt):
    results = []
    
    for i, frame_path in enumerate(frame_paths):
        image = Image.open(frame_path)
        prompt = f"{base_prompt} - Frame {i+1}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt, image],
            config=GenerateContentConfig(
                temperature=0.7,
                seed=42 + i  # Vary seed slightly
            )
        )
        
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                result_image = Image.open(BytesIO(part.inline_data.data))
                output_path = f"processed_frame_{i+1}.png"
                result_image.save(output_path)
                results.append(output_path)
    
    return results
```

## Tips and Best Practices

!!! tip "Optimal Settings"
    - Use `temperature=0.3-0.5` for consistent results
    - Use `temperature=0.7-1.0` for creative variations
    - Set a fixed `seed` for reproducible outputs
    - Adjust `top_k` and `top_p` for fine-tuning creativity

!!! example "Prompt Engineering"
    - Be specific about desired changes
    - Mention style, lighting, and composition requirements
    - Use references to previous frames for consistency
    - Include technical details (resolution, format, etc.)

!!! warning "Rate Limits"
    - Be mindful of API rate limits
    - Implement proper error handling
    - Consider batching requests efficiently