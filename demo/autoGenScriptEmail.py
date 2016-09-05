#coding=utf-8

import smtplib
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
import email.utils
import base64
import os
import xml.dom.minidom
import xlrd
from datetime import *
import time
import zipfile

__iniFileName__ = 'autoGenScriptEmail.ini'

class emailClass:
    smtpserver = ''
    smtpserverport = ''
    smtpservertimeout = ''
    username = ''
    password = ''
    from_addr = ''
    to_addr = ''
    subject = ''
    content = ''


def getTagData(dom,tagname):
    return str(dom.getElementsByTagName(tagname)[0].childNodes[0].data) if dom.getElementsByTagName(tagname).length > 0 else ''

def getTagAttr(dom,tagname):
    dic = dict()
    for inner in dom.getElementsByTagName(tagname):
        dic.setdefault(str(inner.getAttribute('key')),int(inner.getAttribute('value')))
    return dic

def setTagAttr(dom,tagname,value):
    for inner in dom.getElementsByTagName(tagname):
        inner.setAttribute('value',value)

def sendEmail(tmpemail,filenames,time):    
    message = MIMEMultipart('alternative')
    message['Subject'] = tmpemail.subject + time
    message['From'] = tmpemail.from_addr
    message['To'] = tmpemail.to_addr
    TEXT = tmpemail.content + time
    part = MIMEText(TEXT, 'plain', 'utf-8')
    message.attach(part)

    for filename in filenames:
        att1 = MIMEText(open(os.getcwd() + '\\' +filename, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename=' + filename
        message.attach(att1)

    msg = message.as_string()

    sm = smtplib.SMTP(tmpemail.smtpserver,port=int(tmpemail.smtpserverport),timeout=int(tmpemail.smtpservertimeout))
    sm.set_debuglevel(1)
    sm.ehlo()
    sm.ehlo()
    password = base64.b64decode(tmpemail.password)
    sm.login(tmpemail.username, password.decode())
    
    sm.sendmail(tmpemail.from_addr, tmpemail.to_addr.split(','), msg.encode('ascii'))
    sleep(5)
    sm.quit()

    print('success')


def delEmailClass(dom):
    tmpEmail = emailClass()
    tmpEmail.smtpserver = getTagData(dom,'smtpserver')
    tmpEmail.smtpserverport = getTagData(dom,'smtpserverport')
    tmpEmail.smtpservertimeout = getTagData(dom,'smtpservertimeout')
    tmpEmail.username = getTagData(dom,'username')
    tmpEmail.password = getTagData(dom,'password')
    tmpEmail.from_addr = getTagData(dom,'from_addr')
    tmpEmail.to_addr = getTagData(dom,'to_addr')
    tmpEmail.subject = getTagData(dom,'subject')
    tmpEmail.content = getTagData(dom,'content')
    return tmpEmail

def delXls(filepath,dic):
    data = xlrd.open_workbook(filepath)
    fileNames = []
    for (k,x) in dic.items():
        table = data.sheet_by_name(k)
        col1 = table.col_values(1)
        row1 = table.row_values(0)
        colCreatedOn = row1.index('CreatedOn')
        colLastModifiedOn = row1.index('LastModifiedOn')
        row1 = [ inner for inner in row1 if inner != '']
        rowsnum = table.nrows
        colsstr = [ [ '\'' + inner + '\'' if isinstance(inner,(str)) else str(int(inner)) for inner in table.row_values(i) ] for i in range(rowsnum) if i > 0 and table.cell_value(i,3) != '' ]
        for inner in colsstr:
            #print(inner[colLastModifiedOn])
            inner[colLastModifiedOn] = xlrd.xldate.xldate_as_tuple(float(inner[colLastModifiedOn]), 0) 
            y,m,d ,h,M,s = inner[colLastModifiedOn][0:6]

            lastDateTime = str(y) + "%02d" % m + "%02d" % d + "%02d" % h + "%02d" % M + "%02d" % s

            if(int(lastDateTime) < x):
                del inner
                continue

            inner[colLastModifiedOn] = datetime(y,m,d ,h,M,s)
            inner[colLastModifiedOn] = inner[colLastModifiedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')

            inner[colCreatedOn] = xlrd.xldate.xldate_as_tuple(float(inner[colCreatedOn]), 0) 
            y,m,d ,h,M,s = inner[colCreatedOn][0:6]
            inner[colCreatedOn] = datetime(y,m,d ,h,M,s)
            inner[colCreatedOn] = inner[colCreatedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')
            
            del inner[0]

        row1 = 'insert into ' + k + ' ( ' + ','.join(row1) + ' )\nvalues ( '
        #colstr = [[ '\'1_' + x + '\'_1' for x in inner] for innner in colsstr]
        colsstr = [row1 + ','.join(inner) + ' ); \n--go\n' for inner  in colsstr]

        filename = k + '_' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
        fp = open(os.getcwd() + '\\' + filename,mode="a+",encoding="UTF-8") 
        for inner  in colsstr:
            print(str(inner))
            fp.writelines(str(inner))
        fp.writelines('commit;')
        fileNames.append(filename)

    return fileNames

def ZipFiles(filenames):
    zipfilename = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.zip'
    z = zipfile.ZipFile(os.getcwd() + '\\' + zipfilename, 'w', zipfile.ZIP_DEFLATED)
    for filename in filenames:
        z.write(os.path.join(filename))
    z.close()
    return zipfilename

dom = xml.dom.minidom.parse(os.getcwd() + '\\' + __iniFileName__)
tmpEmail = delEmailClass(dom)
filenames = delXls(getTagData(dom,'filepath'),getTagAttr(dom,'item'))
zipFiles = []
zipFiles.append(ZipFiles(filenames))
time = email.utils.formatdate(time.time(),True)
if(getTagData(dom,'AutoEmail').upper()=='TRUE'):
    sendEmail(tmpEmail,zipFiles,time)
#setTagAttr(dom,'item',str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))))
#f= open(os.getcwd() + '\\' + __iniFileName__, 'a')
#dom.writexml(f, addindent='  ', newl='\n')
#f.close()