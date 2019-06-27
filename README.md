![截图](https://github.com/fcatat/common/blob/master/report_jpg.jpg?raw=true)

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
* 从DNSpod获取Token
* python get_dns_info.py 运行后生成report-new.html

在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* 邮件(xing_ji#foxmail.com, 把#换成@)


## 关于作者

```python
    fcatat = {
    地点  : "上海",
    职业  : "运维"
  }
```
