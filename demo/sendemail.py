import smtplib
import time
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
import email.utils
import base64
import os

smtpserver='smtp.mxhichina.com'
username='zhangxw@fingard.com.cn'
password=''

from_addr='zhangxw@fingard.com.cn'
to_addr = ["zhangxw@fingard.com.cn","494923605@qq.com"]
#cc_addr = '494923605@qq.com'

time = email.utils.formatdate(time.time(),True)

message = MIMEMultipart('alternative')
message['Subject'] = 'Mail Subject1'+time
message['From'] = from_addr
#print(",".join(to_addr))
message['To'] = 'zhangxw@fingard.com.cn,494923605@qq.com'#",".join(to_addr)
TEXT = u'ABCDEFG一二三四五六七'
part = MIMEText(TEXT, 'plain', 'utf-8')
#message['Cc'] = cc_addr
message.attach(part)

#构造附件1
att1 = MIMEText(open(os.getcwd() +'\\Sy_BankAccessSystems.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="Sy_BankAccessSystems.txt"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
message.attach(att1)

#构造附件2
att2 = MIMEText(open(os.getcwd() +'\\Sy_BankAccessSystems_20160520091504.txt', 'rb').read(), 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="Sy_BankAccessSystems_20160520091504.txt"'
message.attach(att2)

msg = message.as_string()

sm = smtplib.SMTP(smtpserver,port=587,timeout=20)
sm.set_debuglevel(1)
sm.ehlo()
#sm.starttls()
sm.ehlo()
password=base64.b64decode(password)
sm.login(username, password.decode() )

sm.sendmail(from_addr, to_addr, msg.encode('ascii'))
sleep(5)
sm.quit()

print('success')