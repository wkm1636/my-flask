# Personal Blog Bot

一个基于 **Flask + MySQL 5.7** 构建的个人博客系统，前后端不分离（服务端渲染），UI 现代美观，开箱即用。

## 功能特性

- **用户系统**：注册、登录、登出、密码加密存储、记住我
- **博客管理**：文章 CRUD、Markdown 编辑、封面图上传、草稿/发布
- **分类标签**：文章分类管理、多标签支持
- **评论互动**：登录用户可对文章发表评论
- **首页展示**：分页、关键词搜索、分类/标签筛选、热门文章
- **个人控制台**：数据概览、文章管理、个人资料、修改密码
- **安全防护**：CSRF 防护、XSS 过滤（bleach）、密码哈希、登录态管理
- **现代 UI**：渐变配色、卡片式布局、响应式设计、移动端友好

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Flask 3.0 |
| ORM | Flask-SQLAlchemy |
| 数据库 | MySQL 5.7 (PyMySQL 驱动) |
| 认证 | Flask-Login |
| 表单 | Flask-WTF + WTForms |
| 数据库迁移 | Flask-Migrate (Alembic) |
| 模板引擎 | Jinja2 |
| Markdown | python-markdown + bleach |
| 前端 | 原生 HTML/CSS/JS + Bootstrap Icons |

## 项目结构

```
personal_bolg_bot/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── filters.py           # Jinja2 过滤器（Markdown 渲染等）
│   ├── models/              # 数据模型 (User / Post / Category / Tag / Comment)
│   ├── forms/               # WTForms 表单
│   ├── routes/              # 蓝图路由 (main / auth / blog / dashboard)
│   ├── utils/               # 工具函数 + 错误处理
│   ├── templates/           # Jinja2 模板
│   └── static/              # 静态资源 (CSS / JS / 上传图片)
├── config.py                # 配置类
├── run.py                   # 启动入口
├── init_db.py               # 数据库初始化脚本
├── requirements.txt         # 依赖
├── .env.example             # 环境变量示例
└── README.md
```

## 快速开始

### 1. 准备环境

- Python 3.10+
- MySQL 5.7+
- pip

### 2. 克隆项目并安装依赖

```bash
cd personal_bolg_bot
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 创建 MySQL 数据库

登录 MySQL 5.7 后执行：

```sql
CREATE DATABASE personal_blog_bot
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`，填入数据库信息：

```bash
# Windows
copy .env.example .env
# Linux / macOS
cp .env.example .env
```

编辑 `.env`：

```env
SECRET_KEY=你自己生成的随机字符串
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的MySQL密码
MYSQL_DATABASE=personal_blog_bot
```

### 5. 初始化数据库

```bash
# 创建表 + 插入示例数据（推荐首次使用）
python init_db.py --seed

# 或仅创建表
python init_db.py
```

默认管理员账号：

- 用户名：`admin`
- 密码：`admin123`

### 6. 启动应用

```bash
python run.py
```

打开浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 使用 Flask-Migrate 管理数据库（可选）

如果你希望使用迁移工具来管理表结构变更：

```bash
# Windows PowerShell
$env:FLASK_APP="run.py"
# Linux / macOS
export FLASK_APP=run.py

flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

## 主要页面

| 路径 | 说明 |
|------|------|
| `/` | 首页（文章列表 + 搜索 + 筛选） |
| `/auth/register` | 注册 |
| `/auth/login` | 登录 |
| `/blog/<id>` | 文章详情 + 评论 |
| `/dashboard` | 用户控制台 |
| `/dashboard/posts` | 文章管理 |
| `/dashboard/posts/new` | 写文章 |
| `/dashboard/categories` | 分类管理 |
| `/dashboard/profile` | 个人资料 |
| `/about` | 关于本站 |

## 权限说明

- **首位注册的用户**会自动被设置为管理员
- 普通用户只能管理自己的文章和评论
- 管理员可以删除任意评论、管理分类

## 安全建议（生产部署）

1. 修改 `SECRET_KEY` 为强随机字符串
2. 关闭 `DEBUG`，使用 `production` 配置
3. 使用 HTTPS（Nginx 反代）
4. 使用 Gunicorn / uWSGI 等 WSGI 服务器
5. 严格限制 MySQL 用户权限
6. 定期备份数据库

## 部署示例（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

## License

MIT
