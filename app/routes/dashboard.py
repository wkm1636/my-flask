"""个人后台路由：文章管理、个人资料、分类管理。"""
from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, abort,
)
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db
from app.models import Post, Category, Tag, Comment
from app.forms import (
    PostForm, ProfileForm, ChangePasswordForm, CategoryForm,
)
from app.utils.helpers import save_upload, extract_summary, parse_tags

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    total_posts = Post.query.filter_by(user_id=current_user.id).count()
    total_views = (
        db.session.query(db.func.coalesce(db.func.sum(Post.views), 0))
        .filter_by(user_id=current_user.id)
        .scalar()
    )
    total_comments = (
        Comment.query.join(Post).filter(Post.user_id == current_user.id).count()
    )
    recent = (
        Post.query.filter_by(user_id=current_user.id)
        .order_by(desc(Post.created_at))
        .limit(5)
        .all()
    )
    return render_template(
        "dashboard/index.html",
        total_posts=total_posts,
        total_views=total_views or 0,
        total_comments=total_comments,
        recent=recent,
    )


@dashboard_bp.route("/posts")
@login_required
def post_list():
    page = request.args.get("page", 1, type=int)
    pagination = (
        Post.query.filter_by(user_id=current_user.id)
        .order_by(desc(Post.created_at))
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template("dashboard/post_list.html", pagination=pagination)


def _populate_form_choices(form: PostForm) -> None:
    form.category_id.choices = [(0, "-- 无分类 --")] + [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]


def _save_tags(post: Post, raw: str) -> None:
    names = parse_tags(raw)
    post.tags = []
    for name in names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        post.tags.append(tag)


@dashboard_bp.route("/posts/new", methods=["GET", "POST"])
@login_required
def post_create():
    form = PostForm()
    _populate_form_choices(form)

    if form.validate_on_submit():
        cover_path = save_upload(form.cover.data) if form.cover.data else None
        summary = form.summary.data or extract_summary(form.content.data)
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data,
            summary=summary,
            cover_image=cover_path,
            category_id=form.category_id.data or None,
            is_published=form.is_published.data,
            user_id=current_user.id,
        )
        db.session.add(post)
        db.session.flush()
        _save_tags(post, form.tags.data)
        db.session.commit()
        flash("文章已发布！", "success")
        return redirect(url_for("dashboard.post_list"))

    return render_template(
        "dashboard/post_edit.html", form=form, post=None, mode="新建"
    )


@dashboard_bp.route("/posts/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def post_edit(pid: int):
    post = Post.query.get_or_404(pid)
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    form = PostForm(obj=post)
    _populate_form_choices(form)

    if request.method == "GET":
        form.category_id.data = post.category_id or 0
        form.tags.data = ",".join(t.name for t in post.tags)
        form.is_published.data = post.is_published

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data
        post.summary = form.summary.data or extract_summary(form.content.data)
        post.category_id = form.category_id.data or None
        post.is_published = form.is_published.data
        if form.cover.data:
            cover_path = save_upload(form.cover.data)
            if cover_path:
                post.cover_image = cover_path
        _save_tags(post, form.tags.data)
        db.session.commit()
        flash("文章已更新", "success")
        return redirect(url_for("dashboard.post_list"))

    return render_template(
        "dashboard/post_edit.html", form=form, post=post, mode="编辑"
    )


@dashboard_bp.route("/posts/<int:pid>/delete", methods=["POST"])
@login_required
def post_delete(pid: int):
    post = Post.query.get_or_404(pid)
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("文章已删除", "info")
    return redirect(url_for("dashboard.post_list"))


@dashboard_bp.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data.strip()).first():
            flash("该分类已存在", "warning")
        else:
            cat = Category(
                name=form.name.data.strip(),
                description=form.description.data,
            )
            db.session.add(cat)
            db.session.commit()
            flash("分类已添加", "success")
            return redirect(url_for("dashboard.categories"))

    all_categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template(
        "dashboard/categories.html", form=form, categories=all_categories
    )


@dashboard_bp.route("/categories/<int:cid>/delete", methods=["POST"])
@login_required
def delete_category(cid: int):
    if not current_user.is_admin:
        abort(403)
    cat = Category.query.get_or_404(cid)
    db.session.delete(cat)
    db.session.commit()
    flash("分类已删除", "info")
    return redirect(url_for("dashboard.categories"))


@dashboard_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    pwd_form = ChangePasswordForm()
    if form.submit.data and form.validate_on_submit():
        current_user.bio = form.bio.data
        db.session.commit()
        flash("个人资料已更新", "success")
        return redirect(url_for("dashboard.profile"))
    return render_template(
        "dashboard/profile.html", form=form, pwd_form=pwd_form
    )


@dashboard_bp.route("/password", methods=["POST"])
@login_required
def change_password():
    pwd_form = ChangePasswordForm()
    if pwd_form.validate_on_submit():
        if not current_user.verify_password(pwd_form.old_password.data):
            flash("原密码不正确", "danger")
        else:
            current_user.password = pwd_form.new_password.data
            db.session.commit()
            flash("密码修改成功，请重新登录", "success")
            from flask_login import logout_user
            logout_user()
            return redirect(url_for("auth.login"))
    else:
        for errors in pwd_form.errors.values():
            for err in errors:
                flash(err, "danger")
    return redirect(url_for("dashboard.profile"))
