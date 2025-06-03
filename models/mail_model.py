from src import db
import datetime

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
