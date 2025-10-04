"""
配置管理模块

该模块负责管理图像处理工具的配置设置，包括加载、保存和默认值定义。
"""

import os
import json
from typing import Tuple, Optional
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "image-process-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"


class ConfigManager:
    """
    配置管理类
    """

    def __init__(self, load_saved_config=True):
        self.output: str = ""
        self.add_timestamp: bool = False
        self.orientation: str = "horizontal"
        self.gap: int = 40
        self.divider: bool = True
        self.divider_thickness: int = 4
        self.divider_color: Tuple[int, int, int] = (200, 200, 200)
        self.bg_color: Tuple[int, int, int] = (255, 255, 255)
        self.align: str = "center"
        self.uniform_height: Optional[int] = None
        self.uniform_width: Optional[int] = None
        self.margin: int = 0
        self.cols: Optional[int] = None
        self.rows: Optional[int] = None

        if load_saved_config:
            self.load_config()

    def load_config(self):
        """
        从文件加载配置
        """
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

                    # 加载配置值，保持默认值
                    self.output = config.get("output", self.output)
                    self.add_timestamp = config.get("add_timestamp", self.add_timestamp)
                    self.orientation = config.get("orientation", self.orientation)
                    self.gap = config.get("gap", self.gap)
                    self.divider = config.get("divider", self.divider)
                    self.divider_thickness = config.get(
                        "divider_thickness", self.divider_thickness
                    )
                    self.divider_color = tuple(
                        config.get("divider_color", self.divider_color)
                    )
                    self.bg_color = tuple(config.get("bg_color", self.bg_color))
                    self.align = config.get("align", self.align)
                    self.uniform_height = config.get(
                        "uniform_height", self.uniform_height
                    )
                    self.uniform_width = config.get("uniform_width", self.uniform_width)
                    self.margin = config.get("margin", self.margin)
                    self.cols = config.get("cols", self.cols)
                    self.rows = config.get("rows", self.rows)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # 如果文件不存在或解析失败，则使用默认配置

    def save_config(self):
        """
        保存配置到文件
        """
        # 读取现有配置以保留CLI相关设置
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r") as f:
                    existing_config = json.load(f)
            else:
                existing_config = {}
        except (FileNotFoundError, json.JSONDecodeError):
            existing_config = {}

        # 更新图像处理相关配置
        existing_config.update(
            {
                "output": self.output,
                "add_timestamp": self.add_timestamp,
                "orientation": self.orientation,
                "gap": self.gap,
                "divider": self.divider,
                "divider_thickness": self.divider_thickness,
                "divider_color": self.divider_color,
                "bg_color": self.bg_color,
                "align": self.align,
                "uniform_height": self.uniform_height,
                "uniform_width": self.uniform_width,
                "margin": self.margin,
                "cols": self.cols,
                "rows": self.rows,
            }
        )

        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(existing_config, f, indent=4)

    def reset_to_defaults(self):
        """
        重置配置为默认值
        """
        # 保存当前的输出和时间戳设置（这些是用户可能在命令行或界面中指定的）
        saved_output = self.output
        saved_add_timestamp = self.add_timestamp

        # 重置为默认值（不加载已保存的配置）
        self.__init__(load_saved_config=False)

        # 只恢复之前的输出和时间戳设置，其他都使用默认值
        self.output = saved_output
        self.add_timestamp = saved_add_timestamp
