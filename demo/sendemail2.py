#!/usr/bin/python
# coding: utf-8 -*-

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.message import Message

class Mail:
    def __init__(self,mailServer="smtp.mxhichina.com",user="zhangxw@fingard.com.cn",pwd=""):
        self.mailServer = mailServer
        self.user = user
        self.pwd = pwd
        self.conn = None
    def send_mail(self,mailFrom,mailTo,msg):
        try:
            self.conn = smtplib.SMTP()
            self.conn.connect(self.mailServer)
            self.conn.login(self.user,self.pwd)
            self.conn.sendmail(mailFrom, mailTo, msg.as_string())
            self.conn.close()
            return True
        except Exception as e:
            return False
 
    def send_text(self,mailFrom,mailTo,subject,text):
        #msg = MIMEText(str(text),format,'utf-8')
        msg = Message()
        me = ("%s<" + mailFrom + ">") % (Header(mailFrom,'utf-8'),)
        msg['From'] = me
        msg['To'] = ",".join(mailTo)

        if not isinstance(subject,str):
            subject = str(subject,'utf-8')
        msg['Subject'] = subject

        if not isinstance(text,str):
            text = str(text,'utf-8')
        msg.set_payload('mail content '+ text)

        print(msg)

        return self.send_mail(me,mailTo,msg)

#for test
s = Mail()
subject = "mailtitle5"
txt = '''hi,1'''
s.send_text("zhangxw@fingard.com.cn",["zhangxw@fingard.com.cn","494923605@qq.com"],subject,txt)