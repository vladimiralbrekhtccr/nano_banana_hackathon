# Getting Started

## Prerequisites

- Python 3.8+
- UV package manager
- Google AI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nano_banana_hack
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google AI API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Demo

Execute the test script:

```bash
uv run src/demo_google_api/test_1.py
```

This will:

1. Load your API key from environment variables
2. Process an input image (`concat_1_2.png`)
3. Generate the next frame in a video sequence
4. Save the result as `generated_image.png`

## Configuration Options

The demo uses these configurable parameters:

- **temperature** (0.7): Controls creativity (0.0-2.0)
- **top_p** (0.95): Nucleus sampling (0.1-1.0)
- **top_k** (20): Top-k sampling (1-40)
- **max_output_tokens** (1024): Maximum response length
- **seed** (42): For reproducible results

## Troubleshooting

!!! warning "Common Issues"
    - Ensure your API key is correctly set in the `.env` file
    - Verify the input image path exists
    - Check your internet connection for API requests