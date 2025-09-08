import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from PIL import Image
from io import BytesIO

load_dotenv()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

prompt = (
    "You received a frame from video. Generate the next frame how she goes just next 3-rd frame",
)

image_1 = Image.open("../cute_girl.png")
image_2 = Image.open("../cute_girl_2_step.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt, image_1, image_2],
    config=GenerateContentConfig(
        temperature=1.0,          # Controls creativity (0.0-2.0, higher = more creative)
        top_p=0.95,              # Nucleus sampling (0.1-1.0)
        top_k=50,                # Top-k sampling (1-40)
        max_output_tokens=1024,  # Maximum response length
        candidate_count=1,       # Number of response variants
        seed=42,                 # For reproducible results (optional)
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("generated_image.png")