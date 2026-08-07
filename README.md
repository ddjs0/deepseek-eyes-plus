# deepseek-eyes 👁️

<p align="center">
  <b>给 DeepSeek 装上眼睛（无需外网！）。</b><br>
  截图 → 剪贴板 → MCP → 通义千问VL → 文字描述 → DeepSeek 也能"看见"
</p>

<p align="center">
  <b><i>Give DeepSeek the ability to see.</i></b><br>
  <i>Screenshot → clipboard → Qwen-VL → text → your text-only model can "see"</i>
</p>

<p align="center">
  <a href="#-一键安装">🤖 一键安装</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-为什么需要">为什么需要</a> ·
  <a href="#-客户端配置">客户端配置</a> ·
  <a href="README_EN.md">English</a>
</p>

---

## 🇨🇳 中文

### 🤖 一键安装

把下面的提示词**直接粘贴**给 Claude Code / DeepSeek / ChatGPT，AI 会自动帮你完成克隆、安装、配置全流程：

> 请帮我安装 deepseek-eyes，仓库地址 [https://github.com/ddjs0/deepseek-eyes](https://github.com/ddjs0/deepseek-eyes) 。按 README 中的步骤：克隆 → 创建 venv → pip install -e . → **先读 docs/VISION_MODELS.md，再 ask 我选择视觉模型（默认 Qwen3-VL-8B / 可选 mimo-v2.5 等）**，按选择引导我获取对应的 API Key → 配置 MCP 客户端。

[📋 完整安装提示词（中英文）](docs/INSTALL_PROMPT_CN.md)

---

### ⚡ 手动安装 / 快速开始

```bash
# 1. 克隆
git clone https://github.com/ddjs0/deepseek-eyes.git
cd deepseek-eyes

# 2. 安装
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .

# 3. 获取视觉模型 API Key（默认 ModelScope 免费，每天500次）
# ① 打开 https://modelscope.cn 注册/登录
# ② 点右上角头像 → 个人中心 → 访问令牌
#    或直接访问: https://modelscope.cn/my/myaccesstoken
# ③ 首次使用会提示绑定阿里云账号（必须，按页面引导完成）
# ④ 点击"新建访问令牌" → 命名 → 生成 → 复制
# ⑤ 令牌格式为 ms-xxxxxxxxxxxx，ms- 前缀会自动去除，直接粘贴即可
# 其他平台（小米 mimo / 智谱 / OpenAI / Claude 等）的 key 获取方式见 docs/VISION_MODELS.md

# 4. 测试剪贴板（复制一张图片后运行）
python examples/smoke_test.py
# 预期: ✅ 成功: 剪贴板图片已保存到 ...\clip_xxx.png

# 5. 配置 MCP 客户端（见下方）
```

### 🎯 为什么需要？

DeepSeek V4 / GLM 等文本模型的 API **没有视觉能力** ——你粘贴一张截图，它只能告诉你"我看见了文件路径"。

**deepseek-eyes** 填补了这个缺口：

```
你截了一张图
        │
        ▼
  ┌─────────────────┐
  │ deepseek-eyes    │
  │ 读取剪贴板图片    │
  │ → 发给视觉模型     │
  │ → 返回文字描述   │
  └────────┬────────┘
           ▼
  DeepSeek: "这是一个登录页面，有用户名和密码两个输入框..."
```

**和同类工具的对比：**

| | deepseek-eyes | 原版 clipboard-vision-mcp | ErlichLiu/deepseek-vision |
|---|---|---|---|
| 视觉后端 | 通义千问VL（可换任意 OpenAI 兼容视觉 API） | Groq（需翻墙） | 自选 |
| 免费额度 | 500次/天 | Groq 免费层 | 取决于后端 |
| 语言 | 🇨🇳 中文优先 | 英文 | 🇨🇳 中文 |
| 方式 | MCP stdio | MCP stdio | HTTP 代理 |

### 🔧 工作原理

```
┌──────────────────┐   MCP    ┌──────────────────┐   HTTPS   ┌───────────────────┐
│  Claude Code /    │ ──────▶ │  deepseek-eyes   │ ────────▶│  视觉模型 API       │
│  Opencode         │         │  (Python)        │          │  默认 Qwen3-VL-8B   │
│  (DeepSeek API)   │         │                  │          │  (可换 mimo 等)     │
└──────────────────┘         └──────────────────┘          └───────────────────┘
                                    │
                                    ▼
                          读取系统剪贴板 (PIL)
                          → base64 → 发送 → 返回中文描述 → 删除临时文件
```

### 📋 MCP 工具列表

| 工具 | 功能 |
|------|------|
| `analyze_clipboard` | 分析剪贴板中的图片 |
| `extract_text_from_clipboard` | 剪贴板图片 OCR 提取文字 |
| `describe_ui_from_clipboard` | 分析剪贴板 UI 截图 |
| `diagnose_error_from_clipboard` | 诊断剪贴板错误截图 |
| `code_from_clipboard` | 从剪贴板代码截图提取代码 |
| `analyze_image` | 分析磁盘图片文件 |
| `extract_text` | 磁盘图片 OCR |
| `describe_ui` | 分析磁盘 UI 截图 |
| `diagnose_error` | 诊断磁盘错误截图 |
| `understand_diagram` | 解读流程图/架构图 |
| `analyze_chart` | 分析数据图表 |
| `code_from_screenshot` | 磁盘代码截图提取代码 |
| `analyze_audio` | 分析音频文件（语音转写/声音描述） |
| `analyze_video` | 分析视频文件（画面+声音描述） |

### 🔌 客户端配置

**Claude Code**（`.claude/settings.json`）：

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "C:\\path\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "VISION_API_KEY": "你的_API_Key"
      }
    }
  }
}
```

> ⚠️ `command` 必须使用 venv 中 Python 的**绝对路径**（Windows 用 `\path\to\deepseek-eyes\.venv\Scripts\python.exe`，macOS/Linux 用 `/path/to/deepseek-eyes/.venv/bin/python`）。
>
> 🔑 环境变量通过**客户端配置的 `env` 块**传入（`.env.example` 只是参考文档，程序不读取 `.env` 文件）。
>
> 💡 环境变量（通过客户端配置的 `env` 块传入，`.env.example` 只是参考文档，程序不读取 `.env` 文件）：
> - `VISION_API_KEY`（必填）：视觉模型平台的 API Key。ModelScope 的 `ms-` 前缀会自动去除；旧名 `MODELSCOPE_API_KEY` 仍兼容。
> - `VISION_MODEL`（可选，默认 `Qwen/Qwen3-VL-8B-Instruct`）、`VISION_API_BASE`（可选，默认 ModelScope；可指向任意 OpenAI 兼容端点，如小米 MiMo `https://api.xiaomimimo.com/v1` + `VISION_MODEL=mimo-v2.5` 获得音频/视频理解）
> - 常见平台（小米 mimo / 智谱 / OpenAI / Claude）的完整填法见 [docs/VISION_MODELS.md](docs/VISION_MODELS.md)

**Opencode**（`%APPDATA%\opencode\opencode.json`）：

```json
{
  "mcp": {
    "deepseek-eyes": {
      "type": "local",
      "command": ["C:\\path\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe", "-m", "deepseek_eyes"],
      "enabled": true,
      "environment": {
        "VISION_API_KEY": "你的_API_Key"
      }
    }
  }
}
```

**Codex CLI / ChatGPT 桌面版**（`~/.codex/config.toml`）：

```toml
[mcp_servers.deepseek-eyes]
command = 'C:\path\to\deepseek-eyes\.venv\Scripts\python.exe'
args = ["-m", "deepseek_eyes"]
env = { "VISION_API_KEY" = "你的_API_Key" }
```

或一行命令添加：`codex mcp add deepseek-eyes --env VISION_API_KEY=你的_API_Key -- C:\path\to\deepseek-eyes\.venv\Scripts\python.exe -m deepseek_eyes`

### ❓ 常见问题

见 [故障排查指南](docs/TROUBLESHOOTING.md)

### 🛡️ 安全

- 本地 stdio 进程运行，不开放任何网络端口
- 临时剪贴板文件分析完成后**自动删除**
- 仅接受媒体格式：图片（`.png .jpg .jpeg .gif .webp .bmp`）/ 音频（`.mp3 .flac .m4a .wav .ogg`）/ 视频（`.mp4 .wmv .mov .avi`），防止 LLM 注入后读取任意文件
- 文件大小限制：图片 20MB、音频/视频 100MB，魔数校验
- 媒体经 base64 编码发送至所选视觉模型 API（默认 ModelScope，可换其他平台），参阅对应平台隐私政策

### 🗺️ 路线图

- [ ] 支持 DashScope（阿里云官方）作为备用后端
- [ ] 多 API Key 轮询
- [x] 视频/音频理解（走全模态模型，如小米 MiMo mimo-v2.5，无需关键帧提取）

---

## 🇬🇧 English

See [README_EN.md](README_EN.md) for the full English version.

---

## 🙏 致谢

- 基于 [Capetlevrai/clipboard-vision-mcp](https://github.com/Capetlevrai/clipboard-vision-mcp) (MIT)
- 视觉模型：默认通义千问VL / Qwen-VL via [ModelScope](https://modelscope.cn)，可切换任意 OpenAI 兼容视觉 API（见 [docs/VISION_MODELS.md](docs/VISION_MODELS.md)）

## 📄 License

MIT © Shaohan He
