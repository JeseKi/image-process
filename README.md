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