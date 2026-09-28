from datetime import datetime
from pathlib import Path
from fpdf import FPDF

def save_pdf(layout, exports_dir: Path):
    exports_dir.mkdir(parents=True, exist_ok=True)
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = exports_dir / filename

    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}")
        image_path = Path(panel["image_path"])
        if image_path.exists():
            pdf.image(str(image_path), x=15, y=42, w=180)
        pdf.set_y(155)
        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, f"Caption: {panel['caption']}")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, f"Narration: {panel['narration']}")
        if panel.get("dialogue"):
            pdf.multi_cell(0, 7, f"Dialogue: {panel['dialogue']}")

    pdf.output(str(output))
    return output
