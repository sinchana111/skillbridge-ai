"""Resume parsing and privacy-safe previews."""
import re

def parse_pdf(data: bytes):
    """Extract selectable text and flag likely multi-column PDF pages."""
    import fitz
    if len(data) > 5 * 1024 * 1024:
        raise ValueError("PDF must be at most 5 MB")
    pages, warnings = [], []
    with fitz.open(stream=data, filetype="pdf") as doc:
        if len(doc) > 12:
            raise ValueError("PDF must be at most 12 pages")
        for page_no, page in enumerate(doc, 1):
            blocks = [b for b in page.get_text("blocks") if len(b)>4 and str(b[4]).strip()]
            blocks.sort(key=lambda b: (round(b[1]/12), b[0]))
            pages.append("\n".join(b[4].strip() for b in blocks))
            middle = page.rect.width / 2
            left = sum(1 for b in blocks if b[2] < middle)
            right = sum(1 for b in blocks if b[0] > middle)
            if left >= 2 and right >= 2:
                warnings.append(f"Page {page_no} may use multiple columns; verify reading order.")
    text = "\n".join(pages).strip()
    if not text:
        warnings.append("No selectable text found; scanned PDFs need OCR or pasted text.")
    return text, warnings

def mask_pii(text: str):
    """Best-effort masking. Not a guarantee of full anonymization."""
    text = re.sub(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[EMAIL]", text)
    text = re.sub(r"(?<!\w)(?:\+?\d[\d\s().-]{8,}\d)(?!\w)", "[PHONE]", text)
    return re.sub(r"https?://\S+|www\.\S+", "[URL]", text, flags=re.I)

def extract_sections(text: str):
    from engine import sections
    return sections(text)
