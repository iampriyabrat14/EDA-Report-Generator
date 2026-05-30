import base64
import os
from pathlib import Path
from xhtml2pdf import pisa


def _embed_images(html: str) -> str:
    """Replace local image src paths with base64 data URIs so PDF renders charts."""
    import re

    def replace_src(match):
        src = match.group(1)
        if src.startswith("http"):
            return match.group(0)
        path = Path(src)
        if not path.exists():
            return match.group(0)
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = path.suffix.lstrip(".").lower()
        mime = "image/png" if ext == "png" else f"image/{ext}"
        return f'src="data:{mime};base64,{b64}"'

    return re.sub(r'src="([^"]+)"', replace_src, html)


def html_to_pdf(html: str, output_path: str) -> str:
    html_with_images = _embed_images(html)

    with open(output_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_with_images, dest=f, encoding="utf-8")

    if pisa_status.err:
        raise RuntimeError(f"PDF generation failed with {pisa_status.err} errors.")

    return output_path
