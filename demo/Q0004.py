#coding=utf-8

from collections import Counter
import re
fin='In the latest move to support the economy, Shanghai, Beijing, Chongqing and six other provinces and municipalities will allow banks to refinance high-quality credit assets rated by the People''s Bank of China, said the central bank, as the program was first introduced in Guangdong and Shandong provinces last year.'
'''fout=open("result.txt","w")'''
str='In the latest move to support the economy, Shanghai, Beijing, Chongqing and six other provinces and municipalities will allow banks to refinance high-quality credit assets rated by the People''s Bank of China, said the central bank, as the program was first introduced in Guangdong and Shandong provinces last year.'
#ƥ��������ʽ
reObj=re.compile("\b?([a-zA-Z]+)\b?")
words=reObj.findall(str.lower())

print(Counter(words))

#'''
#for word in words:
#    print(word+":%d\t"%Counter(word))

##�������ֵ�
#word_dict={}
##�Ե��ʵ�Сд��Ϊ��ֵ����ͳ�ƣ�ͬʱҪ
#for word in words:
#    if(not word in word_dict):
#        word_dict[word.lower()]=max(0,words.count(word.lower())+words.count(word.upper())+words.count(word))       
#for(word,number) in sorted(word_dict.items()):
#    print(word+":%d\t"%number)'''