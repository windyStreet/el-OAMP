import smtplib
from bin.base.log import Logger
from email.utils import formataddr
from bin import init
from bin.base.sys import Msg
from bin.base.tool import RabbitMQ

L = Logger.getInstance('mail.log')


class Mail(object):
    def __init__(self, ds):
        if ds is None:
            ds = init.CONF_INFO[init.ROOT_DB_DS]
        conf = init.CONF_INFO[ds]
        self.smtp_name = conf.get('toolName')
        self.smtp_port = conf.get('toolPort')
        self.sender_name = '运维平台'
        self.smtp_account = conf.get('toolUser')
        self.smtp_password = conf.get('toolPassword')

    def set_sender_name(self, sender_name):
        self.sender_name = sender_name
        return self

    def send_mail(self, sender_account=None, receiver_accounts=None, msg=None):
        if sender_account is None:
            sender_account = self.smtp_account
            msg['From'] = formataddr([self.sender_name, self.smtp_account])  # 显示发件人信息
        smtp = None
        try:
            # 创建SMTP对象
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp_name, int(self.smtp_port))
            # server.set_debuglevel(1)  # 可以打印出和SMTP服务器交互的所有信息
            # login()方法用来登录SMTP服务器
            smtp.login(self.smtp_account, self.smtp_password)
            # sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文是一个str，as_string()把MIMEText对象变成str
            smtp.sendmail(sender_account, receiver_accounts, msg.as_string())  # 发送者账户 接收者账户 消息内容
            smtp.quit()
            return True
        except Exception as e:
            msg = Msg.getInstance().set_msg('邮件发送处理异常').set_par(str(e)).set_msg_level_exception().json()
            RabbitMQ.getInstance(ds=init.ROOT_MQ_DS).sendMsg(queue=init.MQ_QUEUE_MSG, msg=msg)
            return False


def getInstance(ds=None):
    return Mail(ds=ds)
