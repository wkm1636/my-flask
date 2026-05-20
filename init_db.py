"""数据库初始化脚本：创建表并插入示例数据。

用法：
    python init_db.py        # 仅创建表
    python init_db.py --seed # 创建表并插入示例数据
"""
import sys
from app import create_app, db
from app.models import User, Post, Category, Tag


def init():
    app = create_app("development")
    with app.app_context():
        db.create_all()
        print("[OK] 数据库表已创建")

        if "--seed" in sys.argv:
            seed_data()


def seed_data():
    if User.query.first():
        print("[SKIP] 数据库已有数据，跳过示例数据插入")
        return

    admin = User(username="admin", email="admin@example.com", is_admin=True,
                 bio="本站管理员")
    admin.password = "admin123"
    db.session.add(admin)
    db.session.flush()

    cats = [
        Category(name="技术分享", description="编程、开发、架构相关"),
        Category(name="生活随笔", description="日常生活与思考"),
        Category(name="读书笔记", description="读书心得与笔记"),
        Category(name="项目实战", description="项目开发实战记录"),
    ]
    db.session.add_all(cats)
    db.session.flush()

    tags = [Tag(name=n) for n in ["Python", "Flask", "MySQL", "Web开发", "前端", "后端"]]
    db.session.add_all(tags)
    db.session.flush()

    sample_content = """# 欢迎来到我的博客

这是一篇使用 **Markdown** 编写的示例文章。

## 功能特性

- 支持 *Markdown* 语法
- 代码高亮
- 图片嵌入
- 表格、引用

## 代码示例

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Blog!"
```

> 这是一段引用文本。Flask 是一个轻量级的 Python Web 框架。

## 表格

| 框架 | 语言 | 特点 |
|-----|------|-----|
| Flask | Python | 轻量灵活 |
| Django | Python | 全功能 |
| FastAPI | Python | 异步高性能 |

希望大家在这里享受写作的乐趣！
"""

    posts_data = [
        ("Flask 入门指南：从零开始搭建 Web 应用", "Flask 是一个轻量级 Python Web 框架，非常适合初学者快速上手。", cats[0], ["Python", "Flask"]),
        ("MySQL 5.7 性能优化实战", "通过索引优化、查询优化、配置调优等手段全面提升 MySQL 性能。", cats[0], ["MySQL", "后端"]),
        ("SQLAlchemy ORM 使用全攻略", "深入理解 SQLAlchemy 的模型定义、关系映射、查询语法。", cats[3], ["Python", "Web开发"]),
        ("写给程序员的时间管理建议", "提高效率不是靠加班，而是靠科学的时间管理方法。", cats[1], []),
        ("《重构》读书笔记：让代码更优雅", "Martin Fowler 的经典之作，每个程序员都应该读。", cats[2], []),
        ("从零开始构建个人博客系统", "本系列将带你一步步实现一个完整的博客系统。", cats[3], ["Python", "Flask", "MySQL"]),
    ]

    for title, summary, cat, tag_names in posts_data:
        post = Post(
            title=title,
            summary=summary,
            content=sample_content,
            category_id=cat.id,
            user_id=admin.id,
            is_published=True,
        )
        for tn in tag_names:
            t = Tag.query.filter_by(name=tn).first()
            if t:
                post.tags.append(t)
        db.session.add(post)

    db.session.commit()
    print("[OK] 示例数据已插入")
    print("       默认管理员账号：admin / admin123")


if __name__ == "__main__":
    init()
