# MCP 客户端配置 / MCP Client Configuration

## Claude Code

在 `.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "C:\\path\\to\\deepseek-eyes-plus\\.venv\\Scripts\\python.exe",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "VISION_API_KEY": "your_key_here"
      }
    }
  }
}
```

> ⚠️ `command` 必须使用 venv 中 Python 的**绝对路径**。

## Cursor

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "python",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "VISION_API_KEY": "your_key_here"
      }
    }
  }
}
```

## Cline / Continue

```json
{
  "mcpServers": {
    "deepseek-eyes": {
      "command": "python",
      "args": ["-m", "deepseek_eyes"],
      "env": {
        "VISION_API_KEY": "your_key_here"
      }
    }
  }
}
```

## Codex CLI / ChatGPT 桌面版

Codex 把 MCP 配置放在 `~/.codex/config.toml`（也可用项目级 `.codex/config.toml`，仅受信任项目生效），添加到 `[mcp_servers]`：

```toml
[mcp_servers.deepseek-eyes]
command = 'C:\path\to\deepseek-eyes-plus\.venv\Scripts\python.exe'
args = ["-m", "deepseek_eyes"]
env = { "VISION_API_KEY" = "your_key_here" }
```

或用 CLI 命令快速添加（效果相同）：

```bash
codex mcp add deepseek-eyes --env VISION_API_KEY=your_key_here -- C:\path\to\deepseek-eyes-plus\.venv\Scripts\python.exe -m deepseek_eyes
```

> 💡 可选：
> - 用 `VISION_MODEL` / `VISION_API_BASE` 切换模型（如小米 MiMo `mimo-v2.5` 全模态，见 `.env.example`）
> - 剪贴板/文件读取属敏感操作，可设 `default_tools_approval_mode = "prompt"` 让每次调用前请求确认
> - 桌面版/IDE 扩展与 CLI 共享这份配置，改完在设置里 Restart 生效

## 手动验证

```bash
python -m deepseek_eyes
# 应该静默等待输入，Ctrl+C 退出
```
