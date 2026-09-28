import re
from pathlib import Path
from PIL import Image, ImageDraw

def _safe_filename(text):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return value[:60] or "panel"

def _placeholder(prompt, output_path, panel_number):
    image = Image.new("RGB", (1024, 768), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, 1004, 748), outline="black", width=5)
    draw.text((55, 55), f"ComicCraft — Panel {panel_number}", fill="black")
    draw.text((55, 130), prompt[:700], fill="black", spacing=8)
    image.save(output_path, "PNG")
    return output_path

def generate_image(prompt, panel_number, output_dir, provider, hf_token="", hf_model="", local_model=""):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"panel_{panel_number:02d}_{_safe_filename(prompt)}.png"

    if provider == "placeholder":
        return _placeholder(prompt, output_path, panel_number)

    if provider == "hf":
        if not hf_token:
            raise RuntimeError("HF_TOKEN is not configured.")
        from huggingface_hub import InferenceClient
        client = InferenceClient(provider="auto", api_key=hf_token)
        image = client.text_to_image(prompt=prompt, model=hf_model)
        image.save(output_path)
        return output_path

    if provider == "local":
        try:
            import torch
            from diffusers import StableDiffusionPipeline
        except ImportError as exc:
            raise RuntimeError(
                "Local mode requires torch, diffusers, transformers and accelerate."
            ) from exc
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionPipeline.from_pretrained(local_model, torch_dtype=dtype)
        pipe = pipe.to(device)
        image = pipe(prompt, num_inference_steps=25).images[0]
        image.save(output_path)
        return output_path

    raise RuntimeError(f"Unsupported IMAGE_PROVIDER: {provider}")
