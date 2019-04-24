from flask_mail import Message
from app.mail import mail
from datetime import datetime
from flask import current_app


def daily_messenger(orders: list):
    msg = Message(datetime.now().strftime("%Y-%M-%D Messenger"), recipients=["xxx@xxx.com"])
    msg.html = '<table><tbody><tr><th>姓名</th><th>Asin</th><th>订单号</th><th>状态</th><th>价格</th><th>PayPal</th></tr>' + \
               ''.join(map(lambda x: '<tr><td>' + '</td><td>'.join(map(lambda k: str(k), x)) + '</td></tr>', orders)) + \
               '</tbody></table>'
    current_app.logger.info('邮件发送 %s', msg.html)
    mail.send(msg)
