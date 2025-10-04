"""
菜单模块

该模块负责处理主菜单的显示和选择逻辑。
"""

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel


class MenuManager:
    """
    菜单管理类
    """

    def __init__(self, console: Console):
        self.console = console

    def show_menu(self, file_count: int, output_path: str) -> str:
        """
        显示主菜单并获取用户选择
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
            file_count=file_count,
            output_path=output_path if output_path else "[red]未设置[/red]",
        )
        self.console.print(Panel(menu_text, title="菜单"))

        choice = Prompt.ask(
            "[bold]请选择操作[/bold]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            default="1",
        )

        return choice

    def show_config_table(self, config) -> None:
        """
        显示当前配置表格
        """
        table = Table(title="当前配置")
        table.add_column("参数", style="cyan")
        table.add_column("值", style="magenta")

        table.add_row("排列方向", config.orientation)
        table.add_row("图片间距", str(config.gap))
        table.add_row("添加分隔线", "是" if config.divider else "否")
        if config.divider:
            table.add_row("分隔线粗细", str(config.divider_thickness))
            table.add_row(
                "分隔线颜色",
                f"{config.divider_color[0]},{config.divider_color[1]},{config.divider_color[2]}",
            )
        table.add_row(
            "背景颜色",
            f"{config.bg_color[0]},{config.bg_color[1]},{config.bg_color[2]}",
        )
        table.add_row("对齐方式", config.align)
        if config.orientation == "horizontal" and config.uniform_height is not None:
            table.add_row("统一高度", str(config.uniform_height))
        elif config.orientation == "vertical" and config.uniform_width is not None:
            table.add_row("统一宽度", str(config.uniform_width))

        # 添加网格布局信息
        if config.cols is not None:
            table.add_row("网格列数", str(config.cols))
        if config.rows is not None:
            table.add_row("网格行数", str(config.rows))

        table.add_row("边距", str(config.margin))
        table.add_row("添加时间戳", "是" if config.add_timestamp else "否")

        self.console.print(table)

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
