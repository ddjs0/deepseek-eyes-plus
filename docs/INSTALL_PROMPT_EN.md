# AI Install Prompt (English)

Copy-paste this into any AI coding assistant (DeepSeek, GLM, Claude, GPT, Gemini, ...) and it will set up `deepseek-eyes` for you end-to-end.

---

```
Please help me install deepseek-eyes, an MCP server that adds vision
capabilities to text-only models (DeepSeek, GLM, etc.) by reading
clipboard/files and analyzing them with a vision model (image/audio/video).

Installation steps:

0. **First ask me which vision backend to use (use ask / multiple-choice):**
   - A) Qwen3-VL-8B — ModelScope official (https://modelscope.cn), free, image-only, simplest config
   - B) mimo-v2.5 — Xiaomi MiMo (https://platform.xiaomimimo.com), full multimodal: image/audio/video
   Continue based on my choice; do not decide for me.

1. Clone the repo:
   git clone https://github.com/ddjs0/deepseek-eyes.git
   cd deepseek-eyes

2. Create venv and install:
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. Guide me to get the matching API Key (per step 0):
   - Qwen3-VL-8B: Visit https://modelscope.cn → Login → Profile → Access Token → Create Token
     Copy the key (free, 500 calls/day)
   - mimo-v2.5: Visit https://platform.xiaomimimo.com → Login → Open Platform → API Key → Create
     Copy the key (check billing/credit requirements first)
   After I provide the key, **confirm it with ask** — never invent one.

4. Test clipboard:
   Copy an image to clipboard (Win+Shift+S to screenshot)
   Run: python examples/smoke_test.py
   Should see "✅ 成功" / "OK: clipboard image saved to..."

5. **First ask me which MCP client I'm using** (single/multi-select: Claude Code / Opencode / Codex CLI or ChatGPT Desktop / Cursor / Cline / Continue / Reasonix / Other), then configure for that client — do not default to Claude Code. env contents depend on step 0 (two templates below), command uses the venv Python absolute path.

   - If Qwen3-VL-8B (env template):
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "ABSOLUTE_PATH\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "modelscope_api_key_from_step_3"
         }
       }
     }
   }

   - If mimo-v2.5 (env template, three extra env vars):
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "ABSOLUTE_PATH\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "xiaomi_api_key_from_step_3",
           "VISION_MODEL": "mimo-v2.5",
           "VISION_API_BASE": "https://api.xiaomimimo.com/v1"
         }
       }
     }
   }

   Config locations per client (env = template above):
   - Claude Code: project `.claude/settings.json` → "mcpServers" (as templates above)
   - Opencode: `%APPDATA%\opencode\opencode.json` → "mcp" node
   - Codex CLI / ChatGPT Desktop: `~/.codex/config.toml` → [mcp_servers.deepseek-eyes]
   - Cursor / Cline / Continue: `.mcp.json` or the client's MCP Servers settings
   - Reasonix: config.toml `[[plugins]]`, env =
     env = { MODELSCOPE_API_KEY = "…", VISION_MODEL = "…", VISION_API_BASE = "…" }
   - Other: write the same env into that client's MCP config

   Use the absolute path to the venv's Python!

6. Restart the client and test:
   Take a screenshot, copy it to clipboard
   Ask: "analyze_clipboard - what's in this image?"
```
