"""deepseek-eyes MCP Server — 给 DeepSeek 装上眼睛

通过任意 OpenAI 兼容视觉 API（默认 Qwen-VL via ModelScope）为无视觉能力的
文本模型提供图片理解能力。支持剪贴板直接读取和文件路径两种方式。

Tools: clipboard-first (analyze_clipboard, extract_text_from_clipboard, ...)
       file-path (analyze_image, extract_text, ...)
"""

from __future__ import annotations

import asyncio
import base64
import os
from pathlib import Path
from typing import Any

import aiofiles
from openai import AsyncOpenAI
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .clipboard import ClipboardError, save_clipboard_image

SERVER_NAME = "deepseek-eyes"
SERVER_VERSION = "1.1.0"

# OpenAI 兼容 API 配置（VISION_MODEL / VISION_API_BASE / VISION_API_KEY）
VISION_API_BASE = (
    os.environ.get("VISION_API_BASE")
    or os.environ.get("MODELSCOPE_BASE_URL")  # 旧名兼容
    or "https://api-inference.modelscope.cn/v1"
)
DEFAULT_MODEL = "Qwen/Qwen3-VL-8B-Instruct"
VISION_MODEL = os.environ.get("VISION_MODEL", DEFAULT_MODEL)


def _resolve_api_key() -> str | None:
    """读取 API Key：优先 VISION_API_KEY，兼容旧名 MODELSCOPE_API_KEY。

    ModelScope 的 key 以 ms- 开头；仅在走 ModelScope 端点（未自定义
    VISION_API_BASE，或 base 含 modelscope）时自动去除前缀，避免误伤
    其他平台的 key。
    """
    key = os.environ.get("VISION_API_KEY") or os.environ.get("MODELSCOPE_API_KEY")
    if key and key.startswith("ms-"):
        base = VISION_API_BASE or ""
        if not base or "modelscope" in base.lower():
            key = key[3:]
    return key

# 安全检查：图片 / 音频 / 视频 三类媒体
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
AUDIO_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg"}
VIDEO_EXTENSIONS = {".mp4", ".wmv", ".mov", ".avi"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | AUDIO_EXTENSIONS | VIDEO_EXTENSIONS
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_MEDIA_BYTES = 100 * 1024 * 1024
MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".wmv": "video/x-ms-wmv",
}
IMAGE_MAGIC_PREFIXES = (
    b"\x89PNG\r\n\x1a\n",
    b"\xff\xd8\xff",
    b"GIF87a",
    b"GIF89a",
    b"RIFF",
    b"BM",
)


def _media_kind(p: Path) -> str:
    """按扩展名判断媒体类别: image / audio / video。"""
    ext = p.suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    raise ValueError(f"不支持的媒体格式: {ext}")


def _validate_media_path(path_str: str) -> Path:
    """校验媒体路径，拒绝不支持的类型和超大文件。"""
    p = Path(path_str).resolve()
    if not p.is_file():
        raise ValueError(f"不是一个文件: {path_str}")
    kind = _media_kind(p)
    limit = MAX_IMAGE_BYTES if kind == "image" else MAX_MEDIA_BYTES
    size = p.stat().st_size
    if size > limit:
        raise ValueError(f"文件过大: {size} 字节 (最大 {limit})。")
    return p


def _validate_magic(kind: str, ext: str, data: bytes) -> None:
    """按媒体类别校验文件魔数。"""
    if kind == "image":
        if not any(data.startswith(m) for m in IMAGE_MAGIC_PREFIXES):
            raise ValueError("文件内容不像是支持的图片格式。")
        return
    if kind == "audio":
        ok = (
            (ext == ".wav" and data[:4] == b"RIFF" and data[8:12] == b"WAVE")
            or (ext == ".mp3" and (
                data.startswith(b"ID3")
                or data.startswith(b"\xff\xfb")
                or data.startswith(b"\xff\xf3")
            ))
            or (ext == ".flac" and data.startswith(b"fLaC"))
            or (ext == ".ogg" and data.startswith(b"OggS"))
            or (ext == ".m4a" and data[4:8] == b"ftyp")
        )
        if not ok:
            raise ValueError("文件内容不像是支持的音频格式。")
        return
    ok = (
        (ext in (".mp4", ".mov") and data[4:8] == b"ftyp")
        or (ext == ".avi" and data[:4] == b"RIFF" and data[8:12] == b"AVI")
        or (ext == ".wmv" and data.startswith(b"\x30\x26\xb2\x75\x8e\x66\xcf\x11"))
    )
    if not ok:
        raise ValueError("文件内容不像是支持的视频格式。")


server = Server(SERVER_NAME)


class VisionClient:
    """OpenAI 兼容视觉客户端 (AsyncOpenAI)"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=VISION_API_BASE)

    async def analyze(self, media_path: str, prompt: str) -> str:
        p = _validate_media_path(media_path)
        ext = p.suffix.lower()
        kind = _media_kind(p)
        async with aiofiles.open(p, "rb") as f:
            data = await f.read()
        _validate_magic(kind, ext, data)
        b64 = base64.b64encode(data).decode("utf-8")

        if kind == "image":
            media_part = {
                "type": "image_url",
                "image_url": {"url": f"data:{MIME_BY_EXT[ext]};base64,{b64}"},
            }
        elif kind == "audio":
            media_part = {
                "type": "input_audio",
                "input_audio": {"data": b64, "format": ext.lstrip(".")},
            }
        else:  # video
            media_part = {
                "type": "video_url",
                "video_url": {"url": f"data:{MIME_BY_EXT[ext]};base64,{b64}"},
            }

        response = await self.client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [media_part, {"type": "text", "text": prompt}],
                }
            ],
            temperature=0.3,
            # mimo-v2.5 等推理模型会把大量 token 花在 reasoning_content 上，
            # 2048 会被思考吃光导致 content 为空返回空字符串；8192 实测充足
            max_tokens=8192,
        )
        return response.choices[0].message.content or ""


vision_client: VisionClient | None = None


PROMPTS: dict[str, str] = {
    "analyze": "请详细描述这张图片的内容。包括所有相关元素、上下文，以及任何对看不到图片的人有用的信息。",
    "extract_text": "提取这张图片中的全部文字。只返回文字内容，保留排版和换行，不做任何评论。",
    "describe_ui": (
        "分析这张 UI 截图。描述：1) 整体布局 2) 组件（按钮、表单、导航、输入框）"
        "3) 可见文字和标签 4) 状态（错误提示、激活标签页、弹窗等）。"
    ),
    "diagnose_error": (
        "分析这张错误截图。返回：1) 精确的错误信息 2) 可能的原因 "
        "3) 具体的修复步骤 4) 如何避免再次发生。"
    ),
    "understand_diagram": (
        "解读这张图表。返回：1) 图表类型 2) 组成部分及其作用 "
        "3) 关系/流程 4) 整体目的。"
    ),
    "analyze_chart": (
        "分析这张数据图表。返回：1) 图表类型 2) 坐标轴和标签 "
        "3) 关键趋势 4) 值得注意的数据点 5) 洞察。"
    ),
    "code_from_screenshot": (
        "从这张截图中提取全部代码。返回：1) 编程语言 2) 格式化的代码块，保留缩进。"
    ),
    "analyze_audio": (
        "请分析这段音频：识别并转写其中的语音内容，描述背景声音、说话人语气等"
        "对听不到音频的人有用的信息。"
    ),
    "analyze_video": (
        "请分析这个视频：描述画面内容、场景变化、动作以及音频/语音内容，"
        "给出对看不到视频的人有用的关键信息。"
    ),
}


def _image_tool(name: str, zh: str, en: str) -> Tool:
    return Tool(
        name=name,
        description=f"{zh} / {en}",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "图片文件的绝对路径 / Absolute path to the image file.",
                }
            },
            "required": ["image_path"],
        },
    )


def _media_tool(name: str, zh: str, en: str) -> Tool:
    return Tool(
        name=name,
        description=f"{zh} / {en}",
        inputSchema={
            "type": "object",
            "properties": {
                "media_path": {
                    "type": "string",
                    "description": "音频/视频文件的绝对路径 / Absolute path to the audio/video file.",
                },
                "prompt": {"type": "string", "description": "自定义问题 / Custom question."},
            },
            "required": ["media_path"],
        },
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_clipboard",
            description=(
                "读取系统剪贴板中的图片并分析。当用户说'看看这个'、'剪贴板里有什么'、"
                "或粘贴截图时使用。可选参数 prompt 可自定义提问。"
                " / Analyze the image in system clipboard."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "自定义问题 / Custom question."}
                },
                "required": [],
            },
        ),
        Tool(
            name="extract_text_from_clipboard",
            description="从剪贴板图片中提取文字(OCR) / Extract text from clipboard image (OCR).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="describe_ui_from_clipboard",
            description="描述剪贴板中 UI 截图的布局、组件和状态 / Describe UI from clipboard screenshot.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="diagnose_error_from_clipboard",
            description="诊断剪贴板中错误截图的原因和修复方案 / Diagnose error screenshot from clipboard.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="code_from_clipboard",
            description="从剪贴板代码截图中提取可编辑的代码 / Extract code from clipboard screenshot.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="analyze_image",
            description="分析磁盘上的图片文件 / Analyze an image file on disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "图片路径"},
                    "prompt": {"type": "string", "description": "自定义问题"},
                },
                "required": ["image_path"],
            },
        ),
        _image_tool("extract_text", "从磁盘图片中提取文字(OCR)", "OCR an image file on disk"),
        _image_tool("describe_ui", "描述磁盘上 UI 截图文件", "Describe a UI screenshot file"),
        _image_tool("diagnose_error", "诊断磁盘上错误截图文件", "Diagnose an error screenshot file"),
        _image_tool("understand_diagram", "解读流程图/架构图等图表", "Interpret a diagram image file"),
        _image_tool("analyze_chart", "分析数据图表中的趋势和洞察", "Analyze a chart image file"),
        _image_tool("code_from_screenshot", "从磁盘代码截图提取代码", "Extract code from a screenshot file"),
        _media_tool("analyze_audio", "分析音频文件（语音转写/声音描述）", "Analyze an audio file"),
        _media_tool("analyze_video", "分析视频文件（画面+声音描述）", "Analyze a video file"),
    ]


async def _run(prompt_key: str, image_path: str, override: str | None = None) -> str:
    assert vision_client is not None
    prompt = override or PROMPTS[prompt_key]
    return await vision_client.analyze(image_path, prompt)


async def _run_clipboard(prompt_key: str, override: str | None = None) -> str:
    try:
        path = save_clipboard_image()
    except ClipboardError as e:
        return f"剪贴板错误: {e}"
    try:
        return await _run(prompt_key, path, override)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if vision_client is None:
        return [
            TextContent(
                type="text",
                text="❌ 未设置 VISION_API_KEY 环境变量（旧名 MODELSCOPE_API_KEY 仍兼容）。\n\n"
                "在 MCP 配置的 env 中设置视觉模型平台的 API Key：\n"
                "1. 默认 ModelScope（免费 500 次/天）：https://modelscope.cn/my/myaccesstoken\n"
                "2. 其他平台（小米 mimo / 智谱 / OpenAI / Claude 等）见 docs/VISION_MODELS.md\n"
                "3. ModelScope 的 ms- 前缀会自动去除，无需手动处理\n\n"
                "VISION_API_KEY not set. "
                "Set it in your MCP env (old name MODELSCOPE_API_KEY still works). "
                "See docs/VISION_MODELS.md for platform-specific keys.",
            )
        ]

    try:
        if name == "analyze_clipboard":
            text = await _run_clipboard("analyze", arguments.get("prompt"))
        elif name == "extract_text_from_clipboard":
            text = await _run_clipboard("extract_text")
        elif name == "describe_ui_from_clipboard":
            text = await _run_clipboard("describe_ui")
        elif name == "diagnose_error_from_clipboard":
            text = await _run_clipboard("diagnose_error")
        elif name == "code_from_clipboard":
            text = await _run_clipboard("code_from_screenshot")
        elif name == "analyze_image":
            text = await _run("analyze", arguments["image_path"], arguments.get("prompt"))
        elif name == "extract_text":
            text = await _run("extract_text", arguments["image_path"])
        elif name == "describe_ui":
            text = await _run("describe_ui", arguments["image_path"])
        elif name == "diagnose_error":
            text = await _run("diagnose_error", arguments["image_path"])
        elif name == "understand_diagram":
            text = await _run("understand_diagram", arguments["image_path"])
        elif name == "analyze_chart":
            text = await _run("analyze_chart", arguments["image_path"])
        elif name == "code_from_screenshot":
            text = await _run("code_from_screenshot", arguments["image_path"])
        elif name == "analyze_audio":
            text = await _run("analyze_audio", arguments["media_path"], arguments.get("prompt"))
        elif name == "analyze_video":
            text = await _run("analyze_video", arguments["media_path"], arguments.get("prompt"))
        else:
            text = f"未知工具: {name}"
        return [TextContent(type="text", text=text)]
    except Exception as e:
        return [TextContent(type="text", text=f"错误: {e}")]


async def main() -> None:
    global vision_client
    api_key = _resolve_api_key()
    if api_key:
        vision_client = VisionClient(api_key)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run() -> None:
    """入口: python -m deepseek_eyes"""
    asyncio.run(main())


if __name__ == "__main__":
    run()
