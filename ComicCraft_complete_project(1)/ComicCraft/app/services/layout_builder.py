from pathlib import Path

def build_comic_layout(story, image_paths: list[Path]):
    if len(story) != len(image_paths):
        raise ValueError("Every story panel must have exactly one image.")
    result = []
    for panel, image_path in zip(story, image_paths):
        result.append({
            "panel_number": panel.panel_number,
            "title": panel.title,
            "scene_description": panel.scene_description,
            "image_prompt": panel.image_prompt,
            "caption": panel.caption,
            "narration": panel.narration,
            "dialogue": panel.dialogue,
            "image_path": str(image_path),
            "image_url": f"/static/panels/{image_path.name}",
        })
    return result
