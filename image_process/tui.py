#!/usr/bin/env python3
"""
图片处理 TUI 工具

该工具提供了一个交互式的文本用户界面，用于合并多张图片。
"""

import os
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.panel import Panel
from .merge_images import merge_images


class ImageProcessorTUI:
    """
    图片处理 TUI 类
    """

    def __init__(self):
        self.console = Console()
        self.files = []
        self.output = ""
        self.orientation = "horizontal"
        self.gap = 40
        self.divider = True
        self.divider_thickness = 4
        self.divider_color = (200, 200, 200)
        self.bg_color = (255, 255, 255)
        self.align = "center"
        self.uniform_height = None
        self.uniform_width = None
        self.margin = 0

    def run(self):
        """
        运行 TUI 界面
        """
        self.console.print(Panel("[bold blue]图片处理工具[/bold blue]", expand=False))
        self.console.print("[green]欢迎使用图片处理工具 TUI 版本！[/green]\\n")

        while True:
            # 显示主菜单
            self.show_menu()
            choice = Prompt.ask(
                "[bold]请选择操作[/bold]",
                choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                default="1",
            )

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
                self.show_help()
            elif choice == "0":
                self.console.print("[yellow]再见！[/yellow]")
                break

    def show_menu(self):
        """
        显示主菜单
        """
        menu_text = """
[bold]主菜单:[/bold]
1. 添加图片文件
2. 移除图片文件
3. 设置输出路径
4. 配置合并参数
5. 查看当前配置
6. 执行图片合并
7. 重置配置
8. 帮助
0. 退出

当前状态:
- 已添加图片数量: [green]{file_count}[/green]
- 输出路径: [blue]{output_path}[/blue]
        """.format(
            file_count=len(self.files),
            output_path=self.output if self.output else "[red]未设置[/red]",
        )
        self.console.print(Panel(menu_text, title="菜单"))

    def add_files(self):
        """
        添加图片文件
        """
        while True:
            file_path = Prompt.ask("[bold]请输入图片文件路径 (回车完成添加):[/bold]")
            if not file_path:
                break

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

        self.console.print("\\n[bold]当前已添加的文件:[/bold]")
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
        self.output = Prompt.ask("[bold]请输入输出文件路径:[/bold]")
        self.console.print(f"[green]输出路径已设置为: {self.output}[/green]")

    def configure_settings(self):
        """
        配置合并参数
        """
        self.console.print("\\n[bold]配置合并参数:[/bold]")

        # 选择方向
        orientation_choice = Prompt.ask(
            "选择排列方向", choices=["horizontal", "vertical"], default=self.orientation
        )
        self.orientation = orientation_choice

        # 设置间距
        self.gap = IntPrompt.ask("设置图片间距 (像素)", default=self.gap)

        # 设置分隔线
        self.divider = Confirm.ask("是否添加分隔线?", default=self.divider)
        if self.divider:
            self.divider_thickness = IntPrompt.ask(
                "设置分隔线粗细 (像素)", default=self.divider_thickness
            )

            # 输入分隔线颜色 (R,G,B)
            color_input = Prompt.ask(
                "设置分隔线颜色 (R,G,B 格式，如 200,200,200)",
                default=f"{self.divider_color[0]},{self.divider_color[1]},{self.divider_color[2]}",
            )
            try:
                r, g, b = map(int, color_input.split(","))
                self.divider_color = (r, g, b)
            except ValueError:
                self.console.print("[red]颜色格式错误，使用默认值[/red]")

        # 设置背景颜色
        bg_color_input = Prompt.ask(
            "设置背景颜色 (R,G,B 格式，如 255,255,255)",
            default=f"{self.bg_color[0]},{self.bg_color[1]},{self.bg_color[2]}",
        )
        try:
            r, g, b = map(int, bg_color_input.split(","))
            self.bg_color = (r, g, b)
        except ValueError:
            self.console.print("[red]颜色格式错误，使用默认值[/red]")

        # 设置对齐方式
        self.align = Prompt.ask(
            "设置图片对齐方式", choices=["start", "center", "end"], default=self.align
        )

        # 统一高度/宽度
        if self.orientation == "horizontal":
            uniform_input = Prompt.ask(
                "是否设置统一高度? (输入数值或直接回车跳过)",
                default="" if self.uniform_height is None else str(self.uniform_height),
            )
            if uniform_input:
                try:
                    self.uniform_height = int(uniform_input)
                except ValueError:
                    self.console.print("[red]数值格式错误，跳过设置[/red]")
        else:
            uniform_input = Prompt.ask(
                "是否设置统一宽度? (输入数值或直接回车跳过)",
                default="" if self.uniform_width is None else str(self.uniform_width),
            )
            if uniform_input:
                try:
                    self.uniform_width = int(uniform_input)
                except ValueError:
                    self.console.print("[red]数值格式错误，跳过设置[/red]")

        # 设置边距
        self.margin = IntPrompt.ask("设置边距 (像素)", default=self.margin)

        self.console.print("[green]配置已更新[/green]")

    def show_current_config(self):
        """
        显示当前配置
        """
        table = Table(title="当前配置")
        table.add_column("参数", style="cyan")
        table.add_column("值", style="magenta")

        table.add_row("排列方向", self.orientation)
        table.add_row("图片间距", str(self.gap))
        table.add_row("添加分隔线", "是" if self.divider else "否")
        if self.divider:
            table.add_row("分隔线粗细", str(self.divider_thickness))
            table.add_row(
                "分隔线颜色",
                f"{self.divider_color[0]},{self.divider_color[1]},{self.divider_color[2]}",
            )
        table.add_row(
            "背景颜色", f"{self.bg_color[0]},{self.bg_color[1]},{self.bg_color[2]}"
        )
        table.add_row("对齐方式", self.align)
        if self.orientation == "horizontal" and self.uniform_height is not None:
            table.add_row("统一高度", str(self.uniform_height))
        elif self.orientation == "vertical" and self.uniform_width is not None:
            table.add_row("统一宽度", str(self.uniform_width))
        table.add_row("边距", str(self.margin))

        self.console.print(table)

        if self.files:
            self.console.print("\\n[bold]已添加的文件:[/bold]")
            for i, file in enumerate(self.files, 1):
                self.console.print(f"{i}. {file}")
        else:
            self.console.print("\\n[yellow]尚未添加任何文件[/yellow]")

        if self.output:
            self.console.print(f"\\n[bold]输出路径:[/bold] {self.output}")
        else:
            self.console.print("\\n[yellow]未设置输出路径[/yellow]")

    def process_images(self):
        """
        执行图片合并
        """
        if not self.files:
            self.console.print("[red]错误: 尚未添加任何图片文件[/red]")
            return

        if not self.output:
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

        # 确保输出目录存在
        output_dir = os.path.dirname(self.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 显示当前配置供用户确认
        self.console.print("\\n[bold]即将执行图片合并，当前配置:[/bold]")
        self.show_current_config()

        if not Confirm.ask("\\n确认执行合并操作?", default=True):
            self.console.print("[yellow]操作已取消[/yellow]")
            return

        try:
            result = merge_images(
                files=self.files,
                output=self.output,
                orientation=self.orientation,
                gap=self.gap,
                divider=self.divider,
                divider_thickness=self.divider_thickness,
                divider_color=self.divider_color,
                bg_color=self.bg_color,
                align=self.align,
                uniform_height=self.uniform_height
                if self.orientation == "horizontal"
                else None,
                uniform_width=self.uniform_width
                if self.orientation == "vertical"
                else None,
                margin=self.margin,
            )
            self.console.print(f"[green]图片合并完成: {result}[/green]")
        except Exception as e:
            self.console.print(f"[red]合并图片时出错: {str(e)}[/red]")

    def reset_config(self):
        """
        重置配置为默认值
        """
        if Confirm.ask("确认重置所有配置为默认值?", default=False):
            # 保留文件列表，只重置其他设置
            files_backup = self.files[:]
            self.__init__()
            self.files = files_backup
            self.console.print("[green]配置已重置为默认值[/green]")
        else:
            self.console.print("[yellow]操作已取消[/yellow]")

    def show_help(self):
        """
        显示帮助信息
        """
        help_text = """
[bold]帮助信息:[/bold]

本工具用于合并多张图片，支持以下功能：
- 水平或垂直排列图片
- 自定义间距和边距
- 添加分隔线
- 自定义背景色和分隔线颜色
- 设置图片对齐方式
- 统一图片高度或宽度

[bold]使用步骤:[/bold]
1. 添加至少两张图片文件
2. 设置输出文件路径
3. 配置合并参数（可选）
4. 执行图片合并

[bold]快捷键说明:[/bold]
- 在提示符下按 Ctrl+C 可随时退出程序
- 输入文件路径时直接回车可结束添加文件
        """
        self.console.print(Panel(help_text, title="帮助"))


def run_tui():
    """
    运行 TUI 界面的入口点
    """
    app = ImageProcessorTUI()
    app.run()


if __name__ == "__main__":
    run_tui()
