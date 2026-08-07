# deepseek-eyes-plus 👁️

> Give DeepSeek the ability to see. Screenshot → clipboard → Qwen-VL → text → your text-only model can "see" images.

[中文 README](README.md) | [Install Prompt](docs/INSTALL_PROMPT_EN.md) | [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## Quick Start

```bash
git clone https://github.com/ddjs0/deepseek-eyes-plus.git
cd deepseek-eyes-plus
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -e .

# Get an API key for the vision model platform (default ModelScope, free, 500 calls/day):
# ① https://modelscope.cn → Register/Login
# ② Avatar → Profile → Access Token
#    or directly: https://modelscope.cn/my/myaccesstoken
# ③ First time: bind your Alibaba Cloud account (required)
# ④ "Create Access Token" → name it → generate → copy
# ⑤ Token format: ms-xxxxxxxxxxxx → the ms- prefix is stripped automatically, paste as-is
# Other platforms (Xiaomi MiMo / Zhipu / OpenAI / Claude): see docs/VISION_MODELS.md

## Why?

Text-only models like **DeepSeek V4** and **GLM 5.1** have no vision capability. Paste a screenshot and they can't see it.

**deepseek-eyes-plus** bridges this gap — an MCP server that reads your clipboard image, sends it to a vision model (default Qwen-VL via ModelScope, or any OpenAI-compatible endpoint), and returns a text description your LLM can reason about.

## How It Works

```
Claude Code / Opencode (DeepSeek API)
        │  MCP
        ▼
deepseek-eyes-plus (Python MCP Server)
        │
        ├── reads system clipboard (PIL)
        ├── encodes image as base64
        ├── sends to vision model via OpenAI-compatible API (default ModelScope)
        ├── returns text description
        └── deletes temp file
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `analyze_clipboard` | Analyze image in system clipboard |
| `extract_text_from_clipboard` | OCR text from clipboard image |
| `describe_ui_from_clipboard` | Describe UI layout from clipboard |
| `diagnose_error_from_clipboard` | Diagnose error screenshot from clipboard |
| `code_from_clipboard` | Extract code from clipboard screenshot |
| `analyze_image` | Analyze image file on disk |
| `extract_text` | OCR image file |
| `describe_ui` | Describe UI screenshot file |
| `diagnose_error` | Diagnose error screenshot file |
| `understand_diagram` | Interpret diagram/flowchart |
| `analyze_chart` | Analyze data chart |
| `code_from_screenshot` | Extract code from screenshot file |
| `analyze_audio` | Analyze audio file (speech transcription / sound description) |
| `analyze_video` | Analyze video file (visual + audio description) |

## Client Configuration

**Claude Code** (`.claude/settings.json`):

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "ABSOLUTE_PATH\\to\\deepseek-eyes-plus\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": { "VISION_API_KEY": "your_key" }
    }
  }
}
```

> 💡 Env vars (via the client's `env` block):
> - `VISION_API_KEY` (required): API key of the vision model platform. ModelScope's `ms-` prefix is stripped automatically; the old name `MODELSCOPE_API_KEY` still works.
> - `VISION_MODEL` (optional, default `Qwen/Qwen3-VL-8B-Instruct`), `VISION_API_BASE` (optional, default ModelScope; point it at any OpenAI-compatible endpoint, e.g. Xiaomi MiMo `https://api.xiaomimimo.com/v1` with `VISION_MODEL=mimo-v2.5` for audio/video understanding).
> - Full per-platform specs (Xiaomi MiMo / Zhipu / OpenAI / Claude): see [docs/VISION_MODELS.md](docs/VISION_MODELS.md)

**Codex CLI / ChatGPT Desktop** (`~/.codex/config.toml`):

```toml
[mcp_servers.deepseek-eyes]
command = 'C:\path\to\deepseek-eyes-plus\.venv\Scripts\python.exe'
args = ["-m", "deepseek_eyes"]
env = { "VISION_API_KEY" = "your_key" }
```

Or add it with one command: `codex mcp add deepseek-eyes --env VISION_API_KEY=your_key -- C:\path\to\deepseek-eyes-plus\.venv\Scripts\python.exe -m deepseek_eyes`

## Security

- Runs as local stdio process — no network ports exposed
- Clipboard temp files auto-deleted after analysis
- Media allowlist (image/audio/video) prevents arbitrary file reads
- Size limits: 20 MB images, 100 MB audio/video; magic-byte validation

## Credits

Forked from [Capetlevrai/clipboard-vision-mcp](https://github.com/Capetlevrai/clipboard-vision-mcp) (MIT). Vision backend: default Qwen-VL via ModelScope, switchable to any OpenAI-compatible vision API (see [docs/VISION_MODELS.md](docs/VISION_MODELS.md)). Full Chinese localization added.
👍

## License

MIT © Shaohan He
