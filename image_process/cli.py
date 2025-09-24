#!/usr/bin/env python3
"""
图片处理工具入口点
支持命令行界面 (CLI) 和文本用户界面 (TUI)
"""

import typer
from typing import Optional
from image_process.main import run_cli, run_tui

app = typer.Typer(help="图片处理工具 - 支持 CLI 和 TUI 模式", no_args_is_help=True)


@app.command(help="运行命令行界面")
def cli():
    """运行命令行界面"""
    run_cli()


@app.command(help="运行文本用户界面")
def tui():
    """运行文本用户界面"""
    run_tui()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    mode: Optional[str] = typer.Option(
        "cli", "--mode", "-m", help="运行模式: cli (命令行界面) 或 tui (文本用户界面)"
    ),
):
    """
    图片处理工具 - 支持 CLI 和 TUI 模式
    """
    if ctx.invoked_subcommand is None:
        if mode and mode.lower() == "tui":
            run_tui()
        else:  # 默认为 CLI 模式
            run_cli()


if __name__ == "__main__":
    app()
