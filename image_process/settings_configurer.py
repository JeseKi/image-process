"""
设置配置模块

该模块负责处理图片合并参数的配置界面。
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt


class SettingsConfigurer:
    """
    设置配置类
    """

    def __init__(self, console: Console):
        self.console = console

    def configure_settings(self, config) -> None:
        """
        配置合并参数
        """
        self.console.print("\n[bold]配置合并参数:[/bold]")

        # 选择方向
        orientation_choice = Prompt.ask(
            "选择排列方向",
            choices=["horizontal", "vertical"],
            default=config.orientation,
        )
        config.orientation = orientation_choice

        # 设置间距
        config.gap = IntPrompt.ask("设置图片间距 (像素)", default=config.gap)

        # 设置分隔线
        config.divider = Confirm.ask("是否添加分隔线?", default=config.divider)
        if config.divider:
            config.divider_thickness = IntPrompt.ask(
                "设置分隔线粗细 (像素)", default=config.divider_thickness
            )

            # 输入分隔线颜色 (R,G,B)
            color_input = Prompt.ask(
                "设置分隔线颜色 (R,G,B 格式，如 200,200,200)",
                default=f"{config.divider_color[0]},{config.divider_color[1]},{config.divider_color[2]}",
            )
            try:
                r, g, b = map(int, color_input.split(","))
                config.divider_color = (r, g, b)
            except ValueError:
                self.console.print("[red]颜色格式错误，使用默认值[/red]")

        # 设置背景颜色
        bg_color_input = Prompt.ask(
            "设置背景颜色 (R,G,B 格式，如 255,255,255)",
            default=f"{config.bg_color[0]},{config.bg_color[1]},{config.bg_color[2]}",
        )
        try:
            r, g, b = map(int, bg_color_input.split(","))
            config.bg_color = (r, g, b)
        except ValueError:
            self.console.print("[red]颜色格式错误，使用默认值[/red]")

        # 设置对齐方式
        config.align = Prompt.ask(
            "设置图片对齐方式", choices=["start", "center", "end"], default=config.align
        )

        # 统一高度/宽度
        if config.orientation == "horizontal":
            uniform_input = Prompt.ask(
                "是否设置统一高度? (输入数值或直接回车跳过)",
                default=""
                if config.uniform_height is None
                else str(config.uniform_height),
            )
            if uniform_input:
                try:
                    config.uniform_height = int(uniform_input)
                except ValueError:
                    self.console.print("[red]数值格式错误，跳过设置[/red]")
        else:
            uniform_input = Prompt.ask(
                "是否设置统一宽度? (输入数值或直接回车跳过)",
                default=""
                if config.uniform_width is None
                else str(config.uniform_width),
            )
            if uniform_input:
                try:
                    config.uniform_width = int(uniform_input)
                except ValueError:
                    self.console.print("[red]数值格式错误，跳过设置[/red]")

        # 设置边距
        config.margin = IntPrompt.ask("设置边距 (像素)", default=config.margin)

        # 设置是否添加时间戳
        config.add_timestamp = Confirm.ask(
            "是否在输出文件名中添加时间戳?", default=config.add_timestamp
        )

        self.console.print("[green]配置已更新[/green]")
