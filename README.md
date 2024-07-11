## 证书失效会发生啥？
* 浏览器报不可信，页面被拦截
* 生产事故，运维绩效扣光 - -

## 大厂也会犯的低级失误？
* 苹果15年1月ChinaCache节点证书到期，未更新证书，导致国内用户appstore访问失败: [戳我](http://tech.163.com/15/0126/12/AGSSODRN00094OE0.html?agt=2337%27)
* 乌龙！火狐浏览器忘记续费证书导致所有扩展被禁用: [戳我](https://kuaibao.qq.com/s/20190504A0C43M00?refer=spider)


## get_dns_info.py是什么?
* 域名多、证书多，人工收集困难，漏续费后果严重。此脚本一键收集并生成html格式报表
> 通过域名提供商（DNSpod）API获取所有域名
>> 解析记录
>>> 筛选A记录与CNAME,去重
>>>> Curl获取证书详情、提供商、过期时间等信息
>>>>> 生成HTML报告


## 环境
* python3
* requests 库


## 使用方法
* DNSpod创建Token，替换脚本ID、token
![截图](https://github.com/fcatat/common/raw/master/create_token.jpg)

```python
# https://www.dnspod.cn/console/user/security创建API Token
ID = 111111  # 替换
Token = 'e96527a8944f0123ww9edscsf4d7' # 替换
```

```python
# 仅汇总了域名总数与使用ssl证书量，可按需添加
domain_sum = len(get_domains())
use_ssl_record_sum = len(all_record)
```

* python get_dns_info.py 运行后生成report-new.html


![截图](https://github.com/fcatat/common/raw/master/report_jpg.jpg)


## 关于作者

```python
    fcatat = {
    地点  : "上海",
    职业  : "运维"
  }
```
