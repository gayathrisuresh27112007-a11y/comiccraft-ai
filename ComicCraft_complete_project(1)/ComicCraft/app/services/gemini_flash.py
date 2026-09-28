import json
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas import PanelOutline, PromptRequest

def _client():
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)

def generate_outline(request: PromptRequest):
    settings = get_settings()
    prompt = f"""
Create exactly {settings.panels_count} connected comic panels.

Story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Return ONLY JSON:
{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "short title",
      "scene_description": "visible scene description",
      "image_prompt": "detailed image-generation prompt"
    }}
  ]
}}

Requirements:
- Exactly {settings.panels_count} panels numbered 1 through {settings.panels_count}.
- Keep the main character consistent.
- Give the story a beginning, development and ending.
- image_prompt must describe the visible character, setting, action, lighting, composition and art style.
- Do not put dialogue inside image_prompt.
"""
    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
        ),
    )
    raw = (response.text or "").strip()
    if not raw:
        raise RuntimeError("Gemini Flash returned an empty response.")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini Flash returned invalid JSON.") from exc
    panels = data.get("panels")
    if not isinstance(panels, list) or len(panels) != settings.panels_count:
        raise RuntimeError("Gemini Flash did not return the required number of panels.")
    return [PanelOutline.model_validate(p) for p in panels]
