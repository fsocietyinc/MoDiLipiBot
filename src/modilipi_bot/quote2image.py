import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


def get_project_root():
    """Find the project root by searching for pyproject.toml upwards."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Could not find project root (pyproject.toml not found)")


BASE_DIR = get_project_root()


def convert(
    quote,
    fg,
    image,
    border_color,
    font_file=None,
    font_size=None,
    width=None,
    height=None,
):
    x1 = width if width else 1920
    y1 = height if height else 1080
    font_size = font_size if font_size else 120

    sentence = f"{quote}"

    quote_font = ImageFont.truetype(
        str(BASE_DIR / "assets" / "fonts" / "NotoSansModiAdvanced.ttf"),
        font_size,
        layout_engine=ImageFont.Layout.RAQM,
    )

    img = Image.new("RGB", (x1, y1), color=(255, 255, 255))

    # Properly resize and crop the background image to fill the canvas
    back = Image.open(image)
    back = ImageOps.fit(back, (x1, y1), Image.Resampling.LANCZOS)
    
    # Apply a high-quality blur
    bback = back.filter(ImageFilter.GaussianBlur(radius=8))
    img.paste(bback, (0, 0))

    d = ImageDraw.Draw(img)

    # Better text wrapping using exact text width
    max_text_width = x1 * 0.85  # Use 85% of the image width
    lines = []
    
    for paragraph in sentence.split('\n'):
        if not paragraph.strip():
            lines.append("")
            continue
            
        words = paragraph.split(' ')
        current_line = []
        for word in words:
            if word == "-":
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                lines.append("")
                lines.append("-")
            else:
                test_line = ' '.join(current_line + [word]) if current_line else word
                if d.textlength(test_line, font=quote_font) <= max_text_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
        if current_line:
            lines.append(' '.join(current_line))

    fresh_sentence = '\n'.join(lines).strip()

    # Calculate text bounding box for centering
    bbox = d.multiline_textbbox((0, 0), fresh_sentence, font=quote_font, align="center")
    x2 = bbox[2] - bbox[0]
    y2 = bbox[3] - bbox[1]

    qx = x1 / 2 - x2 / 2
    qy = y1 / 2 - y2 / 2

    # Draw text with high quality stroke instead of manual 1px offsets
    stroke_w = max(1, font_size // 25)
    
    d.multiline_text(
        (qx, qy), 
        fresh_sentence, 
        align="center", 
        font=quote_font, 
        fill=fg,
        stroke_width=stroke_w,
        stroke_fill=border_color
    )

    return img


def get_base64(image):
    img = Image.open(image)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode()
