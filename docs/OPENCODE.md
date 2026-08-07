# Opencode 配置指南

## 安装

```bash
git clone https://github.com/ddjs0/deepseek-eyes-plus.git
cd deepseek-eyes-plus
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e .
```

## 获取视觉模型 API Key（默认 ModelScope）

默认平台 ModelScope：访问 https://modelscope.cn → 登录 → 个人中心 → 访问令牌 → 创建令牌（免费，每天500次；key 的 ms- 前缀自动去除）。其他平台（小米 mimo / 智谱 / OpenAI / Claude）的 key 获取方式见 docs/VISION_MODELS.md。

## 配置 Opencode

编辑 `%APPDATA%\opencode\opencode.json`：

```json
{
  "mcp": {
    "deepseek-eyes": {
      "type": "local",
      "command": ["C:\\path\\to\\deepseek-eyes-plus\\.venv\\Scripts\\python.exe", "-m", "deepseek_eyes"],
      "enabled": true,
      "environment": {
        "VISION_API_KEY": "your_key_here"
      }
    }
  }
}
```

> ⚠️ 使用 venv 中 Python 的绝对路径。

## 键盘快捷键

```json
{
  "keybinds": {
    "input_paste": "ctrl+v",
    "input_paste_image": "alt+v"
  }
}
```

## 测试

1. 重启 Opencode → 截图 (Win+Shift+S) → Alt+V 粘贴
2. 输入：`analyze_clipboard 这张图里有什么？`
3. DeepSeek 应该能描述图片内容

## 故障排查

- **工具不出现**：运行 `python -m deepseek_eyes` 确认无报错
- **临时文件**：`%TEMP%\deepseek_eyes\`，自动删除
