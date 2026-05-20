"""主路由：首页、关于、分类列表等。"""
from flask import Blueprint, render_template, request
from sqlalchemy import desc, func

from app import db
from app.models import Post, Category, Tag, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    category_id = request.args.get("category", type=int)
    keyword = request.args.get("q", "", type=str).strip()
    tag_id = request.args.get("tag", type=int)

    query = Post.query.filter_by(is_published=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            db.or_(Post.title.like(like), Post.summary.like(like))
        )
    if tag_id:
        query = query.filter(Post.tags.any(Tag.id == tag_id))

    pagination = query.order_by(desc(Post.created_at)).paginate(
        page=page, per_page=6, error_out=False
    )

    categories = Category.query.all()
    hot_posts = (
        Post.query.filter_by(is_published=True)
        .order_by(desc(Post.views))
        .limit(5)
        .all()
    )
    tags = Tag.query.limit(20).all()
    stats = {
        "post_count": Post.query.filter_by(is_published=True).count(),
        "user_count": User.query.count(),
        "category_count": Category.query.count(),
    }

    return render_template(
        "index.html",
        pagination=pagination,
        posts=pagination.items,
        categories=categories,
        hot_posts=hot_posts,
        tags=tags,
        stats=stats,
        current_category=category_id,
        current_tag=tag_id,
        keyword=keyword,
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")
