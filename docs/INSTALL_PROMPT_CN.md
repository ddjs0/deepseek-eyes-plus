# AI 安装提示词 / AI Install Prompt

把下面的提示词直接粘贴给 Claude Code / DeepSeek / ChatGPT，让它帮你完成 deepseek-eyes 的安装和配置。

---

## 🇨🇳 中文（推荐）

```
请帮我安装 deepseek-eyes，这是一个为 DeepSeek 等无视觉能力的模型
提供图片/音频/视频理解能力的 MCP 服务器（剪贴板/文件媒体 → 视觉模型 → 文字描述）。

安装步骤：

前置：**先读仓库里的 docs/VISION_MODELS.md**（常见视觉模型参考表 + 各平台调用规范：模型名 / API Base / Key 获取 / 模态 / 鉴权 / 费用），据此引导选择，不要凭记忆写死。

0. **先问我选择哪个视觉模型（用 ask / 多选工具，列出常见选项并留“其他”）：**
   - 默认（推荐，最简）：Qwen3-VL-8B —— 即 docs/VISION_MODELS.md 中的 ModelScope 默认行；不填 VISION_MODEL 时的默认模型
   - 更强：Qwen3-VL-235B-A22B-Instruct —— ModelScope 官方，更强、仅图片
   - 全模态：mimo-v2.5 / mimo-v2.5-pro —— 小米 MiMo（https://platform.xiaomimimo.com），图片/音频/视频
   - 其他：让用户自己说（任意 OpenAI 兼容视觉 API 都可以，参考 docs/VISION_MODELS.md），用户提供模型名和 API Base；必要时查询对应平台文档确认，不要猜
   根据我的选择继续，不要默认帮我决定。

1. 克隆仓库：
   git clone https://github.com/ddjs0/deepseek-eyes.git
   cd deepseek-eyes

2. 创建虚拟环境并安装：
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. 引导我获取对应的 API Key（取决于第 0 步所选模型属于哪个平台）：
   - ModelScope（Qwen3-VL 系列）：打开 https://modelscope.cn → 登录 → 右上角头像 → 个人中心 → 访问令牌 → 创建令牌
     复制生成的 API Key（Qwen3-VL-8B 免费，每天 500 次；key 形如 ms-xxxxx，ms- 前缀会自动去除，直接粘贴）
   - 小米（mimo 系列）：打开 https://platform.xiaomimimo.com → 登录 → 开放平台 → API Key 管理 → 创建
     复制生成的 API Key（先告诉我是否需要充值/开通，以及计费方式）
   - 其他平台：按该平台的 API Key 获取方式引导，必要时查询文档确认
   引导获取 Key 前，**先用 ask 让我确认：“我已了解相关模型的调用费用”**（尤其非免费平台如 mimo / GPT / Claude，按量计费）；不要跳过费用提示。
   拿到 Key 后，**用 ask 让我确认填入**，不要自己编造。

4. 测试剪贴板是否正常：
   复制一张图片到剪贴板（可以按 Win+Shift+S 截图）
   运行 python examples/smoke_test.py
   应该看到 "✅ 成功" 的输出

5. **先 ask 我用的哪个 MCP 客户端**（多选/单选，列出常见选项：Claude Code / Opencode / Codex CLI 或 ChatGPT 桌面版 / Cursor / Cline / Continue / Reasonix / 其他），按对应客户端配置，不要默认 Claude Code。env 内容按第 0 步的选择填（通用模板见下，三个变量按所选模型/平台填），command 用 venv 中 Python 的绝对路径。

   env 通用模板（任意 OpenAI 兼容视觉 API）：
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "完整的deepseek-eyes目录路径\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "VISION_API_KEY": "所选模型平台的API Key",
           "VISION_MODEL": "第0步选的模型名",
           "VISION_API_BASE": "所选平台的 OpenAI 兼容 API 地址"
         }
       }
     }
   }

   参考值（常见平台完整调用规范见 docs/VISION_MODELS.md，不是唯一选择）：
   - Qwen3-VL-8B（默认）：VISION_MODEL 和 VISION_API_BASE 都可省略（默认 Qwen/Qwen3-VL-8B-Instruct @ https://api-inference.modelscope.cn/v1），env 只需 VISION_API_KEY
   - mimo-v2.5 / mimo-v2.5-pro：VISION_MODEL=mimo-v2.5（或 mimo-v2.5-pro），VISION_API_BASE=https://api.xiaomimimo.com/v1
   - 其他：按该平台文档填模型名和 API 地址（参考 docs/VISION_MODELS.md），必要时先查询验证，不要猜

   各客户端配置位置（env 都填上面模板的内容）：
   - Claude Code：项目 `.claude/settings.json` 的 "mcpServers"（如上模板）
   - Opencode：`%APPDATA%\opencode\opencode.json` 的 "mcp" 节点
   - Codex CLI / ChatGPT 桌面版：`~/.codex/config.toml` 的 [mcp_servers.deepseek-eyes]
   - Cursor / Cline / Continue：`.mcp.json` 或客户端设置里的 MCP Servers
   - Reasonix：config.toml 的 [[plugins]]，env 写成
     env = { VISION_API_KEY = "…", VISION_MODEL = "…", VISION_API_BASE = "…" }
   - 其他：按该客户端的 MCP 配置方式写入同样的 env

   注意：command 必须使用 venv 中 Python 的绝对路径！

6. 重启客户端，然后测试：
   按 Win+Shift+S 截图，Ctrl+C 复制
   在对话框中粘贴截图，然后输入："analyze_clipboard 看看这是什么"

7. **配置完成。** 告诉用户："如果想要换模型，可以直接说"（例如把 VISION_MODEL 从 mimo-v2.5 换成 mimo-v2.5-pro）。换模型只需改 env 里的 VISION_MODEL（必要时连带 VISION_API_BASE）并重启客户端；同一个 key 能访问的模型之间切换无需重新申请 key。
```

---

## 🇬🇧 English

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
