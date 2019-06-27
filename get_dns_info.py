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
ID = 111111  # 替换
Token = 'e96527a8944f0123ww9edscsf4d7' # 替换
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
        # curl超时时间5秒
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
    except:
        print('超时或没有证书')


def new_get_ssl(full_url):
    try:
        # 配置超时时间5秒
        command = 'curl --connect-timeout 5 -lvs https://{}/'.format(full_url)
        cert_info = subprocess.getstatusoutput(command)[1]
        # name = re.findall('(?<=common.name:).*', cert_info)[0]
        name = full_url
        issuer = re.findall('(?<=issuer:).*', cert_info)[0]
        expire_date = re.findall('(?<=expire.date:).*', cert_info)[0]
        return [name, issuer, expire_date]
    except:
        pass


# 取所有域名改写为html <tb>,使用集合去重
domain_str = ''
all_record = set()
for i in get_domains():
    domain_str_tbody = '<tr>' + '\n' + \
        '<td>' + i['name'] + '</td>' + '\n' + \
        '<td>' + i['grade_title'] + '</td>' + '\n' + \
        '<td>' + i['records'] + '</td>' + '\n' + \
        '<td>' + i['updated_on'] + '</td>' + '\n' + \
        '</tr>' + '\n'
    domain_str += domain_str_tbody
    for j in get_records(i['id']):
        if j['type'] == 'A' or j['type'] == 'CNAME':
            all_record.add(j['name']+'.'+i['name'])


# 拼装record tbody
record_str = ''
for k in all_record:
    record_info = new_get_ssl(k)
    if record_info:
        record_str_tbody = '<tr>' + '\n' + \
            '<td>' + record_info[0] + '</td>' + '\n' + \
            '<td>' + record_info[1] + '</td>' + '\n' + \
            '<td>' + record_info[2] + '</td>' + '\n' + \
            '</tr>' + '\n'
        record_str += record_str_tbody

# 汇总所有数据
domain_sum = len(get_domains())
use_ssl_record_sum = len(all_record)



# html原文
html = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Report</title>
    <!-- Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body id="bg-color" class="bg-warning">
    <div id="container" class="container">

	    <!-- 报告标题 -->
	    <div id="Headrow" class="row">
      		<h1 id="HeadH1" align="center">
      			<strong id="HeadTxt">All_Cert_Info  </strong>
      			<!--<small id="author">Sonny.zhang</small>-->
      		</h1>
      		</br>
	    </div>

		<!-- 数据统计 -->
		<div id="Totalrow" class="Totalrow">
			<div class="jumbotron">
				<!-- 测试执行时间、用例数 -->
			    <div id="UTimerow" class="row">
					<div class="col-xs-12 col-md-6">
						<p role="presentation">
							<span>
								域名总数：<span class="label label-success">%s</span>
							</span>
						</p>
					</div>
					<div class="col-xs-12 col-md-6">
						<p role="presentation">
							<span>
								使用证书总数：</small><span class="label label-success">%s</span>
							</span>
						</p>
					</div>
			    </div>
		    </div>
		</div>

		<!-- 测试计划 -->
	    <div id="domain" class="row">
    		<div id="domain-title" class="panel panel-primary">
    			<div class="panel-heading">
    				<strong><center class="text-uppercase">域名详情</center></strong>
    			</div>
			</div>
			<!-- 一个测试计划 -->
			<div id="tb1">
				<table class="table table-striped">
					<center><caption>只检测A记录与CNAME证书</caption></center>
					<thead>
						<tr>
							<th>域名</th>
							<th>套餐</th>
							<th>条目数</th>
							<th>创建时间</th>
						</tr>
					</thead>
					<tbody>
                        %s
					</tbody>
				</table>
			</div>
	    </div>
        <div id="cert" class="row">
    		<div id="cert-title" class="panel panel-primary">
    			<div class="panel-heading">
    				<strong><center class="text-uppercase">证书详情</center></strong>
    			</div>
			</div>
			<!-- 一个测试计划 -->
			<div id="plan1">
				<table class="table table-striped">
					<center><caption>只检测A记录与CNAME证书</caption></center>
					<thead>
						<tr>
							<th>域名</th>
							<th>发行商</th>
							<th>过期时间</th>
						</tr>
					</thead>
					<tbody>
						%s
					</tbody>
				</table>
			</div>
	    </div>
    </div>
  </body>
</html>

''' % (domain_sum, use_ssl_record_sum, domain_str, record_str)
f = open('report-new.html', 'w')
f.write(html)
f.close()



