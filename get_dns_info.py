# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_dns_info
   Description :
   Author :       ops@lechebang.com
   date：          2019/6/25
-------------------------------------------------
   Change Activity:
                   2019/6/25:
-------------------------------------------------
"""
import requests
import subprocess
import re

# https://www.dnspod.cn/console/user/security创建API Token
ID = 111111 # 替换
Token = 'xxxxxxxxxxxxxxxxxxxxxxx' # 替换
full_token = '%s,%s' % (ID, Token)
content = {
    "login_token": full_token,
    "format": "json",
    "lang": "cn",
    "error_on_empty": "no",
}


# 获取所有域名
def get_domains():
    res = requests.post(url="https://dnsapi.cn/Domain.List", data=content)
    domains = res.json()['domains']
    return domains


# 获取所有记录
def get_records(domainid):
    content['domain_id'] = domainid
    res = requests.post(url="https://dnsapi.cn/Record.List", data=content)
    records = res.json()['records']
    return records


# 获取证书信息
def get_ssl(full_url):
    try:
        # 通过curl获取证书
        command = 'curl --connect-timeout 5 -lvs https://{}/'.format(full_url)
        cert_info = subprocess.getstatusoutput(command)[1]

        print('domain:', full_url)
        res = re.search(
            'subject:(.*?)\n.*?start date:(.*?)\n.*?expire date:(.*?)\n.*?common name:(.*?)\n.*?issuer:(.*?)\n',
            cert_info)
        print('subject:', res.group(1)),
        print('start date:', res.group(2)),
        print('expire date:', res.group(3)),
        print('common name:', res.group(4)),
        print('issuer:', res.group(5)),
        print('*'*80)
    except Exception as e:
        print('超时或没有证书')


for i in get_domains():
    for j in get_records(i['id']):
        if j['type'] == 'A' or j['type'] == 'CNAME':
            get_ssl(j['name']+'.'+i['name'])


