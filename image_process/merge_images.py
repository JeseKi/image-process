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
    cols: Optional[int] = None,
    rows: Optional[int] = None,
) -> str:
    assert orientation in ("horizontal", "vertical")
    assert gap >= 0 and divider_thickness >= 0 and margin >= 0

    images = [Image.open(f).convert("RGBA") for f in files]

    # 如果指定了网格布局参数，则使用网格布局
    if cols is not None or rows is not None:
        return _merge_images_grid(
            images=images,
            output=output,
            gap=gap,
            divider=divider,
            divider_thickness=divider_thickness,
            divider_color=divider_color,
            bg_color=bg_color,
            align=align,
            margin=margin,
            cols=cols,
            rows=rows,
        )
    else:
        # 使用原有的线性布局
        return _merge_images_linear(
            images=images,
            output=output,
            orientation=orientation,
            gap=gap,
            divider=divider,
            divider_thickness=divider_thickness,
            divider_color=divider_color,
            bg_color=bg_color,
            align=align,
            uniform_height=uniform_height,
            uniform_width=uniform_width,
            margin=margin,
        )


def _merge_images_linear(
    images: List[Image.Image],
    output: str,
    orientation: str,
    gap: int,
    divider: bool,
    divider_thickness: int,
    divider_color: Tuple[int, int, int],
    bg_color: Tuple[int, int, int],
    align: str,
    uniform_height: Optional[int],
    uniform_width: Optional[int],
    margin: int,
) -> str:
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


def _merge_images_grid(
    images: List[Image.Image],
    output: str,
    gap: int,
    divider: bool,
    divider_thickness: int,
    divider_color: Tuple[int, int, int],
    bg_color: Tuple[int, int, int],
    align: str,
    margin: int,
    cols: Optional[int],
    rows: Optional[int],
) -> str:
    n = len(images)

    # 计算网格布局的行列数
    if cols is not None and rows is not None:
        # 如果同时指定行数和列数，直接使用
        grid_cols = cols
        grid_rows = rows
    elif cols is not None:
        # 如果只指定列数，计算所需行数
        grid_cols = cols
        grid_rows = (n + grid_cols - 1) // grid_cols  # 向上取整
    elif rows is not None:
        # 如果只指定行数，计算所需列数
        grid_rows = rows
        grid_cols = (n + grid_rows - 1) // grid_rows  # 向上取整
    else:
        # 这种情况不应该发生，但为了安全起见
        grid_cols = int(n**0.5)  # 简单的平方根布局
        grid_rows = (n + grid_cols - 1) // grid_cols

    # 确保网格大小能容纳所有图像
    if grid_cols * grid_rows < n:
        if cols is not None:  # 如果固定了列数
            grid_rows = (n + grid_cols - 1) // grid_cols
        elif rows is not None:  # 如果固定了行数
            grid_cols = (n + grid_rows - 1) // grid_rows
        else:  # 都没固定则调整
            grid_cols = int(n**0.5)
            grid_rows = (n + grid_cols - 1) // grid_cols

    # 统一调整图像大小
    # 找到网格中每个位置对应的实际图片，计算目标尺寸
    max_width = 0
    max_height = 0

    for img in images:
        max_width = max(max_width, img.width)
        max_height = max(max_height, img.height)

    # 缩放所有图片到统一尺寸
    resized_images = []
    for img in images:
        resized_img = img.resize((max_width, max_height), Image.Resampling.LANCZOS)
        resized_images.append(resized_img)

    # 计算画布尺寸
    total_gap_cols = max(grid_cols - 1, 0)
    total_gap_rows = max(grid_rows - 1, 0)
    total_divider_cols = total_gap_cols * (
        divider_thickness if divider and divider_thickness > 0 else 0
    )
    total_divider_rows = total_gap_rows * (
        divider_thickness if divider and divider_thickness > 0 else 0
    )

    canvas_w = (
        grid_cols * max_width + total_gap_cols * gap + total_divider_cols + 2 * margin
    )
    canvas_h = (
        grid_rows * max_height + total_gap_rows * gap + total_divider_rows + 2 * margin
    )

    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_color + (255,))
    draw = ImageDraw.Draw(canvas)

    # 放置图像到网格中
    for idx, img in enumerate(resized_images):
        # 计算网格中的行和列
        row = idx // grid_cols
        col = idx % grid_cols

        # 计算在画布上的位置
        x = margin + col * (
            max_width
            + gap
            + (divider_thickness if divider and divider_thickness > 0 else 0)
        )
        y = margin + row * (
            max_height
            + gap
            + (divider_thickness if divider and divider_thickness > 0 else 0)
        )

        # 如果启用了divider，需要考虑divider的偏移
        if divider and divider_thickness > 0:
            x += col * divider_thickness
            y += row * divider_thickness

        # 绘制divider（如果是非最后一列或最后一行）
        if divider and divider_thickness > 0 and col < grid_cols - 1:
            # 垂直divider
            x0 = x + max_width
            x1 = x0 + divider_thickness - 1
            y0 = y
            y1 = y + max_height - 1
            draw.rectangle([x0, y0, x1, y1], fill=divider_color)

        if divider and divider_thickness > 0 and row < grid_rows - 1:
            # 水平divider
            x0 = x
            x1 = x + max_width - 1
            y0 = y + max_height
            y1 = y0 + divider_thickness - 1
            draw.rectangle([x0, y0, x1, y1], fill=divider_color)

        canvas.paste(img, (x, y), img)

    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    canvas.convert("RGB").save(output)
    return output
