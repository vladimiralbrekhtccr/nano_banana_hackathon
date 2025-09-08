# Nano Banana Hackathon Project

## Overview
This project is built for the Nano Banana Hackathon, showcasing applications using Gemini 2.5 Flash Image features. The goal is to create innovative demos that leverage advanced image capabilities including consistency, fusion, and editing.

## Project Structure
- `src/demo_google_api/` - Contains demo implementations using Google's Gemini API
- `src/demo_google_api/test_1.py` - Test script for video frame generation using Gemini 2.5 Flash Image

## Dependencies
This project uses `uv` for Python package management.

### Key Dependencies
- `google-genai` - Google Generative AI client
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing

## Setup
1. Install dependencies with uv:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   - Create a `.env` file
   - Add your `GEMINI_API_KEY`

## Features
- Video frame generation and continuation
- Image processing with Gemini 2.5 Flash Image
- Configurable generation parameters (temperature, top_p, top_k, etc.)

## Hackathon Focus Areas
The project aims to showcase:
- Dynamic storytelling through consistent character generation
- Advanced image editing capabilities
- Creative workflow automation
- Natural language photo editing

## Submission Requirements
- 2-minute video demo
- Public project link/demo
- Gemini integration writeup (max 200 words)

## Running Tests
```bash
uv run src/demo_google_api/test_1.py
```

## Documentation with MkDocs

This project includes MkDocs documentation setup.

### Install MkDocs dependencies
```bash
uv add --group docs mkdocs mkdocs-material mkdocstrings[python] pymdown-extensions
```

### Serve documentation locally
```bash
uv run mkdocs serve
```
Then open http://127.0.0.1:8000 in your browser.

### Build documentation
```bash
uv run mkdocs build
```

### Deploy to GitHub Pages
```bash
uv run mkdocs gh-deploy
```