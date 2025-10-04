#!/usr/bin/env python3
"""
图片处理 TUI 工具

该工具提供了一个交互式的文本用户界面，用于合并多张图片。
"""

import os
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from .merge_images import merge_images
from datetime import datetime
from .config import ConfigManager
from .file_selector import FileSelector
from .menu import MenuManager
from .settings_configurer import SettingsConfigurer


class ImageProcessorTUI:
    """
    图片处理 TUI 类
    """

    def __init__(self):
        self.console = Console()
        self.files = []
        self.config = ConfigManager()
        self.menu_manager = MenuManager(self.console)
        self.settings_configurer = SettingsConfigurer(self.console)

    def run(self):
        """
        运行 TUI 界面
        """
        self.console.print(Panel("[bold blue]图片处理工具[/bold blue]", expand=False))
        self.console.print("[green]欢迎使用图片处理工具 TUI 版本！[/green]\n")

        while True:
            # 显示主菜单
            choice = self.menu_manager.show_menu(len(self.files), self.config.output)

            if choice == "1":
                self.add_files()
            elif choice == "2":
                self.remove_file()
            elif choice == "3":
                self.set_output_path()
            elif choice == "4":
                self.configure_settings()
            elif choice == "5":
                self.show_current_config()
            elif choice == "6":
                self.process_images()
            elif choice == "7":
                self.reset_config()
            elif choice == "8":
                self.menu_manager.show_help()
            elif choice == "0":
                self.console.print("[yellow]再见！[/yellow]")
                break

    def add_files(self):
        """
        添加图片文件
        """
        selector = FileSelector()
        selected_files = selector.run()
        if selected_files:
            for file_path in selected_files:
                if os.path.exists(file_path):
                    self.files.append(file_path)
                    self.console.print(f"[green]已添加文件: {file_path}[/green]")
                else:
                    self.console.print(f"[red]文件不存在: {file_path}[/red]")

    def remove_file(self):
        """
        移除图片文件
        """
        if not self.files:
            self.console.print("[yellow]没有已添加的文件[/yellow]")
            return

        self.console.print("\n[bold]当前已添加的文件:[/bold]")
        for i, file in enumerate(self.files, 1):
            self.console.print(f"{i}. {file}")

        try:
            index = int(Prompt.ask("[bold]请输入要移除的文件编号 (0取消):[/bold]")) - 1
            if 0 <= index < len(self.files):
                removed_file = self.files.pop(index)
                self.console.print(f"[green]已移除文件: {removed_file}[/green]")
            elif index == -1:
                self.console.print("[yellow]取消操作[/yellow]")
            else:
                self.console.print("[red]无效的编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")

    def set_output_path(self):
        """
        设置输出路径
        """
        self.config.output = Prompt.ask("[bold]请输入输出文件路径:[/bold]")
        self.console.print(f"[green]输出路径已设置为: {self.config.output}[/green]")
        self.config.save_config()

    def configure_settings(self):
        """
        配置合并参数
        """
        self.settings_configurer.configure_settings(self.config)
        self.config.save_config()

    def show_current_config(self):
        """
        显示当前配置
        """
        self.menu_manager.show_config_table(self.config)

        if self.files:
            self.console.print("\n[bold]已添加的文件:[/bold]")
            for i, file in enumerate(self.files, 1):
                self.console.print(f"{i}. {file}")
        else:
            self.console.print("\n[yellow]尚未添加任何文件[/yellow]")

        if self.config.output:
            self.console.print(f"\n[bold]输出路径:[/bold] {self.config.output}")
        else:
            self.console.print("\n[yellow]未设置输出路径[/yellow]")

    def process_images(self):
        """
        执行图片合并
        """
        if not self.files:
            self.console.print("[red]错误: 尚未添加任何图片文件[/red]")
            return

        if not self.config.output:
            self.console.print("[red]错误: 尚未设置输出路径[/red]")
            return

        # 检查所有输入文件是否存在
        missing_files = []
        for file in self.files:
            if not os.path.exists(file):
                missing_files.append(file)

        if missing_files:
            self.console.print("[red]以下文件不存在:[/red]")
            for file in missing_files:
                self.console.print(f"  - {file}")
            return

        # 添加时间戳到输出文件名
        original_output = self.config.output
        if self.config.add_timestamp:
            name, ext = os.path.splitext(self.config.output)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.config.output = f"{name}_{timestamp}{ext}"

        # 确保输出目录存在
        output_dir = os.path.dirname(self.config.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 显示当前配置供用户确认
        self.console.print("\n[bold]即将执行图片合并，当前配置:[/bold]")
        self.show_current_config()

        if not Confirm.ask("\n确认执行合并操作?", default=True):
            self.console.print("[yellow]操作已取消[/yellow]")
            return

        try:
            result = merge_images(
                files=self.files,
                output=self.config.output,
                orientation=self.config.orientation,
                gap=self.config.gap,
                divider=self.config.divider,
                divider_thickness=self.config.divider_thickness,
                divider_color=self.config.divider_color,
                bg_color=self.config.bg_color,
                align=self.config.align,
                uniform_height=self.config.uniform_height
                if self.config.orientation == "horizontal"
                else None,
                uniform_width=self.config.uniform_width
                if self.config.orientation == "vertical"
                else None,
                margin=self.config.margin,
                cols=self.config.cols,
                rows=self.config.rows,
            )
            self.console.print(f"[green]图片合并完成: {result}[/green]")

            # 合成完成后自动清空已选择的图片列表
            self.console.print("[green]正在自动清空已选择的图片列表...[/green]")
            self.files.clear()
            self.console.print("[green]图片列表已清空[/green]")

        except Exception as e:
            self.console.print(f"[red]合并图片时出错: {str(e)}[/red]")
        finally:
            # 恢复原始输出路径
            self.config.output = original_output

    def reset_config(self):
        """
        重置配置为默认值
        """
        if Confirm.ask("确认重置所有配置为默认值?", default=False):
            # 保留文件列表，只重置其他设置
            files_backup = self.files[:]
            self.config.reset_to_defaults()
            self.files = files_backup
            self.console.print("[green]配置已重置为默认值[/green]")
            self.config.save_config()
        else:
            self.console.print("[yellow]操作已取消[/yellow]")


def run_tui():
    """
    运行 TUI 界面的入口点
    """
    app = ImageProcessorTUI()
    app.run()


if __name__ == "__main__":
    run_tui()
