from flask import Flask, render_template, request, flash, redirect, url_for
import os
import sys
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_capsule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 配置邮件服务
app.config['MAIL_SERVER'] = 'smtp.example.com'  # 需要替换为实际的SMTP服务器
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # 需要替换为实际的邮箱账号
app.config['MAIL_PASSWORD'] = 'your_password'  # 需要替换为实际的邮箱密码
app.config['MAIL_DEFAULT_SENDER'] = ('时光邮局', 'your_email@example.com')
mail = Mail(app)

# 定义数据模型
class TimeCapsuleMail(db.Model):
    __tablename__ = 'time_capsule_mails'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_sent = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, content, recipient, password, delivery_date):
        self.title = title
        self.content = content
        self.recipient = recipient
        self.password = password
        self.delivery_date = delivery_date
        self.is_sent = False
    
    def __repr__(self):
        return f'<TimeCapsuleMail {self.title} to {self.recipient} on {self.delivery_date}>'

# 邮件发送函数 - 不再使用后台线程
def check_and_send_mails():
    # 获取当前日期
    today = datetime.date.today()
    
    # 查找今天应该发送的邮件
    mails_to_send = TimeCapsuleMail.query.filter(
        TimeCapsuleMail.delivery_date <= today,
        TimeCapsuleMail.is_sent == False
    ).all()
    
    # 发送邮件
    for mail_item in mails_to_send:
        try:
            msg = Message(
                subject=f"时光邮局: {mail_item.title}",
                recipients=[mail_item.recipient],
                body=f"""
您好，

这是一封来自过去的信，由时光邮局为您传递。

标题: {mail_item.title}
内容: {mail_item.content}

查看密码: {mail_item.password}

祝好,
时光邮局
                """
            )
            mail.send(msg)
            
            # 更新邮件状态
            mail_item.is_sent = True
            db.session.commit()
            print(f"邮件已发送至 {mail_item.recipient}")
        except Exception as e:
            print(f"发送邮件失败: {str(e)}")

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        recipient = request.form.get('recipient')
        password = request.form.get('password')
        delivery_date_str = request.form.get('delivery_date')
        
        # 验证所有字段都已填写
        if not all([title, content, recipient, password, delivery_date_str]):
            flash('请填写所有必填字段', 'error')
            return redirect(url_for('index'))
        
        # 转换日期字符串为日期对象
        try:
            delivery_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('日期格式无效', 'error')
            return redirect(url_for('index'))
        
        # 验证日期是否在未来
        if delivery_date <= datetime.date.today():
            flash('请选择未来的日期', 'error')
            return redirect(url_for('index'))
        
        # 创建新的时光邮件
        new_mail = TimeCapsuleMail(
            title=title,
            content=content,
            recipient=recipient,
            password=password,
            delivery_date=delivery_date
        )
        
        # 保存到数据库
        try:
            db.session.add(new_mail)
            db.session.commit()
            flash('您的信已成功保存，将在指定日期发送', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'保存失败: {str(e)}', 'error')
        
        return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

# 添加一个检查邮件的路由，替代后台线程
@app.route('/check-mails', methods=['GET'])
def check_mails():
    check_and_send_mails()
    return "邮件检查完成"

# 创建数据库表 - 不再使用before_first_request装饰器
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
