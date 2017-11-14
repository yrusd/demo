#coding=utf-8

from time import sleep
import base64
import os
import xml.dom.minidom
import xlrd
from datetime import *
import time
import string


__iniFileName__ = 'Yqzl_DonetAndJava.ini'

def getTagData(dom,tagname):
    return str(dom.getElementsByTagName(tagname)[0].childNodes[0].data) if dom.getElementsByTagName(tagname).length > 0 else ''

def getTagAttr(dom,tagname):
    dic = dict()
    for inner in dom.getElementsByTagName(tagname):
        dic.setdefault(str(inner.getAttribute('key')),str(inner.getAttribute('value')))
    return dic

def getTagSigAttr(dom,tagname,attrname):
    return str(dom.getElementsByTagName(tagname)[0].getAttribute(attrname)) if dom.getElementsByTagName(tagname).length > 0 else '>'

def setTagAttr(dom,tagname,value):
    for inner in dom.getElementsByTagName(tagname):
        inner.setAttribute('value',value)

def delXls(dom,filepath,dic,optition):
    data = xlrd.open_workbook(filepath)
    fileNames = []
    nameConvert = getTagAttr(dom,'NameConvert_item')
    DoNet_Script = dict()
    Java_Script = dict()
    for (k,x) in dic.items():
        table = data.sheet_by_name(k)
        col1 = table.col_values(1)
        row1 = table.row_values(0)
        if k != "BankAreas":
            colCreatedOn = row1.index('CreatedOn')
            colLastModifiedOn = row1.index('LastModifiedOn')
        row1 = [ inner for inner in row1 if inner != '']
        rowsnum = table.nrows
        colsstr = [ [ '\'' + inner + '\'' if isinstance(inner,(str)) else str(int(inner)) for inner in table.row_values(i) ] for i in range(rowsnum) if i > 0 and table.cell_value(i,7) != '' ]

        DoNet = []
        DoNet_values = []
        for inner in colsstr:
            #print(inner[colLastModifiedOn])

            if k != "BankAreas":

                if len(inner[colLastModifiedOn]) < 4:
                    continue

                inner[colLastModifiedOn] = xlrd.xldate.xldate_as_tuple(float(inner[colLastModifiedOn]), 0) 
                y,m,d ,h,M,s = inner[colLastModifiedOn][0:6]

                lastDateTime = str(y) + "%02d" % m + "%02d" % d + "%02d" % h + "%02d" % M + "%02d" % s

                if(int(lastDateTime) < int(x)):
                    continue

                inner[colLastModifiedOn] = datetime(y,m,d ,h,M,s)
                inner[colLastModifiedOn] = inner[colLastModifiedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')

                inner[colCreatedOn] = xlrd.xldate.xldate_as_tuple(float(inner[colCreatedOn]), 0) 
                y,m,d ,h,M,s = inner[colCreatedOn][0:6]
                inner[colCreatedOn] = datetime(y,m,d ,h,M,s)
                inner[colCreatedOn] = inner[colCreatedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')
            
            del inner[0]
            DoNet_values.append(inner)
            DoNet.append(dict(zip(row1, inner)))
        
        if(len(DoNet) > 0):

            Java = ConvertToJavaDic(dom,k + '_item',DoNet,k)
            #DoNet_keys = tuple(DoNet[0].keys())
            #DoNet_values = tuple(tuple(d.values()) for d in DoNet)
            if (len(Java) > 0):
                Java_keys = tuple(Java[0].keys())
                Java_values = tuple(tuple(d.values()) for d in Java)

                Java_keys = 'insert into ' + nameConvert[k] + ' (' + ','.join(Java_keys) + ') values ('
                #colstr = [[ '\'1_' + x + '\'_1' for x in inner] for innner in
                #colsstr]
                Java_values = [Java_keys + ','.join(inner) + '); \n' for inner  in Java_values]

                Java_Script.setdefault(nameConvert[k],''.join(Java_values) + ''  if len(Java_values) > 0 else '')


            row1 = 'insert into ' + k + ' (' + ','.join(row1) + ') values ('
            #colstr = [[ '\'1_' + x + '\'_1' for x in inner] for innner in
            #colsstr]
            DoNet_values = [row1 + ','.join(inner) + '); \n' for inner  in DoNet_values]

            #filename =".net_"+ k + '_' +
            #time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
            #fp = open(os.getcwd() + '\\' +
            #filename,mode="a+",encoding="UTF-8")
            #for inner in DoNet_values:
            #    print(str(inner))
            #    fp.writelines(str(inner))
            #fp.writelines('commit;')

            DoNet_Script.setdefault(k,''.join(DoNet_values) + '' if len(DoNet_values) > 0 else '')

            
            #filename ="java_"+ nameConvert[k] + '_' +
            #time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
            #fp = open(os.getcwd() + '\\' +
            #filename,mode="a+",encoding="UTF-8")
            #for inner in Java_values:
            #    print(str(inner))
            #    fp.writelines(str(inner))
            #fp.writelines('commit;')
    
    filename = ".net_" + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
    fp = open(os.getcwd() + '\\' + filename,mode="a+",encoding="UTF-8") 
    if 'Sy_banks' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_banks"])
    if 'Sy_StandardAreas' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_StandardAreas"])
    if 'Sy_BankAccessSystems' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_BankAccessSystems"])
    if 'BankAreas' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["BankAreas"])
    if 'Sy_BankAccessCmds' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_BankAccessCmds"])
    if 'Sy_BankParamDef' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_BankParamDef"])
    if 'Sy_BankParams' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_BankParams"])
    if 'Sy_QryCmdAccConfig' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_QryCmdAccConfig"])
    if 'Sy_UnifiedPayCode' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_UnifiedPayCode"])
    if 'Sy_PayStateConfig' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_PayStateConfig"])
    if 'Sy_PayCodeMappings' in DoNet_Script.keys():
        fp.writelines(DoNet_Script["Sy_PayCodeMappings"])
    print(filename)
    filename = "java_" + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
    fp = open(os.getcwd() + '\\' + filename,mode="a+",encoding="UTF-8") 
    fp.writelines('spool direct.log  \n')
    if 't_sy_banks' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_banks"])
    if 't_sy_areas' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_areas"])
    if 't_sy_directchannels' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchannels"])
    if 't_sy_directchannelareas' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchannelareas"])
    if 't_sy_directchannelcmds' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchannelcmds"])
    if 't_sy_directchannelcmdparamdef' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchannelcmdparamdef"])
    if 't_sy_directchannelcmdparamval' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchannelcmdparamval"])
    if 't_sy_directquerycmdconfigs' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directquerycmdconfigs"])
    if 't_sy_transcodes' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_transcodes"])
    if 't_sy_directchanneltransresults' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchanneltransresults"])    
    if 't_sy_directchanneltranscodes' in Java_Script.keys():
        fp.writelines(Java_Script["t_sy_directchanneltranscodes"])
    fp.writelines('spool off  \n')
    print(filename)

def ConvertToJavaDic(dom,tagname,list,tablename):
    tagDic = getTagAttr(dom,tagname)
    nameDic = getTagAttr(dom,"CommandTypeConvert_item")
    codeDic = getTagAttr(dom,"DirectAccessCodeConvert_item")
    unifiedIDDic = getTagAttr(dom,"UnifiedIDConvert_item")
    t_sy_directchannelareasDic = getTagAttr(dom,"t_sy_directchannelareas_item")
    directPayWayConvertDic = getTagAttr(dom,"DirectPayWayConvert_item")
    paystateConvertDic = getTagAttr(dom,"PayStateConvert_item")
    Java = []    
    appendFlag = True
    for inner in list:
        appendFlag = True
        JavaDic = dict()
        if tablename == "BankAreas":
            for(k,v) in t_sy_directchannelareasDic.items():
                JavaDic.setdefault(k,v)
        for (k,v) in inner.items():
            if(tablename == "Sy_UnifiedPayCode" and k == "URID"):
                JavaDic.setdefault("URID",unifiedIDDic[v.replace('\'','')])
                continue
            if(tablename == "Sy_PayStateConfig" and k == "DirectPayWay"):
                if len(v.replace('\'','')) > 1:
                    JavaDic.setdefault("DIRECTPAYWAY",directPayWayConvertDic[v.replace('\'','')])
                    continue
                else:
                    JavaDic.setdefault("DIRECTPAYWAY",v)
                    continue
            if(tablename == "Sy_PayStateConfig" and k == "PayState"):
                if v in paystateConvertDic.keys():
                    v = paystateConvertDic[v]                    
            if(tablename == "Sy_PayStateConfig" and k == "UnifiedPayCode"):
                if v not in unifiedIDDic.values():
                    v = '\'E8001\''
                    #continue
                    #appendFlag = False
                    #break
            if(tablename == "Sy_PayCodeMappings" and k == "UnifiedID"):
                if v not in unifiedIDDic.keys():
                    v = '8001'
                    #appendFlag = False
                    #break
                JavaDic.setdefault("TRANSCODEID",unifiedIDDic[v.replace('\'','')])
                continue
            if(tablename == "Sy_PayStateConfig" and k == "DirectAccessCode"):
                JavaDic.setdefault("DIRECTCHANNELID",codeDic[v.replace('\'','')])
                continue
            if(tagDic[k] != '' and tagDic[k] != None):
                if(tablename == "Sy_QryCmdAccConfig" and k == "Description"):
                    for(d,c) in nameDic.items():
                        if(d in v):
                            JavaDic.setdefault("COMMANDTYPE",c)
                            break
                if(str(tagDic[k]) == "CREATEDBY" or str(tagDic[k]) == "LASTMODIFIEDBY"):
                    JavaDic.setdefault(str(tagDic[k]),'\'admin\'')
                else:
                    JavaDic.setdefault(str(tagDic[k]),v)
                continue
        if appendFlag:
            Java.append(JavaDic)
    return Java
    
dom = xml.dom.minidom.parse(os.getcwd() + '\\' + __iniFileName__)
delXls(dom,getTagData(dom,'filepath'),getTagAttr(dom,'item'),getTagSigAttr(dom,'dealitems','optition'))