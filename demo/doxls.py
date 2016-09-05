import xlrd
import os
from datetime import *
import time

data = xlrd.open_workbook(u'E:\\documents\\直联接口\\ATS_Project\\003-基础数据\\01-直联银行数据\\直联银行数据.xlsx')

table = data.sheet_by_name(u'Sy_BankAccessSystems')
col1 = table.col_values(1)
#fp= open(os.getcwd() +'\\Sy_BankAccessSystems.txt',mode="a+",encoding="UTF-8") 
#tmp=str(open(os.getcwd() +'\\Sy_BankAccessSystems.txt',mode="r",encoding="utf-8").read())
#print(tmp)
#for inner in fp.readlines():
#    print(inner)
#fp.writelines('123\r\n')
#fp.writelines('123\r\n')
#for inner in fp.readlines():
#    print(inner)
#fp.close()
#col1 = [ inner if isinstance(inner,(str)) else str(int(inner)) for inner in col1 if inner != '']
#col1 = [ inner if isinstance(inner,(str)) else str(inner) for inner in col1]
#col1 = [  inner  for inner in col1 if inner != '']
#map(map,[str,str],col1)
row1=table.row_values(0)
colCreatedOn=row1.index('CreatedOn')
colLastModifiedOn=row1.index('LastModifiedOn')
#print(colCreatedOn)
row1=[ inner for inner in row1 if inner!='']
rowsnum=table.nrows
colsstr=[ [ inner if isinstance(inner,(str)) else str(int(inner)) for inner in table.row_values(i) ] for i in range(rowsnum) if i>0 and table.cell_value(i,3)!='' ]  
for inner in colsstr:    
    inner[colCreatedOn]=xlrd.xldate.xldate_as_tuple(float(inner[colCreatedOn]), 0) 
    y,m,d ,h,M,s= inner[colCreatedOn][0:6]
    inner[colCreatedOn]=datetime(y,m,d ,h,M,s)
    inner[colCreatedOn]=inner[colCreatedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')
    inner[colLastModifiedOn]=xlrd.xldate.xldate_as_tuple(float(inner[colLastModifiedOn]), 0) 
    y,m,d ,h,M,s= inner[colLastModifiedOn][0:6]
    inner[colLastModifiedOn]=datetime(y,m,d ,h,M,s)
    inner[colLastModifiedOn]=inner[colLastModifiedOn].strftime('to_date(\'%Y-%m-%d %H:%M:%S\' ,\'yyyy-mm-dd hh24:mi:ss\')')
    del inner[0]
    #print(inner)
row1='insert into Sy_BankAccessSystems ( '+','.join(row1)+' )\nvalues ( '
colstr=[[ '\''+x+'\'' for x in inner] for innner in colsstr]
colsstr=[row1+','.join(inner) + ' ) \n--go\n' for inner  in colsstr]
#print(colsstr)
fp= open(os.getcwd() +'\\Sy_BankAccessSystems_'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.txt',mode="a+",encoding="UTF-8") 
for inner  in colsstr:
    print(str(inner))
    fp.writelines(str(inner))
#print(','.join(col1))
#print(table.nrows)
#print(table.ncols)
#print(','+','.join(table.col_values(1)))