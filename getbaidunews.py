#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import jieba
import csv
import codecs
import json
reload(sys)
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()
import urllib
import re
'''
when i find a address which is meet the requirement，i stop finding the another address which are also meet the requirements
'''
regex = re.compile('\s+')
jieba.del_word('草坪')
jieba.add_word('张尚武')
jieba.add_word('将军澳')
jieba.add_word('地方台')
jieba.add_word('凤凰视频')
jieba.add_word('港口公园')
jieba.add_word('金龙大道')
jieba.add_word('新华社区')
jieba.add_word('人蚁大战')
jieba.add_word('复兴论坛')
jieba.add_word('小黄家蚁')
jieba.add_word('大井码头')
jieba.add_word('天水围')
jieba.add_word('东南网')
jieba.load_userdict('address.txt')
addressfile = open('address.txt','r')
alladdress = []
for line in addressfile:
    alladdress.append(line[:-1])
#print(len(address_list))
query_word = '红火蚁'
items = 20
#http://news.baidu.com/ns?cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0
#http://news.baidu.com/ns?ct=1&tn=news&ie=utf-8&bt=0&et=0
news_base_url = 'http://news.baidu.com/ns?cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#news_url = news_base_url + query_word
news_list = []
def compareaddress(alladdress , split_list):
    res = []
    for item1 in split_list:
        for item2 in alladdress:
            #((len(item2)%3 - len(item1)) == 0) || (len(item2)%3 - len(item1)) == 1))
            if item2.find(item1) == 0 and ( (len(item2)/3 - len(item1)) == 0   or (len(item2)/3 - len(item1)) == 1) :
                #print (item1 + str(len(item1)))
                #print (item2 + str(len(item2)))
                res.append(item1)
                break
    res = list(set(res))
    return res

def deletelenEqualThree(alist):
    for i in range(len(alist)-1 , -1 , -1):
        if len(alist[i]) == 1:
            del alist[i]

first = True
kk = 0
with open('result6.csv','wb') as f:
    f.write(codecs.BOM_UTF8)
    w = csv.writer(f,dialect='excel')
    for i in range(1,37):#1~36
        items_num = i*items-items
        parameters = {'word': query_word,'pn':items_num}
        #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # 获取 JSON 数据
        r = requests.get(news_base_url, params=parameters, headers = headers)
        print(r.url)
        soup = BeautifulSoup(r.text, 'lxml')
        #news_html_list = soup.select('div.result')
        news_html_list = soup.find_all('div','result')
        for news_html in news_html_list:
            news = {}
            news['标题'] = news_html.a.get_text().strip()
            news['链接'] = news_html.a['href']
            source = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0\xa0', u' ').split(' ')
            news['来源'] = source[0]
            news['发布日期'] = source[1]
            news_content = news_html.find('div').get_text().strip().replace(u'\xa0\xa0', u' ').split(' ')
            news_content[2] = (news_content[2])[5:]
            news_content_tostring = ''.join(news_content[2:-1])
            news['新闻内容'] = news_content_tostring[:-3]
            seg_content_list = jieba.cut(news['新闻内容'], cut_all=False)#seg_content_list is a generator
            seg_title_list = jieba.cut(news['标题'], cut_all=False)
            #print(type(seg_content_list))
            seg_content_res = " ".join(seg_content_list)  # 全模式
            seg_title_res = " ".join(seg_title_list)  # 全模式
            #print(seg_content_res)

            seg_content_res_list = filter(None,seg_content_res.split(' '))
            #seg_content_res_list = list(set(seg_content_res_list))
            seg_title_res_list = filter(None, seg_title_res.split(' '))
            #seg_title_res_list = list(set(seg_title_res_list))
            all_res_list = seg_content_res_list + seg_title_res_list
            all_res_list = list(set(all_res_list))
            #get_title_addresss_list = compareaddress(alladdress,seg_title_res_list)
            print kk
            kk = kk+1
            news['新闻内容分词结果'] = '/ '.join(seg_content_res_list)
            news['新闻标题分词结果'] = '/ '.join(seg_title_res_list)
            #print(len(seg_content_res_list))
            deletelenEqualThree(all_res_list)
            #print(len(seg_content_res_list))
            #print(' '.join(seg_content_res_list))
            get_all_addresss_list = compareaddress(alladdress, all_res_list)
            #print(seg_content_res_list[0])
            news['地址'] = ' '.join(get_all_addresss_list)
            #news['标题地址'] = ' '.join(get_title_addresss_list)
            # print(news['标题'] )
            # for i in range(len(news['标题地址'])):
            #     print news['标题地址'][i],
            # print
            #print(news['新闻内容地址'])
            #print (['新闻内容分词'])
            #news_list.append(news)
            #print (((news_list[kk])['新闻内容分词']))
            if first:
                w.writerow(news.keys())
                first = False
            w.writerow(news.values())

# for news in news_list:
#     print(news['标题地址'])

# print len(news_list)
# newslist = []
# for news in news_list:
#     newslist.append(json.dumps(news,ensure_ascii=False,encoding="utf-8"))
#     #print(json.dumps(news,ensure_ascii=False,encoding="utf-8")  )
# # for news in newslist:
# #     seg_list = jieba.cut(news['新闻内容'], cut_all=True)
# #     print(",".join(seg_list))  # 全模式
# print newslist[0]

# for news in news_list:
#     print(news['新闻内容'])

# print len(news_list)
# newslist = []
# for news in news_list:
#     newslist.append(json.dumps(news,ensure_ascii=False,encoding="utf-8"))
#
# print newslist[0]