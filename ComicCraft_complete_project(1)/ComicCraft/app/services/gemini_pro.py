import json
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas import PanelOutline, PromptRequest, StoryPanel, StoryResponse

def _client():
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)

def generate_story(request: PromptRequest, outline: list[PanelOutline]):
    settings = get_settings()
    outline_json = json.dumps([p.model_dump() for p in outline], ensure_ascii=False)
    prompt = f"""
Expand this outline into a polished comic story.

Story idea: {request.story_prompt}
Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline_json}

Return ONLY JSON:
{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "...",
      "scene_description": "...",
      "image_prompt": "...",
      "caption": "...",
      "narration": "...",
      "dialogue": "..."
    }}
  ]
}}

Rules:
- Exactly {settings.panels_count} panels.
- Preserve panel order and continuity.
- Keep narration concise and engaging.
- Dialogue should be short and natural.
"""
    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
        ),
    )
    raw = (response.text or "").strip()
    if not raw:
        raise RuntimeError("Gemini Pro returned an empty response.")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini Pro returned invalid JSON.") from exc
    result = StoryResponse.model_validate(data)
    if len(result.panels) != settings.panels_count:
        raise RuntimeError("Gemini Pro did not return the required number of panels.")
    return result.panels
