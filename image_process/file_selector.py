"""
文件选择器模块

该模块提供了一个基于Textual的TUI界面，用于选择图片文件。
"""

import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, SelectionList
from textual.binding import Binding


class FileSelector(App):
    """一个用于选择文件的TUI应用。"""

    BINDINGS = [
        Binding("ctrl+x", "quit_and_return", "退出"),
    ]

    def compose(self) -> ComposeResult:
        """创建应用的子组件。"""
        yield Header(show_clock=True, name="选择图片文件")
        image_files = [
            f
            for f in os.listdir(".")
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]
        # 按修改时间排序（最新的在前）
        image_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        yield SelectionList[str](*[(f, f) for f in image_files])
        yield Footer()

    def on_mount(self) -> None:
        """应用挂载时的回调。"""
        self.query_one(SelectionList).focus()

    def action_quit_and_return(self) -> None:
        """退出应用并返回选中的文件。"""
        selected_files = self.query_one(SelectionList).selected
        self.exit(selected_files)
