#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import requests
import os

#create floder in the current path
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        print (path + 'create floder success')
        os.makedirs(path)
        return True
    else:
        print (path + 'create floder fail or floder  already exist')
        return False

#store pictures
def save_pic(path,pic_name,data):
    if data == None:
        return
    if (not path.endswith("/")):
        path = path + "/"
    # resolve the problem of encode, make sure that chinese name could be store
    #fp = open(string.decode('utf-8').encode('cp936'), 'wb')
    pathName= path+pic_name
    file = open( pathName, "wb")
    file.write(data)
    file.flush()
    file.close()

#download pictures
def downloadPictures(pageAdderss,keyword):

    flag = mkdir(keyword)
    if flag==False:
        return
    pic_url = re.findall('"objURL":"(.*?)",',pageAdderss,re.S)
    i = 0
    print ('find keyword:'+keyword+'\'s picture ，download now...')
    for each in pic_url:
        try:
            pic= requests.get(each, timeout=20,allow_redirects=False)
            print ('number  ' + str(i + 1) + ' picture，the picture address is: ' + str(each))
        except requests.exceptions.ConnectionError:
            print ('error picture couldn\'t be downloaded')
            continue
        string = keyword+'_'+str(i) + '.jpg'
        save_pic(keyword,string,pic.content)
        i += 1

#download by keyword and the numebr of pictures  equal or less than 61 ,cause the label's number of 'objURL' equal or less than 61
def autoPicDownloadMachine_Baidu(word):

    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url,allow_redirects=False)
    downloadPictures(result.text, word)


def getImg(dataList, localPath):
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    x = 0
    for list in dataList:
        for i in list:
            if i.get('thumbURL') != None:
#                print('download now：%s' % i.get('thumbURL'))
                ir = requests.get(i.get('thumbURL'),allow_redirects=False)
                open(localPath + '%d.jpg' % x, 'wb').write(ir.content)
                x += 1
            else:
                print('error this picture couldn\'t be downloaded')

def get_page(page, keyword):
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&ct=201326592&v=flip'
    result = requests.get(url,allow_redirects=False).text
    pic_url = re.findall('"objURL":"(.*?)",', result, re.S)
    urls = []
    urls.append(url)
    next_page = re.search('<a href="(.*?)" class="n">下一页</a>', result).group(1).encode('utf-8')
    next_page = next_page.split("pn")[0]+"pn="
    while len(urls) < page:
        #next_page = re.search('<a href="(.*?)" class="n">下一页</a>', html).group(1).encode('utf-8')
        next_page_full = 'http://image.baidu.com' + next_page+ str(len(urls)*20)
        urls.append(next_page_full)
    i = 0
    my_page=0

    for pageAdderss in urls:
        print (pageAdderss)
        page_pic = 0
        flag = mkdir(keyword)
        # if flag == False:
        #     return
        pic_html = requests.get(pageAdderss, timeout=1000,allow_redirects=False).text
        pic_url = re.findall('"objURL":"(.*?)",', pic_html, re.S)
        print ('find keyword:' + keyword + '\'s picture ，download now...')
        print ("######################the current page is "+ str(my_page)+"##########################")
        my_page+=1
        for each in pic_url:
            print ("#############the current page is "+ str(my_page)+"  the current page_pic is " + str(page_pic) +"  the total pic_number is " + str(i) + "##########################")
            page_pic+=1
            try:
                pic = requests.get(each, timeout=1000,allow_redirects=False)
                print ('number  ' + str(i + 1) + ' picture，the picture address is: ' + str(each))
            except requests.exceptions.ConnectionError:
                print ('error picture couldn\'t be downloaded')
                continue
            string = keyword + '_' + str(i) + '.jpg'
            save_pic(keyword, string, pic.content)
            i += 1



if __name__ == '__main__':
    #keyword = rresultaw_input("Input key word: ")
    #autoPicDownloadMachine_Baidu(keyword)
    #dataList = getManyPages(keyword, 3)
    #getImg(dataList, str(keyword))

    keyword = input("Input key word: ")
    page = int(input("Input page: "))
    get_page(page, keyword)
