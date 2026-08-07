# AI 安装提示词 / AI Install Prompt

把下面的提示词直接粘贴给 Claude Code / DeepSeek / ChatGPT，让它帮你完成 deepseek-eyes 的安装和配置。

---

## 🇨🇳 中文（推荐）

```
请帮我安装 deepseek-eyes，这是一个为 DeepSeek 等无视觉能力的模型
提供图片/音频/视频理解能力的 MCP 服务器（剪贴板/文件媒体 → 视觉模型 → 文字描述）。

安装步骤：

0. **先问我选择视觉后端（用 ask / 多选工具，列出两个选项）：**
   - A) Qwen3-VL-8B —— ModelScope 官方（https://modelscope.cn），免费、仅图片、默认配置最简
   - B) mimo-v2.5 —— 小米 MiMo（https://platform.xiaomimimo.com），支持图片/音频/视频全模态
   根据我的选择继续，不要默认帮我决定。

1. 克隆仓库：
   git clone https://github.com/ddjs0/deepseek-eyes.git
   cd deepseek-eyes

2. 创建虚拟环境并安装：
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate # macOS/Linux
   pip install -e .

3. 引导我获取对应的 API Key（按第 0 步的选择）：
   - Qwen3-VL-8B：打开 https://modelscope.cn → 登录 → 右上角头像 → 个人中心 → 访问令牌 → 创建令牌
     复制生成的 API Key（免费，每天 500 次）
   - mimo-v2.5：打开 https://platform.xiaomimimo.com → 登录 → 开放平台 → API Key 管理 → 创建
     复制生成的 API Key（先告诉我是否需要充值/开通，以及计费方式）
   拿到 Key 后，**用 ask 让我确认填入**，不要自己编造。

4. 测试剪贴板是否正常：
   复制一张图片到剪贴板（可以按 Win+Shift+S 截图）
   运行 python examples/smoke_test.py
   应该看到 "✅ 成功" 的输出

5. 配置 Claude Code 的 MCP：
   在项目的 .claude/settings.json 中添加，env 按第 0 步的选择填：

   - 选了 Qwen3-VL-8B：
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "完整的deepseek-eyes目录路径\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "步骤3获取的ModelScope API Key"
         }
       }
     }
   }

   - 选了 mimo-v2.5（多三个环境变量）：
   {
     "mcpServers": {
       "deepseek-eyes": {
         "command": "完整的deepseek-eyes目录路径\\.venv\\Scripts\\python.exe",
         "args": ["-m", "deepseek_eyes"],
         "env": {
           "MODELSCOPE_API_KEY": "步骤3获取的小米API Key",
           "VISION_MODEL": "mimo-v2.5",
           "VISION_API_BASE": "https://api.xiaomimimo.com/v1"
         }
       }
     }
   }

   注意：command 必须使用 venv 中 Python 的绝对路径！
   如果你是 Reasonix/其他客户端，按对应客户端的 MCP 配置方式写入同样的 env。

6. 重启客户端，然后测试：
   按 Win+Shift+S 截图，Ctrl+C 复制
   在对话框中粘贴截图，然后输入："analyze_clipboard 看看这是什么"
```

---

## 🇬🇧 English

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

5. Configure Claude Code MCP in .claude/settings.json (env depends on step 0):

   - If Qwen3-VL-8B:
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

   - If mimo-v2.5 (three extra env vars):
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

   Use the absolute path to the venv's Python!
   For Reasonix/other clients, write the same env into that client's MCP config.

6. Restart the client and test:
   Take a screenshot, copy it to clipboard
   Ask: "analyze_clipboard - what's in this image?"
```
