#!/usr/bin/env python3
"""
图片处理 CLI 工具

该工具提供了一个命令行接口，用于合并多张图片。
"""

import typer
from typing import List, Tuple, Optional
from .merge_images import merge_images
import os

app = typer.Typer(
    help="图片处理 CLI 工具",
    no_args_is_help=True,
    epilog="示例: image-process --files img1.jpg --files img2.jpg --output result.jpg"
)

@app.command(help="合并多张图片")
def merge(
    files: List[str] = typer.Option(
        ..., 
        "--files", "-f",
        help="要合并的图片文件列表"
    ),
    output: str = typer.Option(
        ..., 
        "--output", "-o",
        help="输出文件路径"
    ),
    orientation: str = typer.Option(
        "horizontal", 
        "--orientation", 
        help="图片排列方向 (horizontal/vertical)"
    ),
    gap: int = typer.Option(
        40, 
        "--gap", 
        help="图片间距 (像素)"
    ),
    divider: bool = typer.Option(
        True, 
        "--divider/--no-divider", 
        help="是否添加分隔线"
    ),
    divider_thickness: int = typer.Option(
        4, 
        "--divider-thickness", 
        help="分隔线粗细 (像素)"
    ),
    divider_color: Tuple[int, int, int] = typer.Option(
        (200, 200, 200), 
        "--divider-color", 
        help="分隔线颜色 (R,G,B)"
    ),
    bg_color: Tuple[int, int, int] = typer.Option(
        (255, 255, 255), 
        "--bg-color", 
        help="背景颜色 (R,G,B)"
    ),
    align: str = typer.Option(
        "center", 
        "--align", 
        help="图片对齐方式 (start/center/end)"
    ),
    uniform_height: Optional[int] = typer.Option(
        None, 
        "--uniform-height", 
        help="统一高度 (仅在水平排列时有效)"
    ),
    uniform_width: Optional[int] = typer.Option(
        None, 
        "--uniform-width", 
        help="统一宽度 (仅在垂直排列时有效)"
    ),
    margin: int = typer.Option(
        0, 
        "--margin", 
        help="边距 (像素)"
    )
):
    """
    合并多张图片
    """
    # 检查输入文件是否存在
    for file in files:
        if not os.path.exists(file):
            typer.echo(f"错误: 文件 '{file}' 不存在", err=True)
            raise typer.Exit(code=1)
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 调用合并函数
    try:
        result = merge_images(
            files=files,
            output=output,
            orientation=orientation,
            gap=gap,
            divider=divider,
            divider_thickness=divider_thickness,
            divider_color=divider_color,
            bg_color=bg_color,
            align=align,
            uniform_height=uniform_height if orientation == "horizontal" else None,
            uniform_width=uniform_width if orientation == "vertical" else None,
            margin=margin
        )
        typer.echo(f"图片合并完成: {result}")
    except Exception as e:
        typer.echo(f"合并图片时出错: {str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()