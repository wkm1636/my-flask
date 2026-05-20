"""博客相关表单。"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField(
        "标题",
        validators=[DataRequired(message="标题不能为空"), Length(1, 200)],
        render_kw={"placeholder": "请输入文章标题"},
    )
    summary = TextAreaField(
        "摘要",
        validators=[Optional(), Length(0, 500)],
        render_kw={"placeholder": "可选，不填则自动从正文截取", "rows": 3},
    )
    category_id = SelectField("分类", coerce=int, validators=[Optional()])
    tags = StringField(
        "标签",
        validators=[Optional(), Length(0, 200)],
        render_kw={"placeholder": "多个标签用英文逗号分隔，如：Python,Flask,Web"},
    )
    cover = FileField(
        "封面图",
        validators=[
            FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "仅支持图片"),
        ],
    )
    content = TextAreaField(
        "正文",
        validators=[DataRequired(message="正文不能为空")],
        render_kw={"placeholder": "支持 Markdown 语法...", "rows": 20},
    )
    is_published = BooleanField("立即发布", default=True)
    submit = SubmitField("发 布")


class CommentForm(FlaskForm):
    content = TextAreaField(
        "评论内容",
        validators=[
            DataRequired(message="评论不能为空"),
            Length(1, 500, message="评论 1-500 字"),
        ],
        render_kw={"placeholder": "说点什么吧...", "rows": 3},
    )
    submit = SubmitField("发布评论")


class CategoryForm(FlaskForm):
    name = StringField(
        "分类名",
        validators=[DataRequired(message="分类名不能为空"), Length(1, 64)],
    )
    description = StringField(
        "描述", validators=[Optional(), Length(0, 255)]
    )
    submit = SubmitField("保 存")
