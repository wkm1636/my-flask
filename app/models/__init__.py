"""数据库模型聚合导出。"""
from app.models.user import User
from app.models.post import Post, Category, Tag
from app.models.comment import Comment

__all__ = ["User", "Post", "Category", "Tag", "Comment"]
