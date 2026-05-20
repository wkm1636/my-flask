"""博客文章路由：详情、评论。"""
from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, abort,
)
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db
from app.models import Post, Comment, Category
from app.forms import CommentForm

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/<int:post_id>", methods=["GET", "POST"])
def detail(post_id: int):
    post = Post.query.get_or_404(post_id)
    if not post.is_published and (
        not current_user.is_authenticated or current_user.id != post.user_id
    ):
        abort(404)

    post.views = (post.views or 0) + 1
    db.session.commit()

    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("请先登录后再发表评论", "warning")
            return redirect(url_for("auth.login", next=request.url))
        comment = Comment(
            content=form.content.data.strip(),
            user_id=current_user.id,
            post_id=post.id,
        )
        db.session.add(comment)
        db.session.commit()
        flash("评论已发布", "success")
        return redirect(url_for("blog.detail", post_id=post.id) + "#comments")

    comments = (
        post.comments.order_by(desc(Comment.created_at)).all()
    )
    related = (
        Post.query.filter(
            Post.is_published == True,  # noqa: E712
            Post.id != post.id,
            Post.category_id == post.category_id,
        )
        .order_by(desc(Post.created_at))
        .limit(4)
        .all()
    )
    return render_template(
        "blog/detail.html",
        post=post,
        form=form,
        comments=comments,
        related=related,
    )


@blog_bp.route("/comment/<int:cid>/delete", methods=["POST"])
@login_required
def delete_comment(cid: int):
    comment = Comment.query.get_or_404(cid)
    if comment.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash("评论已删除", "info")
    return redirect(url_for("blog.detail", post_id=post_id) + "#comments")


@blog_bp.route("/category/<int:cid>")
def category(cid: int):
    cat = Category.query.get_or_404(cid)
    page = request.args.get("page", 1, type=int)
    pagination = (
        Post.query.filter_by(category_id=cid, is_published=True)
        .order_by(desc(Post.created_at))
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template(
        "blog/category.html", category=cat, pagination=pagination
    )
