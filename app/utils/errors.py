"""统一错误处理。"""
from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(_):
        return render_template("errors/error.html", code=403, msg="无权访问"), 403

    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/error.html", code=404, msg="页面不存在"), 404

    @app.errorhandler(500)
    def server_error(_):
        return render_template("errors/error.html", code=500, msg="服务器内部错误"), 500
