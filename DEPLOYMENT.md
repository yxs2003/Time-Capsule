# 时光邮局网站部署文档

## 项目概述

时光邮局是一个允许用户发送"未来邮件"的网站应用。用户可以撰写邮件并设置未来的发送日期，系统会在指定日期自动发送邮件到收件人邮箱。

## 技术栈

- 前端：HTML, CSS, JavaScript（像素风格UI）
- 后端：Flask (Python)
- 数据库：SQLite
- 邮件发送：Flask-Mail

## 部署前准备

### 1. 环境要求

- Python 3.6+
- pip 包管理器
- 可用的SMTP邮件服务器

### 2. 配置邮件服务

在 `src/main.py` 文件中，需要修改以下邮件配置：

```python
app.config['MAIL_SERVER'] = 'smtp.example.com'  # 替换为您的SMTP服务器
app.config['MAIL_PORT'] = 587  # 根据您的SMTP服务器调整端口
app.config['MAIL_USE_TLS'] = True  # 根据需要调整TLS设置
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # 替换为您的邮箱账号
app.config['MAIL_PASSWORD'] = 'your_password'  # 替换为您的邮箱密码
app.config['MAIL_DEFAULT_SENDER'] = ('时光邮局', 'your_email@example.com')  # 替换为发件人信息
```

## 部署步骤

### 1. 安装依赖

```bash
# 创建并激活虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 初始化数据库

首次运行应用时，数据库会自动创建。无需额外操作。

### 3. 运行应用

#### 开发环境

```bash
python src/main.py
```

应用将在 http://localhost:5000 上运行。

#### 生产环境

建议使用 Gunicorn 或 uWSGI 作为 WSGI 服务器，并配合 Nginx 作为反向代理。

示例 Gunicorn 命令：

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "src.main:app"
```

### 4. 邮件调度器

应用内置了邮件调度系统，会自动检查并发送到期的邮件。调度器作为守护线程运行，无需额外配置。

## 自定义与扩展

### 修改UI样式

- CSS样式文件位于 `src/static/css/style.css`
- JavaScript文件位于 `src/static/js/script.js`
- HTML模板位于 `src/templates/` 目录

### 数据库迁移

默认使用SQLite数据库。如需迁移到其他数据库（如MySQL或PostgreSQL），修改 `src/main.py` 中的数据库URI：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = '你的数据库URI'
```

## 故障排除

### 邮件发送失败

- 检查SMTP服务器配置是否正确
- 确认邮箱账号和密码是否有效
- 查看应用日志获取详细错误信息

### 数据库错误

- 确保应用有权限创建和写入数据库文件
- 检查数据库连接配置

## 安全注意事项

- 生产环境中，不要在代码中硬编码邮箱密码，建议使用环境变量
- 定期更新依赖包以修复潜在安全漏洞
- 考虑对用户密码进行加密存储

## 联系与支持

如有任何问题或需要支持，请联系开发者。
