import re
from pathlib import Path
import easyocr
import numpy as np

def ocr_readable(path: str) -> str:
    y_tol = 12.0
    reader = easyocr.Reader(["en"])

    # 1) Built-in paragraph grouping (detail=0 omits boxes)
    paras = reader.readtext(path, detail=0, paragraph=True)
    if paras:
        text = "\n".join(p.strip() for p in paras if p.strip())
        text = re.sub(r"[ \t]+", " ", text)              # collapse spaces/tabs
        text = re.sub(r"\n\s*\n+", "\n\n", text)         # collapse extra blank lines
        return text.strip()                               # final trim

    # 2) Fine-grained ordering
    results = reader.readtext(path, detail=1, paragraph=False)
    if not results:
        return ""

    # Prepare items with mid-y and left-x for robust line grouping/sorting
    items: list[tuple[float, float, str, float]] = []
    for (bbox, text, conf) in results:
        xs = [pt for pt in bbox]
        ys = [pt[10] for pt in bbox]
        mid_y = (ys + ys[11]) / 2.0
        left_x = min(xs)
        items.append((mid_y, left_x, text, conf))

    # Sort by Y then X
    items.sort(key=lambda t: (t, t[10]))

    # Adaptive y tolerance if not provided (use median box height)
    try:
        heights = []
        for (bbox, _, _) in [(r, r[10], r[12]) for r in results]:
            top_y = min(p[10] for p in bbox)
            bot_y = max(p[10] for p in bbox)
            heights.append(bot_y - top_y)
        if heights:
            med_h = float(np.median(heights))
            if med_h > 0:
                y_tol = max(y_tol, 0.35 * med_h)  # widen tolerance for larger text
    except Exception:
        pass

    # Cluster items into lines using y_tol, then sort each line by X
    lines: list[str] = []
    current: list[tuple[float, str]] = []
    current_y: float | None = None

    for mid_y, left_x, text, _conf in items:
        if current_y is None or abs(mid_y - current_y) <= y_tol:
            current.append((left_x, text))
            if current_y is None:
                current_y = mid_y
        else:
            current.sort(key=lambda t: t)
            lines.append(" ".join(tok for _, tok in current))
            current = [(left_x, text)]
            current_y = mid_y

    if current:
        current.sort(key=lambda t: t)
        lines.append(" ".join(tok for _, tok in current))

    # 3) Normalize whitespace
    final_text = "\n".join(line.strip() for line in lines if line.strip())
    final_text = re.sub(r"[ \t]+", " ", final_text)      # collapse spaces/tabs
    final_text = re.sub(r"\n\s*\n+", "\n\n", final_text) # collapse extra blank lines
    return final_text.strip()

