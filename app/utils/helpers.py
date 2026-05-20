"""工具函数：图片上传、文本处理等。"""
import os
import re
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage) -> str | None:
    """保存上传的图片，返回相对静态路径。"""
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        return None

    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    new_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_name)
    file_storage.save(save_path)
    return f"uploads/{new_name}"


def extract_summary(content: str, length: int = 150) -> str:
    """从 Markdown 正文提取纯文本摘要。"""
    text = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"[#*`>\-_~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:length] + ("..." if len(text) > length else "")


def parse_tags(raw: str) -> list[str]:
    """将逗号分隔的标签字符串解析为列表。"""
    if not raw:
        return []
    items = [t.strip() for t in re.split(r"[,，]", raw) if t.strip()]
    return list(dict.fromkeys(items))[:10]


def time_ago(dt: datetime) -> str:
    """友好的相对时间显示。"""
    if not dt:
        return ""
    delta = datetime.utcnow() - dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return "刚刚"
    if seconds < 3600:
        return f"{int(seconds // 60)} 分钟前"
    if seconds < 86400:
        return f"{int(seconds // 3600)} 小时前"
    if seconds < 86400 * 30:
        return f"{int(seconds // 86400)} 天前"
    return dt.strftime("%Y-%m-%d")
