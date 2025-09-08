import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from PIL import Image
from io import BytesIO
import datetime
import json

load_dotenv()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

def generate_content(image1, image2, custom_prompt, temperature, top_p, top_k, max_tokens, seed):
    """
    Generate content based on one or two input images
    """
    if image1 is None:
        return None, None, "Please upload at least one image"
    
    # Default prompt if none provided
    if image2 is not None:
        prompt = custom_prompt or "You received frames from video. Generate the next frame how she goes just next 3-rd frame"
        images = [image1, image2]
    else:
        prompt = custom_prompt or "Describe this image and generate a creative continuation or variation"
        images = [image1]
    
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Convert gradio images to PIL if needed
        processed_images = []
        for img in images:
            if hasattr(img, 'save'):
                processed_images.append(img)
            else:
                processed_images.append(Image.fromarray(img))
        
        # Generate content using Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt] + processed_images,
            config=GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=int(top_k),
                max_output_tokens=int(max_tokens),
                candidate_count=1,
                seed=int(seed) if seed else None,
            )
        )
        
        # Process response
        generated_image = None
        text_output = ""
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_output += part.text + "\n"
            elif part.inline_data is not None:
                generated_image = Image.open(BytesIO(part.inline_data.data))
        
        # Save session data
        session_data = {
            "timestamp": timestamp,
            "prompt": prompt,
            "parameters": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": int(top_k),
                "max_tokens": int(max_tokens),
                "seed": int(seed) if seed else None
            },
            "text_output": text_output.strip(),
            "num_input_images": len(images)
        }
        
        # Save input images
        input_paths = []
        for i, img in enumerate(processed_images):
            input_path = f"outputs/input_{timestamp}_{i+1}.png"
            img.save(input_path)
            input_paths.append(input_path)
        session_data["input_images"] = input_paths
        
        # Save generated image if available
        if generated_image:
            output_path = f"outputs/generated_{timestamp}.png"
            generated_image.save(output_path)
            session_data["output_image"] = output_path
        
        # Save session metadata
        with open(f"outputs/session_{timestamp}.json", "w") as f:
            json.dump(session_data, f, indent=2)
        
        status_msg = f"Content generated successfully! Saved to outputs/session_{timestamp}.json"
        if text_output:
            status_msg += f"\n\nGenerated text: {text_output.strip()}"
        
        return generated_image, output_path if generated_image else None, status_msg
        
    except Exception as e:
        return None, None, f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Gemini Image Generation Demo") as demo:
    gr.Markdown("# Image Generation with Gemini 2.5 Flash")
    gr.Markdown("Upload 1 or 2 images and generate content. With 2 images, it creates video frame continuation. With 1 image, it creates variations or descriptions.")
    
    with gr.Row():
        with gr.Column():
            image1 = gr.Image(label="Image 1 (Required)", type="pil")
            image2 = gr.Image(label="Image 2 (Optional - for video frame continuation)", type="pil")
            prompt_input = gr.Textbox(
                label="Custom Prompt (optional)",
                placeholder="Leave empty for automatic prompts based on number of images",
                lines=3
            )
            
            with gr.Accordion("Generation Parameters", open=False):
                temperature = gr.Slider(
                    minimum=0.0, maximum=2.0, value=0.7, step=0.1,
                    label="Temperature (creativity)"
                )
                top_p = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.95, step=0.05,
                    label="Top-p (nucleus sampling)"
                )
                top_k = gr.Slider(
                    minimum=1, maximum=100, value=50, step=1,
                    label="Top-k (diversity)"
                )
                max_tokens = gr.Slider(
                    minimum=64, maximum=2048, value=1024, step=64,
                    label="Max output tokens"
                )
                seed = gr.Number(
                    label="Seed (optional, for reproducibility)",
                    value=42,
                    precision=0
                )
            
            generate_btn = gr.Button("Generate Content", variant="primary")
            
        with gr.Column():
            output_image = gr.Image(label="Generated Content")
            output_file = gr.File(label="Download Generated Image")
            output_text = gr.Textbox(label="Status/Description", lines=5)
    
    # Info section
    gr.Markdown("## Features")
    gr.Markdown("""
    **Dynamic Parameters:** Adjust temperature, top-p, top-k, max tokens, and seed in real-time
    
    **Auto-Save:** All generations are automatically saved to the `outputs/` directory with:
    - Input images
    - Generated images 
    - Session metadata (prompt, parameters, timestamp)
    - JSON file with all session details
    
    **Model:** Uses Gemini 2.5 Flash Image Preview for high-quality image generation
    """)
    
    # Connect the function
    generate_btn.click(
        fn=generate_content,
        inputs=[image1, image2, prompt_input, temperature, top_p, top_k, max_tokens, seed],
        outputs=[output_image, output_file, output_text]
    )

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7591)