# ComicCraft — AI Comic Story Creator

This is a complete FastAPI + Jinja2 implementation of the supplied ComicCraft project documentation.

Workflow:
1. Gemini creates a structured 5-panel outline.
2. Gemini expands it into narration, captions and dialogue.
3. Hugging Face generates an illustration for every panel.
4. The panels are assembled into a downloadable PDF.

## Requirements
- Python 3.11+
- Gemini API key
- Hugging Face token with inference permission
- VS Code recommended

## Windows setup

```powershell
cd ComicCraft
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your keys.

```text
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token
```

Run:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

Run tests:

```powershell
pytest
```

## Image generation

The default is `IMAGE_PROVIDER=hf`, using Hugging Face Inference Providers.

For UI/PDF testing without image-generation credits, set:

```text
IMAGE_PROVIDER=placeholder
```

For local Diffusers, install PyTorch/Diffusers/Transformers/Accelerate and set:

```text
IMAGE_PROVIDER=local
LOCAL_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
```

Local diffusion can require substantial RAM/VRAM.

## Project structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── schemas.py
│   └── services/
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
├── templates/
├── static/
├── tests/
├── requirements.txt
├── .env.example
└── .gitignore
```

Never commit `.env` or API tokens.
