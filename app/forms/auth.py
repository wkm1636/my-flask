"""认证相关表单。"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    Regexp,
)

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "用户名 / 邮箱",
        validators=[DataRequired(message="请输入用户名或邮箱"), Length(1, 120)],
        render_kw={"placeholder": "请输入用户名或邮箱"},
    )
    password = PasswordField(
        "密码",
        validators=[DataRequired(message="请输入密码")],
        render_kw={"placeholder": "请输入密码"},
    )
    remember_me = BooleanField("记住我")
    submit = SubmitField("登 录")


class RegisterForm(FlaskForm):
    username = StringField(
        "用户名",
        validators=[
            DataRequired(message="用户名不能为空"),
            Length(3, 64, message="长度需在 3-64 位"),
            Regexp(
                r"^[A-Za-z0-9_\u4e00-\u9fa5]+$",
                message="只能包含中英文、数字、下划线",
            ),
        ],
        render_kw={"placeholder": "3-64 位，支持中英文/数字/下划线"},
    )
    email = StringField(
        "邮箱",
        validators=[
            DataRequired(message="邮箱不能为空"),
            Email(message="请输入合法邮箱"),
            Length(1, 120),
        ],
        render_kw={"placeholder": "请输入邮箱"},
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(message="请输入密码"),
            Length(6, 32, message="密码长度需 6-32 位"),
        ],
        render_kw={"placeholder": "6-32 位"},
    )
    password2 = PasswordField(
        "确认密码",
        validators=[
            DataRequired(message="请再次输入密码"),
            EqualTo("password", message="两次密码不一致"),
        ],
        render_kw={"placeholder": "请再次输入密码"},
    )
    submit = SubmitField("注 册")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("该用户名已被使用")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("该邮箱已被注册")


class ProfileForm(FlaskForm):
    bio = TextAreaField(
        "个人简介",
        validators=[Length(0, 255, message="不超过 255 字")],
        render_kw={"placeholder": "介绍一下自己吧~", "rows": 4},
    )
    submit = SubmitField("保存修改")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "原密码", validators=[DataRequired(message="请输入原密码")]
    )
    new_password = PasswordField(
        "新密码",
        validators=[
            DataRequired(message="请输入新密码"),
            Length(6, 32, message="长度需 6-32 位"),
        ],
    )
    confirm_password = PasswordField(
        "确认新密码",
        validators=[
            DataRequired(message="请再次输入新密码"),
            EqualTo("new_password", message="两次密码不一致"),
        ],
    )
    submit = SubmitField("修改密码")
