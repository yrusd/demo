#coding=utf-8

__author__='king.z'

import os
import xml.dom.minidom

dom=xml.dom.minidom.parse(os.getcwd()+'\\autoGenScriptEmail.ini')

def getTagData(dom,tagname):
    return str(dom.getElementsByTagName(tagname)[0].childNodes[0].data) if dom.getElementsByTagName(tagname).length>0 else ''

def getTagAttr(dom,tagname):
    dic=dict()
    for inner in dom.getElementsByTagName(tagname):
        dic.setdefault(str(inner.getAttribute('key')),int(inner.getAttribute('value')))
    return dic
 
smtpserver=getTagData(dom,'smtpserver')
print(smtpserver)
#print(smtpserver=='1')
dic=getTagAttr(dom,'item')
#print(dic)
for key,value in dic.items():
    print('{0}:{1}'.format(key,value))
print(dic.get('21'))
print(dic.get('12')==None)