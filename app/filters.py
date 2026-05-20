"""Jinja2 自定义过滤器。"""
import markdown as md
import bleach

from app.utils.helpers import time_ago

ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "br", "hr", "strong", "em", "u", "s",
    "blockquote", "code", "pre", "img",
    "ul", "ol", "li", "a", "table", "thead", "tbody",
    "tr", "th", "td", "span", "div",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class"],
}


def markdown_to_html(text: str) -> str:
    if not text:
        return ""
    html = md.markdown(
        text,
        extensions=["fenced_code", "tables", "codehilite", "nl2br", "toc"],
    )
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)


def register_filters(app):
    app.jinja_env.filters["markdown"] = markdown_to_html
    app.jinja_env.filters["time_ago"] = time_ago
