#coding=utf-8

from collections import Counter
import re
fin='In the latest move to support the economy, Shanghai, Beijing, Chongqing and six other provinces and municipalities will allow banks to refinance high-quality credit assets rated by the People''s Bank of China, said the central bank, as the program was first introduced in Guangdong and Shandong provinces last year.'
'''fout=open("result.txt","w")'''
str='In the latest move to support the economy, Shanghai, Beijing, Chongqing and six other provinces and municipalities will allow banks to refinance high-quality credit assets rated by the People''s Bank of China, said the central bank, as the program was first introduced in Guangdong and Shandong provinces last year.'
#匹配正则表达式
reObj=re.compile("\b?([a-zA-Z]+)\b?")
words=reObj.findall(str.lower())

print(Counter(words))

#'''
#for word in words:
#    print(word+":%d\t"%Counter(word))

##建立空字典
#word_dict={}
##以单词的小写作为键值进行统计，同时要
#for word in words:
#    if(not word in word_dict):
#        word_dict[word.lower()]=max(0,words.count(word.lower())+words.count(word.upper())+words.count(word))       
#for(word,number) in sorted(word_dict.items()):
#    print(word+":%d\t"%number)'''