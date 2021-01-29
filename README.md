


# BaWangCan
一键报名大众点评霸王餐（免费试）

 - 生成Excel表格反馈报名结果
 - 微信公众号推送报名结果

## 第八套中小学生广播体操，现在开始...
第一节，_φ(❐_❐✧ 人丑就要多读书

┏(＾0＾)┛   ┏(´0｀)┛   ┏(´0｀)┛   ┏(´0｀)┛

┗(＾0＾)┏   ┗(｀0´)┏   ┗(｀0´)┏   ┗(｀0´)┏

┗(＾0＾)┛   ┏(´0｀)┛   ┏(´0｀)┛   ┗(｀0´)┏   ┗(｀0´)┏

_(:ι」∠)_好饿，但是不想动

睡觉没前途(￣o￣) . z Z　

## 运行环境

 - [Python 3](https://www.python.org/)

## 第三方库

 - 所需的第三库已放置在【***requirements.txt***】，可使用pip进行批量安装。
```python
pip install -r requirements.txt
```

## 微信推送

 - 从[Server酱](http://sc.ftqq.com/?c=code)申请SCKEY，并修改【***backendThread.py***】代码。
```python
    def weixinTrap(self):
        '''
        微信推送
        '''
        # 从http://sc.ftqq.com/?c=code获取微信推送的SCKEY，并绑定官微
        SCKEY = 'SCU155771T3549c0427011a83c02d53a4f054055166012211d21350'    # Server酱申请的SCKEY
```

## FAQ 
### 1. 如果大众点评城市列表发生变化了，咋办？

> 	使用【***getCity.py***】脚本，即可生成【***area.py***】文件。

### 2. 【大众点评免费试.exe】程序太大，大小能优化吗？
> 当前瓶颈：【***PyQt5***】依赖包太大，生成的文件过大。【暂未找到合适的方法】

> 详情可见：[【Python】大众点评免费试Bug列表](https://www.yuque.com/docs/share/e8433f92-6176-47a2-8211-2e1efcb63d7b?#%20%E3%80%8A%E3%80%90Python%E3%80%91%E5%A4%A7%E4%BC%97%E7%82%B9%E8%AF%84%E5%85%8D%E8%B4%B9%E8%AF%95Bug%E5%88%97%E8%A1%A8%E3%80%8B)
