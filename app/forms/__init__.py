"""表单模块。"""
from app.forms.auth import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
from app.forms.blog import PostForm, CommentForm, CategoryForm

__all__ = [
    "LoginForm",
    "RegisterForm",
    "ProfileForm",
    "ChangePasswordForm",
    "PostForm",
    "CommentForm",
    "CategoryForm",
]
