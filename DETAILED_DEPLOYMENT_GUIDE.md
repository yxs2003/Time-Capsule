# 时光邮局网站部署详细教程

## 1. 项目概述

时光邮局是一个允许用户发送"未来邮件"的网站应用。用户可以撰写邮件并设置未来的发送日期，系统会在指定日期自动发送邮件到收件人邮箱。

### 主要功能

- 像素风格UI，首页展示一半红一半白的胶囊
- 点击胶囊后的过渡动画效果
- 邮件表单（标题、内容、收件人、收件密码、发信时间）
- 定时邮件发送系统

### 技术栈

- 前端：HTML, CSS, JavaScript
- 后端：Flask (Python)
- 数据库：SQLite
- 邮件发送：Flask-Mail

## 2. 环境准备

### 系统要求

- Python 3.6+ (推荐 Python 3.8+)
- pip 包管理器
- 可用的SMTP邮件服务器

### 安装步骤

1. 克隆或解压源代码到您的服务器

2. 创建并激活虚拟环境（推荐）
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境（Linux/Mac）
   source venv/bin/activate
   
   # 激活虚拟环境（Windows）
   venv\Scripts\activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

## 3. 配置邮件服务

在 `src/main.py` 文件中，找到并修改以下邮件配置：

```python
# 配置邮件服务
app.config['MAIL_SERVER'] = 'smtp.example.com'  # 替换为您的SMTP服务器
app.config['MAIL_PORT'] = 587  # 根据您的SMTP服务器调整端口
app.config['MAIL_USE_TLS'] = True  # 根据需要调整TLS设置
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # 替换为您的邮箱账号
app.config['MAIL_PASSWORD'] = 'your_password'  # 替换为您的邮箱密码
app.config['MAIL_DEFAULT_SENDER'] = ('时光邮局', 'your_email@example.com')  # 替换为发件人信息
```

### 常见SMTP服务器配置

#### Gmail
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_gmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'  # 需要使用应用专用密码
```

#### QQ邮箱
```python
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_qq_number@qq.com'
app.config['MAIL_PASSWORD'] = 'your_authorization_code'  # 需要使用授权码
```

#### 163邮箱
```python
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_account@163.com'
app.config['MAIL_PASSWORD'] = 'your_authorization_code'  # 需要使用授权码
```

## 4. 数据库配置

默认使用SQLite数据库，无需额外配置。如需使用其他数据库（如MySQL或PostgreSQL），修改 `src/main.py` 中的数据库URI：

```python
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_capsule.db'  # 默认SQLite配置

# MySQL配置示例
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/time_capsule_db'

# PostgreSQL配置示例
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/time_capsule_db'
```

## 5. 运行应用

### 开发环境

```bash
# 确保在项目根目录下
cd time_capsule_mail

# 激活虚拟环境（如果使用）
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 运行应用
python src/main.py
```

应用将在 http://localhost:5000 上运行。

### 生产环境

#### 使用Gunicorn（推荐，仅Linux/Mac）

1. 安装Gunicorn
   ```bash
   pip install gunicorn
   ```

2. 运行应用
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 "src.main:app"
   ```

#### 使用uWSGI

1. 安装uWSGI
   ```bash
   pip install uwsgi
   ```

2. 创建uwsgi.ini配置文件
   ```ini
   [uwsgi]
   module = src.main:app
   master = true
   processes = 4
   socket = 0.0.0.0:8000
   chmod-socket = 660
   vacuum = true
   die-on-term = true
   ```

3. 运行应用
   ```bash
   uwsgi --ini uwsgi.ini
   ```

#### 使用Nginx作为反向代理

1. 安装Nginx

2. 配置Nginx
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. 重启Nginx
   ```bash
   sudo systemctl restart nginx
   ```

## 6. 邮件调度系统

### 手动触发邮件检查

访问 `/check-mails` 路由可以手动触发邮件检查和发送：

```
http://your_domain.com/check-mails
```

### 设置定时任务（推荐）

使用cron作业定期触发邮件检查：

1. 编辑crontab
   ```bash
   crontab -e
   ```

2. 添加定时任务（每小时检查一次）
   ```
   0 * * * * curl http://localhost:5000/check-mails
   ```

## 7. 自定义与扩展

### 修改UI样式

- CSS样式文件位于 `src/static/css/style.css`
- JavaScript文件位于 `src/static/js/script.js`
- HTML模板位于 `src/templates/` 目录

### 添加新功能

如需添加新功能，可以在 `src/main.py` 中添加新的路由和处理逻辑。

## 8. 故障排除

### 邮件发送失败

- 检查SMTP服务器配置是否正确
- 确认邮箱账号和密码是否有效
- 查看应用日志获取详细错误信息

### 数据库错误

- 确保应用有权限创建和写入数据库文件
- 检查数据库连接配置

### 应用启动失败

- 检查依赖是否安装完整
- 确认Python版本兼容性
- 查看错误日志

## 9. 安全注意事项

- 生产环境中，不要在代码中硬编码邮箱密码，建议使用环境变量
- 定期更新依赖包以修复潜在安全漏洞
- 考虑对用户密码进行加密存储
- 使用HTTPS保护网站流量

## 10. 维护与备份

- 定期备份数据库文件
- 监控服务器资源使用情况
- 检查邮件发送日志，确保系统正常运行

## 11. 联系与支持

如有任何问题或需要支持，请联系开发者。
