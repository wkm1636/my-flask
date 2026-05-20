-- ============================================================
--  Personal Blog Bot - 数据库初始化脚本
--  数据库: MySQL 5.7+
--  字符集: utf8mb4
--  生成日期: 2026-05-19
-- ============================================================
--
--  用法:
--    1) 命令行: mysql -u root -p < personal_blog_bot.sql
--    2) Navicat / DBeaver / Workbench 等可视化工具直接打开执行
--    3) 进入 MySQL 后: SOURCE /path/to/personal_blog_bot.sql;
--
--  默认管理员账号: admin / admin123
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';

-- ------------------------------------------------------------
-- 1. 创建数据库
-- ------------------------------------------------------------
DROP DATABASE IF EXISTS `personal_blog_bot`;
CREATE DATABASE `personal_blog_bot`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `personal_blog_bot`;


-- ============================================================
-- 2. 表结构
-- ============================================================

-- ------------------------------------------------------------
-- 2.1 用户表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id`            INT             NOT NULL AUTO_INCREMENT       COMMENT '主键ID',
    `username`      VARCHAR(64)     NOT NULL                      COMMENT '用户名',
    `email`         VARCHAR(120)    NOT NULL                      COMMENT '邮箱',
    `password_hash` VARCHAR(255)    NOT NULL                      COMMENT '密码哈希(werkzeug)',
    `avatar`        VARCHAR(255)    DEFAULT 'default_avatar.png'  COMMENT '头像路径',
    `bio`           VARCHAR(255)    DEFAULT '这个人很懒，还没写简介~' COMMENT '个人简介',
    `is_admin`      TINYINT(1)      DEFAULT 0                     COMMENT '是否管理员',
    `created_at`    DATETIME        DEFAULT CURRENT_TIMESTAMP     COMMENT '注册时间',
    `last_login`    DATETIME        DEFAULT CURRENT_TIMESTAMP     COMMENT '最后登录时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_users_username` (`username`),
    UNIQUE KEY `uq_users_email`    (`email`),
    KEY `ix_users_username` (`username`),
    KEY `ix_users_email`    (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';


-- ------------------------------------------------------------
-- 2.2 分类表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id`          INT          NOT NULL AUTO_INCREMENT    COMMENT '主键ID',
    `name`        VARCHAR(64)  NOT NULL                   COMMENT '分类名',
    `description` VARCHAR(255) DEFAULT NULL               COMMENT '分类描述',
    `created_at`  DATETIME     DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_categories_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章分类表';


-- ------------------------------------------------------------
-- 2.3 标签表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
    `id`   INT         NOT NULL AUTO_INCREMENT  COMMENT '主键ID',
    `name` VARCHAR(50) NOT NULL                 COMMENT '标签名',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_tags_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';


-- ------------------------------------------------------------
-- 2.4 文章表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
    `id`           INT          NOT NULL AUTO_INCREMENT    COMMENT '主键ID',
    `title`        VARCHAR(200) NOT NULL                   COMMENT '文章标题',
    `summary`      VARCHAR(500) DEFAULT NULL               COMMENT '文章摘要',
    `content`      LONGTEXT     NOT NULL                   COMMENT '文章正文(Markdown)',
    `cover_image`  VARCHAR(255) DEFAULT NULL               COMMENT '封面图路径',
    `views`        INT          DEFAULT 0                  COMMENT '阅读量',
    `is_published` TINYINT(1)   DEFAULT 1                  COMMENT '是否发布(0草稿/1已发布)',
    `created_at`   DATETIME     DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
    `updated_at`   DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `user_id`      INT          NOT NULL                   COMMENT '作者ID',
    `category_id`  INT          DEFAULT NULL               COMMENT '分类ID',
    PRIMARY KEY (`id`),
    KEY `ix_posts_title`       (`title`),
    KEY `ix_posts_created_at`  (`created_at`),
    KEY `fk_posts_user`        (`user_id`),
    KEY `fk_posts_category`    (`category_id`),
    CONSTRAINT `fk_posts_user`     FOREIGN KEY (`user_id`)     REFERENCES `users` (`id`)      ON DELETE CASCADE,
    CONSTRAINT `fk_posts_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='博客文章表';


-- ------------------------------------------------------------
-- 2.5 文章-标签 关联表 (多对多)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `post_tags`;
CREATE TABLE `post_tags` (
    `post_id` INT NOT NULL COMMENT '文章ID',
    `tag_id`  INT NOT NULL COMMENT '标签ID',
    PRIMARY KEY (`post_id`, `tag_id`),
    KEY `fk_pt_tag` (`tag_id`),
    CONSTRAINT `fk_pt_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_pt_tag`  FOREIGN KEY (`tag_id`)  REFERENCES `tags`  (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章标签关联表';


-- ------------------------------------------------------------
-- 2.6 评论表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
    `id`         INT          NOT NULL AUTO_INCREMENT    COMMENT '主键ID',
    `content`    VARCHAR(500) NOT NULL                   COMMENT '评论内容',
    `created_at` DATETIME     DEFAULT CURRENT_TIMESTAMP  COMMENT '评论时间',
    `user_id`    INT          NOT NULL                   COMMENT '评论用户ID',
    `post_id`    INT          NOT NULL                   COMMENT '所属文章ID',
    PRIMARY KEY (`id`),
    KEY `ix_comments_created_at` (`created_at`),
    KEY `fk_comments_user`       (`user_id`),
    KEY `fk_comments_post`       (`post_id`),
    CONSTRAINT `fk_comments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comments_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';


-- ============================================================
-- 3. 示例数据
-- ============================================================

-- ------------------------------------------------------------
-- 3.1 管理员用户
--      用户名: admin
--      密码:   admin123  (使用 werkzeug pbkdf2:sha256 哈希)
-- ------------------------------------------------------------
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `avatar`, `bio`, `is_admin`, `created_at`, `last_login`) VALUES
(1, 'admin', 'admin@example.com',
 'pbkdf2:sha256:1000000$TShCEtpBmGwzktS2$c83e0f21f394294809ea39c53070d93b32612727febe055002200b9d7e3456a3',
 'default_avatar.png', '本站管理员，热爱分享技术与生活。', 1, NOW(), NOW());


-- ------------------------------------------------------------
-- 3.2 分类数据
-- ------------------------------------------------------------
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`) VALUES
(1, '技术分享', '编程、开发、架构相关',   NOW()),
(2, '生活随笔', '日常生活与思考',         NOW()),
(3, '读书笔记', '读书心得与笔记',         NOW()),
(4, '项目实战', '项目开发实战记录',       NOW());


-- ------------------------------------------------------------
-- 3.3 标签数据
-- ------------------------------------------------------------
INSERT INTO `tags` (`id`, `name`) VALUES
(1, 'Python'),
(2, 'Flask'),
(3, 'MySQL'),
(4, 'Web开发'),
(5, '前端'),
(6, '后端');


-- ------------------------------------------------------------
-- 3.4 示例文章
-- ------------------------------------------------------------
INSERT INTO `posts` (`id`, `title`, `summary`, `content`, `cover_image`, `views`, `is_published`, `user_id`, `category_id`, `created_at`, `updated_at`) VALUES
(1, 'Flask 入门指南：从零开始搭建 Web 应用',
    'Flask 是一个轻量级 Python Web 框架，非常适合初学者快速上手。本文带你从环境搭建到第一个 Web 应用。',
    '# Flask 入门指南\n\nFlask 是一个轻量级的 Python Web 框架。\n\n## 安装\n\n```bash\npip install flask\n```\n\n## Hello World\n\n```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "Hello, Flask!"\n\nif __name__ == "__main__":\n    app.run(debug=True)\n```\n\n> Flask 的核心理念是「微」与「灵活」。\n\n## 优势\n\n- 入门简单\n- 扩展灵活\n- 生态丰富\n- 适合中小型项目',
    NULL, 168, 1, 1, 1, NOW(), NOW()),

(2, 'MySQL 5.7 性能优化实战',
    '通过索引优化、查询优化、配置调优等手段全面提升 MySQL 性能。',
    '# MySQL 5.7 性能优化\n\n## 索引优化\n\n- 为 WHERE 条件创建索引\n- 避免在索引列上使用函数\n- 使用覆盖索引\n\n## 配置调优\n\n```ini\n[mysqld]\ninnodb_buffer_pool_size = 4G\ninnodb_log_file_size = 512M\nmax_connections = 500\n```\n\n## 查询优化\n\n使用 `EXPLAIN` 分析查询：\n\n```sql\nEXPLAIN SELECT * FROM posts WHERE user_id = 1;\n```\n\n> 建议：每周分析一次慢查询日志。',
    NULL, 245, 1, 1, 1, NOW(), NOW()),

(3, 'SQLAlchemy ORM 使用全攻略',
    '深入理解 SQLAlchemy 的模型定义、关系映射、查询语法、性能优化。',
    '# SQLAlchemy ORM 使用全攻略\n\n## 模型定义\n\n```python\nfrom flask_sqlalchemy import SQLAlchemy\ndb = SQLAlchemy()\n\nclass User(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(64), unique=True)\n```\n\n## 关系映射\n\n- 一对多: `db.relationship`\n- 多对多: 通过中间表\n\n## 常用查询\n\n```python\nUser.query.filter_by(username="admin").first()\nUser.query.order_by(User.created_at.desc()).limit(10).all()\n```',
    NULL, 132, 1, 1, 4, NOW(), NOW()),

(4, '写给程序员的时间管理建议',
    '提高效率不是靠加班，而是靠科学的时间管理方法。分享我多年实践的几个原则。',
    '# 程序员的时间管理\n\n## 番茄工作法\n\n25 分钟专注 + 5 分钟休息，一个轮回为一个番茄。\n\n## 任务清单\n\n- 早晨列出当日 3 件最重要的事\n- 用 GTD 方法处理琐事\n- 周日复盘本周\n\n> 时间管理的本质是精力管理。\n\n## 专注工具\n\n1. 屏蔽通知\n2. 关闭无关网页\n3. 使用白噪音',
    NULL, 89, 1, 1, 2, NOW(), NOW()),

(5, '《重构》读书笔记：让代码更优雅',
    'Martin Fowler 的经典之作，每个程序员都应该读。本文整理书中核心要点。',
    '# 《重构》读书笔记\n\n## 什么是重构\n\n在不改变软件外部行为的前提下，改善其内部结构。\n\n## 代码的坏味道\n\n- 重复代码\n- 过长函数\n- 过大的类\n- 过长参数列\n- 发散式变化\n\n## 常用手法\n\n1. **提炼函数** (Extract Function)\n2. **内联函数** (Inline Function)\n3. **提炼变量** (Extract Variable)\n4. **改变函数声明** (Change Function Declaration)\n\n> 让营地比你来时更干净。',
    NULL, 76, 1, 1, 3, NOW(), NOW()),

(6, '从零开始构建个人博客系统',
    '本系列将带你一步步实现一个完整的博客系统，涵盖前后端、数据库、部署的方方面面。',
    '# 从零构建个人博客\n\n## 技术选型\n\n- 后端: Flask 3.0\n- 数据库: MySQL 5.7\n- ORM: SQLAlchemy\n- 前端: Jinja2 + 原生 CSS\n\n## 项目结构\n\n```\nblog/\n├── app/\n│   ├── models/\n│   ├── routes/\n│   └── templates/\n├── config.py\n└── run.py\n```\n\n## 核心功能\n\n| 模块 | 功能 |\n|------|------|\n| 用户 | 注册、登录、登出 |\n| 文章 | CRUD、分类、标签 |\n| 评论 | 发表、删除 |\n\n> 麻雀虽小，五脏俱全。',
    NULL, 312, 1, 1, 4, NOW(), NOW());


-- ------------------------------------------------------------
-- 3.5 文章-标签 关联
-- ------------------------------------------------------------
INSERT INTO `post_tags` (`post_id`, `tag_id`) VALUES
(1, 1), (1, 2),                 -- Flask入门 -> Python, Flask
(2, 3), (2, 6),                 -- MySQL优化 -> MySQL, 后端
(3, 1), (3, 4),                 -- SQLAlchemy -> Python, Web开发
(6, 1), (6, 2), (6, 3);         -- 博客系统 -> Python, Flask, MySQL


-- ------------------------------------------------------------
-- 3.6 示例评论
-- ------------------------------------------------------------
INSERT INTO `comments` (`content`, `user_id`, `post_id`, `created_at`) VALUES
('写得很好，对初学者非常友好！',   1, 1, NOW()),
('期待后续的进阶教程~',             1, 1, NOW()),
('MySQL 配置那部分太实用了，已收藏。', 1, 2, NOW()),
('SQLAlchemy 的多对多关系一直让我头疼，看完豁然开朗。', 1, 3, NOW());


-- ============================================================
-- 4. 恢复设置
-- ============================================================
SET FOREIGN_KEY_CHECKS = 1;


-- ============================================================
-- 5. 验证
-- ============================================================
SELECT '数据库初始化完成！' AS message;
SELECT
    (SELECT COUNT(*) FROM users)       AS users_count,
    (SELECT COUNT(*) FROM categories)  AS categories_count,
    (SELECT COUNT(*) FROM tags)        AS tags_count,
    (SELECT COUNT(*) FROM posts)       AS posts_count,
    (SELECT COUNT(*) FROM comments)    AS comments_count;

-- ============================================================
--  默认管理员账号:  admin
--  默认管理员密码:  admin123
--  登录后请尽快修改密码!
-- ============================================================
