# AI Install Prompt (English)

Copy-paste this into any AI coding assistant (DeepSeek, GLM, Claude, GPT, Gemini, ...) and it will set up `deepseek-eyes` for you end-to-end.

---

```
Please help me install deepseek-eyes, an MCP server that adds vision
capabilities to text-only models (DeepSeek, GLM, etc.) by reading
clipboard/files and analyzing them with a vision model (image/audio/video).

Installation steps:

Prerequisite: **first read docs/VISION_MODELS.md in the repo** (common vision model reference + per-platform calling specs: model names / API base / key source / modality / auth / fees), and guide based on it — do not hardcode from memory.

0. **First ask me which vision model to use (use ask / multiple-choice, list common options and leave "Other"):**
   - Default (recommended, simplest): Qwen3-VL-8B — the ModelScope default row in docs/VISION_MODELS.md; the default model when VISION_MODEL is not set
   - Stronger: Qwen3-VL-235B-A22B-Instruct — ModelScope official, stronger, image-only
   - Full multimodal: mimo-v2.5 / mimo-v2.5-pro — Xiaomi MiMo (https://platform.xiaomimimo.com), image/audio/video
   - Other: let the user specify (any OpenAI-compatible vision API works, see docs/VISION_MODELS.md) — user provides model name and API Base; check the platform docs if needed, never guess
   Continue based on my choice; do not decide for me.

1. Clone the repo:
   git clone https://github.com/ddjs0/deepseek-eyes.git
   cd deepseek-eyes

2. Create venv and install:
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. Guide me to get the matching API Key (depends on which platform the model from step 0 belongs to):
   - ModelScope (Qwen3-VL family): Visit https://modelscope.cn → Login → Profile → Access Token → Create Token
     Copy the key (Qwen3-VL-8B free, 500 calls/day; key looks like ms-xxxxx, the ms- prefix is stripped automatically, paste as-is)
   - Xiaomi (mimo family): Visit https://platform.xiaomimimo.com → Login → Open Platform → API Key → Create
     Copy the key (check billing/credit requirements first)
   - Other platforms: guide per that platform's API key docs, check documentation if needed
   Before guiding me to get the key, **first ask me to confirm with ask: "我已了解相关模型的调用费用" ("I understand the calling fees for the chosen model")** — especially for paid platforms like mimo / GPT / Claude, which are pay-as-you-go; do not skip the fee notice.
   After I provide the key, **confirm it with ask** — never invent one.

4. Test clipboard:
   Copy an image to clipboard (Win+Shift+S to screenshot)
   Run: python examples/smoke_test.py
   Should see "✅ 成功" / "OK: clipboard image saved to..."

5. **First ask me which MCP client I'm using** (single/multi-select: Claude Code / Opencode / Codex CLI or ChatGPT Desktop / Cursor / Cline / Continue / Reasonix / Other), then configure for that client — do not default to Claude Code. env contents depend on step 0 (generic template below; fill the three vars per the chosen model/platform), command uses the venv Python absolute path.

   Generic env template (any OpenAI-compatible vision API):
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "ABSOLUTE_PATH\\to\\deepseek-eyes\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "VISION_API_KEY": "api_key_for_the_chosen_platform",
           "VISION_MODEL": "model_name_from_step_0",
           "VISION_API_BASE": "openai_compatible_api_base_of_the_chosen_platform"
         }
       }
     }
   }

   Reference values (full per-platform calling specs in docs/VISION_MODELS.md; not the only options):
   - Qwen3-VL-8B (default): VISION_MODEL and VISION_API_BASE can be omitted (defaults to Qwen/Qwen3-VL-8B-Instruct @ https://api-inference.modelscope.cn/v1); env only needs VISION_API_KEY
   - mimo-v2.5 / mimo-v2.5-pro: VISION_MODEL=mimo-v2.5 (or mimo-v2.5-pro), VISION_API_BASE=https://api.xiaomimimo.com/v1
   - Other: fill model name and API base per that platform's docs (see docs/VISION_MODELS.md); verify first, never guess

   Config locations per client (env = template above):
   - Claude Code: project `.claude/settings.json` → "mcpServers" (as templates above)
   - Opencode: `%APPDATA%\opencode\opencode.json` → "mcp" node
   - Codex CLI / ChatGPT Desktop: `~/.codex/config.toml` → [mcp_servers.deepseek-eyes]
   - Cursor / Cline / Continue: `.mcp.json` or the client's MCP Servers settings
   - Reasonix: config.toml `[[plugins]]`, env =
     env = { VISION_API_KEY = "…", VISION_MODEL = "…", VISION_API_BASE = "…" }
   - Other: write the same env into that client's MCP config

   Use the absolute path to the venv's Python!

6. Restart the client and test:
   Take a screenshot, copy it to clipboard
   Ask: "analyze_clipboard - what's in this image?"

7. **Setup complete.** Tell the user: "If you want to switch models, just say so" (e.g. change VISION_MODEL from mimo-v2.5 to mimo-v2.5-pro). Switching models only means editing VISION_MODEL in env (and VISION_API_BASE if needed) and restarting the client; switching between models accessible with the same key needs no new key.
```
