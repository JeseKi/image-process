# Image Process CLI

一个用于合并图片的命令行工具。

## 安装

推荐使用 pipx 安装：

```bash
pipx install .
```

或者使用 pip 安装：

```bash
pip install .
```

## 使用方法

### 查看帮助

```bash
image-process --help
```

### 设置默认运行模式

您可以设置默认运行模式（CLI 或 TUI）：

```bash
# 设置默认为 CLI 模式
image-process --config-mode cli

# 设置默认为 TUI 模式
image-process --config-mode tui
```

### 合并图片

```bash
image-process merge --files img1.jpg img2.jpg img3.jpg --output result.jpg
```

### 参数说明

- `-f, --files`: 要合并的图片文件列表
- `-o, --output`: 输出文件路径
- `--orientation`: 图片排列方向 (horizontal/vertical)，默认为 horizontal
- `--gap`: 图片间距 (像素)，默认为 40
- `--divider/--no-divider`: 是否添加分隔线，默认为 True
- `--divider-thickness`: 分隔线粗细 (像素)，默认为 4
- `--divider-color`: 分隔线颜色 (R,G,B)，默认为 (200, 200, 200)
- `--bg-color`: 背景颜色 (R,G,B)，默认为 (255, 255, 255)
- `--align`: 图片对齐方式 (start/center/end)，默认为 center
- `--uniform-height`: 统一高度 (仅在水平排列时有效)
- `--uniform-width`: 统一宽度 (仅在垂直排列时有效)
- `--margin`: 边距 (像素)，默认为 0

### 示例

```bash
# 水平排列合并图片，间距为 20 像素
image-process --files img1.jpg --files img2.jpg --output result.jpg --gap 20

# 垂直排列合并图片，不添加分隔线
image-process --files img1.jpg --files img2.jpg --output result.jpg --orientation vertical --no-divider

# 水平排列合并图片，自定义分隔线颜色和背景色
image-process --files img1.jpg --files img2.jpg --output result.jpg --divider-color 0 0 0 --bg-color 255 255 255
```

## 交互式 TUI 模式

除了命令行参数，本工具也提供了一个全功能的文本用户界面（TUI），让您可以在终端中以交互方式进行操作。

### 启动 TUI

您可以通过以下任一命令启动 TUI 模式：

```bash
image-process-tui
```

或者

```bash
image-process --mode tui
```

### 功能介绍

启动后，您会看到一个主菜单，包含以下选项：

- **1. 添加图片文件**: 打开一个交互式文件选择器。
  - 使用 `↑` 和 `↓` 箭头在文件列表中导航。
  - 按 `Enter` 键选中或取消选中一个文件。
  - 按 `Ctrl+X` 键确认选择并返回主菜单。
- **2. 移除图片文件**: 列出已添加的图片，并让您选择要移除的文件。
- **3. 设置输出路径**: 设置合并后图片的保存路径和文件名。
- **4. 配置合并参数**: 调整合并图片的各种参数，如排列方向、间距、分隔线、背景色等。
- **5. 查看当前配置**: 显示所有已添加的文件和当前的合并参数。
- **6. 执行图片合并**: 根据当前配置开始合并图片。
- **7. 重置配置**: 将所有合并参数恢复为默认值。
- **8. 帮助**: 显示帮助信息。
- **0. 退出**: 退出程序。

## 开发

### 安装依赖

使用 uv 安装依赖：

```bash
uv pip install -r requirements.txt
```

或者使用 pip：

```bash
pip install -r requirements.txt
```

### 代码格式化

使用 ruff 格式化代码：

```bash
ruff format .
```

### 代码检查

使用 ruff 检查代码：

```bash
ruff check .
```
