#!/usr/bin/env python3
"""
图片处理工具入口点
支持命令行界面 (CLI) 和文本用户界面 (TUI)
"""

import typer
import os
import json
from typing import Optional
from image_process.main import run_cli, run_tui

# Configuration directory and file
CONFIG_DIR = os.path.expanduser("~/.config/image-process-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config():
    """
    加载配置文件
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}


def save_config(config):
    """
    保存配置文件
    """
    # 读取现有配置以保留图像处理相关设置
    existing_config = load_config()

    # 将CLI特定配置合并到现有配置中
    existing_config.update(config)

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_config, f, indent=4, ensure_ascii=False)


app = typer.Typer(help="图片处理工具 - 支持 CLI 和 TUI 模式")


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
        None, "--mode", "-m", help="运行模式: cli (命令行界面) 或 tui (文本用户界面)"
    ),
    config_mode: Optional[str] = typer.Option(
        None,
        "--config-mode",
        "-c",
        help="设置默认运行模式: cli 或 tui (这将保存到配置文件中)",
    ),
    show_help: bool = typer.Option(
        None, "--help", "-h", is_eager=True, help="显示帮助信息"
    ),
):
    """
    图片处理工具 - 支持 CLI 和 TUI 模式

    默认行为: 根据配置文件中的设置运行 CLI 或 TUI
    使用 --help 参数可查看使用帮助
    使用 --config-mode 可设置默认运行模式
    """
    if show_help:
        # Print help information
        print("图片处理工具 - 支持 CLI 和 TUI 模式")
        print("")
        print("使用方法:")
        print("  image-process              # 根据配置文件运行 CLI 或 TUI")
        print("  image-process --mode cli   # 运行命令行界面")
        print("  image-process --mode tui   # 运行文本用户界面")
        print("  image-process --config-mode cli  # 设置默认为 CLI 模式")
        print("  image-process --config-mode tui  # 设置默认为 TUI 模式")
        print("  image-process --help       # 显示此帮助信息")
        print("")
        print("子命令:")
        print("  cli  运行命令行界面")
        print("  tui  运行文本用户界面")
        print("")
        return

    # If setting the config mode
    if config_mode:
        if config_mode.lower() in ["cli", "tui"]:
            config = load_config()
            config["default_mode"] = config_mode.lower()
            save_config(config)
            print(f"默认运行模式已设置为: {config_mode.lower()}")
        else:
            print("错误: 模式必须是 'cli' 或 'tui'")
        return

    if ctx.invoked_subcommand is None:
        # Load configuration
        config = load_config()

        # Determine the default mode from config, fallback to CLI
        config_default_mode = config.get("default_mode", "cli")

        # Use mode from command line option if provided, otherwise use config default
        selected_mode = mode if mode is not None else config_default_mode

        if selected_mode and selected_mode.lower() == "tui":
            run_tui()
        else:  # Default to CLI mode
            run_cli()


if __name__ == "__main__":
    app()
