

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

## 微信推送【感谢Server酱～】

 - 从[Server酱](http://sc.ftqq.com/?c=code)申请SCKEY，并修改【***backendThread.py***】代码。

```python
    def weixinTrap(self):
        '''
        微信推送
        '''
        # 从http://sc.ftqq.com/?c=code获取微信推送的SCKEY，并绑定官微
        SCKEY = 'SCU155771T3549c0427011a83c02d53a4f054055166012211d21350'    # Server酱申请的SCKEY
```

## 更新 by ZhangJinbao520

 - 写作不易，您的Star✨是我继续完善的动力，感谢~

### 2021/02/01

 1. 新增二维码登录功能
 2. 新增微信公众号推送功能
 
 ### 2021/02/03
 
 1. 【***src***】文件夹为UI版本
 2. 【***src2***】文件夹为精简版本，【***config.ini***】需要自给自足

## FAQ 

*建议、吐槽、提问请点击【**[Issues](https://github.com/zhangjinbao520/BaWangCan/issues)**】。*

### 1. 如果大众点评城市列表发生变化了，咋办？

> 	使用【***getCity.py***】脚本，即可生成【***area.py***】文件。

### 2. 【***main.py***】程序打包太大，大小能优化吗？
> 当前瓶颈：【***PyQt5***】依赖包太大，暂未找到合适的方法。
