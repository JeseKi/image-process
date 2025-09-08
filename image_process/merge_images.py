from PIL import Image, ImageDraw
from typing import List, Tuple, Optional
import os


def merge_images(
    files: List[str],
    output: str,
    orientation: str = "horizontal",
    gap: int = 40,
    divider: bool = True,
    divider_thickness: int = 4,
    divider_color: Tuple[int, int, int] = (200, 200, 200),
    bg_color: Tuple[int, int, int] = (255, 255, 255),
    align: str = "center",
    uniform_height: Optional[int] = None,
    uniform_width: Optional[int] = None,
    margin: int = 0,
) -> str:
    assert orientation in ("horizontal", "vertical")
    assert gap >= 0 and divider_thickness >= 0 and margin >= 0

    images = [Image.open(f).convert("RGBA") for f in files]

    if orientation == "horizontal" and uniform_height is not None:
        new_imgs = []
        for im in images:
            w, h = im.size
            nh = uniform_height
            nw = int(w * nh / h)
            new_imgs.append(im.resize((nw, nh), Image.Resampling.LANCZOS))
        images = new_imgs
    elif orientation == "vertical" and uniform_width is not None:
        new_imgs = []
        for im in images:
            w, h = im.size
            nw = uniform_width
            nh = int(h * nw / w)
            new_imgs.append(im.resize((nw, nh), Image.Resampling.LANCZOS))
        images = new_imgs

    widths = [im.width for im in images]
    heights = [im.height for im in images]
    n = len(images)
    num_gaps = max(n - 1, 0)

    total_dividers = num_gaps * (
        divider_thickness if divider and divider_thickness > 0 else 0
    )

    if orientation == "horizontal":
        canvas_w = sum(widths) + num_gaps * gap + total_dividers + 2 * margin
        canvas_h = max(heights) + 2 * margin
    else:
        canvas_w = max(widths) + 2 * margin
        canvas_h = sum(heights) + num_gaps * gap + total_dividers + 2 * margin

    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_color + (255,))
    draw = ImageDraw.Draw(canvas)

    cursor_x, cursor_y = margin, margin
    for idx, im in enumerate(images):
        w, h = im.size

        if orientation == "horizontal":
            if align == "center":
                paste_y = margin + (canvas_h - 2 * margin - h) // 2
            elif align == "end":
                paste_y = canvas_h - margin - h
            else:
                paste_y = margin
            canvas.paste(im, (cursor_x, paste_y), im)
            cursor_x += w

            if idx < n - 1:
                half_gap_left = gap // 2
                cursor_x += half_gap_left
                if divider and divider_thickness > 0:
                    x0 = cursor_x
                    x1 = cursor_x + divider_thickness - 1
                    y0 = margin
                    y1 = canvas_h - margin - 1
                    draw.rectangle([x0, y0, x1, y1], fill=divider_color)
                    cursor_x += divider_thickness
                half_gap_right = gap - half_gap_left
                cursor_x += half_gap_right
        else:
            if align == "center":
                paste_x = margin + (canvas_w - 2 * margin - w) // 2
            elif align == "end":
                paste_x = canvas_w - margin - w
            else:
                paste_x = margin
            canvas.paste(im, (paste_x, cursor_y), im)
            cursor_y += h

            if idx < n - 1:
                half_gap_top = gap // 2
                cursor_y += half_gap_top
                if divider and divider_thickness > 0:
                    x0 = margin
                    x1 = canvas_w - margin - 1
                    y0 = cursor_y
                    y1 = cursor_y + divider_thickness - 1
                    draw.rectangle([x0, y0, x1, y1], fill=divider_color)
                    cursor_y += divider_thickness
                half_gap_bottom = gap - half_gap_top
                cursor_y += half_gap_bottom

    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    canvas.convert("RGB").save(output)
    return output
