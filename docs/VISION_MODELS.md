# 常见视觉模型参考 / Common Vision Model Reference

> deepseek-eyes-plus 通过 **OpenAI 兼容接口**（`openai` SDK 的 `AsyncOpenAI` + `chat.completions.create`）调用视觉模型。
> 接入任何平台只需在 MCP 客户端 env 里配三个变量：
>
> - `VISION_API_KEY`：所选平台的 API Key（旧名 `MODELSCOPE_API_KEY` 仍兼容，`VISION_API_KEY` 优先）
> - `VISION_MODEL`：模型名（不填时默认 `Qwen/Qwen3-VL-8B-Instruct`）
> - `VISION_API_BASE`：该平台的 OpenAI 兼容 API 地址（不填时默认 `https://api-inference.modelscope.cn/v1`）
>
> 本文件是安装/换模型时的参考，具体模型名、价格、限制以各平台官方文档为准。

## 速查表

| 平台 | VISION_MODEL（模型名） | VISION_API_BASE | 模态 | 说明 |
|---|---|---|---|---|
| ModelScope（默认） | `Qwen/Qwen3-VL-8B-Instruct` | `https://api-inference.modelscope.cn/v1` | 图片 | 免费 500 次/天；可不填（代码默认值） |
| ModelScope | `Qwen/Qwen3-VL-235B-A22B-Instruct` | `https://api-inference.modelscope.cn/v1` | 图片 | 更强 |
| 小米 MiMo | `mimo-v2.5` / `mimo-v2.5-pro` | `https://api.xiaomimimo.com/v1` | 图片/音频/视频 | 按量计费，需充值 |
| 智谱 GLM | `glm-4.6v-flash` | `https://open.bigmodel.cn/api/paas/v4` | 图片 | 智谱开放平台 |
| 硅基流动 | `OpenBMB/MiniCPM-V-2.6` | `https://api.siliconflow.cn/v1` | 图片 | 聚合平台 |
| OpenAI | `gpt-4o` / `gpt-4o-mini` 等 | `https://api.openai.com/v1` | 图片 | 海外，需代理 |
| Anthropic Claude | `claude-sonnet-4` 等 Claude 模型 ID | `https://api.anthropic.com/v1/` | 图片 | 海外，需代理；官方 OpenAI 兼容端点 |

## 各平台调用规范

### 1. ModelScope（通义千问 Qwen3-VL）— 默认

- **Key 获取**：https://modelscope.cn → 登录 → 右上角头像 → 个人中心 → 访问令牌 → 创建令牌；key 形如 `ms-xxxxx`，**`ms-` 前缀由代码自动去除**，直接粘贴即可。
- **env 填法**：不填 `VISION_MODEL` / `VISION_API_BASE` 即用默认；env 里 `VISION_API_KEY` 填 ModelScope key 即可（`MODELSCOPE_API_KEY` 旧名也可）。
- **模态**：图片（`image_url`）。
- **费用**：Qwen3-VL-8B 免费 500 次/天；235B 按量计费，以官网为准。
- **注意**：免费额度按模型分别计数。

### 2. 小米 MiMo — 全模态

- **Key 获取**：https://platform.xiaomimimo.com → 登录 → 开放平台 → API Key 管理 → 创建（需开通/充值，计费方式见平台）。
- **env 填法**：
  ```toml
  VISION_API_KEY = "小米 API Key"
  VISION_MODEL = "mimo-v2.5"        # 或 mimo-v2.5-pro
  VISION_API_BASE = "https://api.xiaomimimo.com/v1"
  ```
- **模态**：图片 / 音频 / 视频（全模态，deepseek-eyes-plus 的音频、视频工具用它才能跑通）。
- **费用**：按量计费（mimo-v2.5 约 ¥1/百万输入 token 量级，具体以平台为准）。
- **注意**：音频格式限 `mp3/flac/m4a/wav/ogg`，视频格式限 `mp4/wmv/mov/avi`（平台错误信息里给出的支持列表）。

### 3. 智谱 GLM

- **Key 获取**：https://open.bigmodel.cn → 开放平台 → API Keys。
- **env 填法**：
  ```toml
  VISION_API_KEY = "智谱 API Key"
  VISION_MODEL = "glm-4.6v-flash"
  VISION_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
  ```
- **模态**：图片。
- **费用**：以智谱开放平台计费为准。

### 4. 硅基流动 SiliconFlow

- **Key 获取**：https://cloud.siliconflow.cn → API 密钥。
- **env 填法**：
  ```toml
  VISION_API_KEY = "硅基流动 API Key"
  VISION_MODEL = "OpenBMB/MiniCPM-V-2.6"
  VISION_API_BASE = "https://api.siliconflow.cn/v1"
  ```
- **模态**：图片。
- **费用**：以平台计费为准。

### 5. OpenAI（GPT-4o 系列）

- **Key 获取**：https://platform.openai.com → API Keys（海外账号，需代理）。
- **env 填法**：
  ```toml
  VISION_API_KEY = "OpenAI API Key"
  VISION_MODEL = "gpt-4o"           # 或 gpt-4o-mini 等
  VISION_API_BASE = "https://api.openai.com/v1"
  ```
- **模态**：图片（`image_url`；`input_audio` 原生支持但未实测，`video_url` 不支持）。
- **费用**：按量计费，以平台为准。

### 6. Anthropic Claude

- **Key 获取**：https://console.anthropic.com → API Keys（海外账号，需代理）。
- **env 填法**（走官方 OpenAI 兼容端点，非原生 Messages API）：
  ```toml
  VISION_API_KEY = "Anthropic API Key"
  VISION_MODEL = "claude-sonnet-4"  # 任意 Claude 模型 ID（如 claude-opus-5）
  VISION_API_BASE = "https://api.anthropic.com/v1/"
  ```
- **模态**：**仅图片**。官方 OpenAI 兼容层明确不支持音频输入（会被忽略），`video_url` 也不在支持列表。
- **鉴权**：直接把 Anthropic API Key 当 api_key 传（SDK 自动带 `Authorization: Bearer`），不需要 `x-api-key` 头。
- **费用**：按量计费，以平台为准。
- **注意**：Anthropic 官方说明该兼容层主要用于测试/对比模型能力，非长期生产方案；deepseek-eyes-plus 的音频/视频工具切到 Claude 后不可用。

## 其他平台

任意 **OpenAI 兼容的视觉 API** 都可以接入：用户提供平台、模型名、API Base、API Key 四个信息即可，按上面同样的 env 填法配置。拿不准模型名或 base_url 时查询该平台文档确认，不要猜。
