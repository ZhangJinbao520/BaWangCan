# -*- coding: utf-8 -*-
# 
# WARNING: Do not edit this file unless you know what you are doing.
# See https://github.com/zhangjinbao520/BaWangCan
# 
# __author__ = "ZhangJinbao"
# Copyright(C) 2021 ZhangJinbao All rights reserved.
#
# 作用：
#    1、二维码登录状态的监测线程
#    2、【Run】按钮状态的切换线程
#    3、霸王餐（免费试）的报名线程

from PyQt5.QtCore import QThread, pyqtSignal
from openpyxl import Workbook
from config import Config
import requests, time, re, json

class linkStatusThread(QThread):
    '''
    连接状态线程：
        # 实时监测二维码（QRCode）登录状态线程
    '''
    linkStatus = pyqtSignal(int)    # 自定义信号，queryQRCodeStatus的状态码
    def __init__(self, lgtoken):
        super().__init__()
        self.lgtoken = lgtoken
    
    def run(self):
        '''
        run()重写
        信号定义：
             -1 ：连接超时
              0 ：连接中...
              1 ：扫描成功
              2 ：确认登录
              3 ：取消登录
            Oth ：连接异常
        '''
        url = 'https://account.dianping.com/account/ajax/queryqrcodestatus'    # queryQRCodeStatus的URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        data = {'lgtoken': self.lgtoken}
        while True:
            response = requests.post(url=url, headers=headers, data=data)
            if response.status_code == 200:
                status = response.json()['msg']['status']    # 返回状态码
                if status == 2:    # 提取cookie
                    Config().saveConfig('Cookie', 'Cookie', response.headers['set-Cookie'])
                time.sleep(0.5)    # 等待时间，防止线程一直占用CPU
                self.linkStatus.emit(int(status))    # 发射信号
            else:
                self.linkStatus.emit(int(response.status_code))

class runStatusThread(QThread):
    '''
    [Run]按钮的自定义信号线程
    作用：[Run]按钮的文字切换
        '执行中.. '与'执行中...'切换
    '''
    runStatus = pyqtSignal(str)    # 自定义信号
    def __init__(self, currentText=None):
        super().__init__()
        self.currentText = currentText

    def run(self):
        '''
        信号定义：
            开始执行
            执行中.. 
            执行中...
        '''
        while True:
            if self.currentText == "执行中.. ":
                self.runStatus.emit("执行中...")
            elif self.currentText == "执行中..." or self.currentText == "Run":
                self.runStatus.emit("执行中.. ")
            time.sleep(0.5)

class runResultThread(QThread):
    '''
    免费试执行的自定义线程
    作用：自动报名免费试，生成表格、并微信推送报名结果
    '''
    runResult = pyqtSignal()    # 自定义信号
    def __init__(self, cookie, userNickName=None, city=None, cityId=None):
        super().__init__()
        self.Cookie = cookie
        self.userNickName = userNickName
        self.City = city
        self.CityId = cityId
        self.Rows = {
            '序号': 'No.',    # 自定义
            '活动名称': 'activityTitle',
            '活动链接': 'detailUrl',
            '活动类型': 'mode',
            '活动商圈': 'regionName',
            '报名开始时间': 'applyStartTime',    # 自定义
            '报名结束时间': 'applyEndTime',    # 自定义
            '活动名额': 'activityCount',    # 自定义
            '报名人数': 'applyCount',    # 自定义
            '中奖率（%）': 'winningRate',    # 活动名额/报名人数*100
            '关注人数': 'attentionCount',    # 自定义
            '活动开始时间': 'activityStartTime',    # 自定义
            '活动结束时间': 'activityEndTime',    # 自定义
            '活动地址': 'activityAddress',    # 自定义
            '剩余PASS次数': 'passCount',    # 自定义
            '报名结果': 'applyResult',    # 自定义
        }
        self.Database = {}

    def run(self):
        '''
        run()重写
        '''
        # type = {
        #     1: '美食',
        #     2: '丽人',
        #     3: '婚假',
        #     4: '亲子',
        #     5: '家装',
        #     6: '玩乐',
        #     7: 'N/A',
        #     8: '培训',
        #     9: 'N/A',
        # }
        mode = {
            1: '聚会',
            2: 'V聚会',
            3: '电子券',
            4: '好礼到家',
            5: '天天抽奖',
        }
        self.PASS = 0
        self.SKIP = 0
        self.FAIL = 0
        self.MESSAGE = ''
        count = 1
        self.MESSAGE += '-----开始报名霸王餐（免费试）-----\n\n'
        self.MESSAGE += ' - 城市：***{}***\n\n'.format(self.City)
        self.MESSAGE += '--------------------------------\n\n'
        activityTitles = self.getBaWangCanList()    # 获取霸王餐列表
        for _activity in activityTitles:
            self.Database[count] = {}
            for key in self.Rows.values():    # 部分Rows字段为自定义字段
                try:
                    if key != 'mode':
                        self.Database[count][key] = _activity[key]
                    else:
                        self.Database[count][key] = mode[_activity[key]]
                except:
                    self.Database[count][key] = ''
            # 霸王餐详情
            details = self.getBaWangCanDetail(_activity['detailUrl'])
            for key in self.Rows.values():
                try:
                    self.Database[count][key] = details[key]
                except:
                    pass
            # 霸王餐报名
            self.MESSAGE += '{}\n\n'.format(self.Database[count]['activityTitle'])
            offlineActivityId = _activity['detailUrl'].replace('http://s.dianping.com/event/', '')
            self.Database[count]['applyResult'] = self.runBaWangCan(offlineActivityId)
            self.MESSAGE += ' - 【报名结果】：{}\n\n'.format(self.Database[count]['applyResult'])
            self.Database[count]['No.'] = count
            count += 1
        self.MESSAGE += '-----今日成果预览-----\n\n'
        self.MESSAGE += '用户名：***{0}***\n\n- 今日报名成功：**{1}**\n\n- 今日报名重复：**{2}**\n\n- 今日报名异常：**{3}**'.format(self.userNickName, self.PASS, self.SKIP, self.FAIL)
        self.weixinTrap()    # 微信推送
        self.excelOperate()    # 表格生成
        self.runResult.emit()

    def getBaWangCanList(self):
        '''
        获取霸王餐列表
        '''
        detail = []
        url = 'http://m.dianping.com/activity/static/pc/ajaxList'
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        data = {
            'cityId': self.CityId,
            'mode': "",
            'page': 1,
            'type': 0,    # type：霸王餐类型
        }
        while True:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                hasNext = response.json()['data']['hasNext']
                detail += response.json()['data']['detail']
                if hasNext:    # 是否还有下一页列表
                    data['page'] += 1
                else:
                    break
            else:
                break
        return detail

    def getBaWangCanDetail(self, url):
        '''
        获取霸王餐详情
        '''
        detail = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            detail['activityAddress'] = re.search(r'活动地址：</span>\s+(.*)\s', response.text)[1]
            try:
                detail['applyStartTime'] = re.search(r'报名时间：</span>(\d+月\d+日).*(\d+月\d+日).*', response.text)[1]
                detail['applyEndTime'] = re.search(r'报名时间：</span>(\d+月\d+日).*(\d+月\d+日).*', response.text)[2]
            except:
                detail['applyStartTime'] = re.search(r'报名时间：</span>(\d+月\d+日).*', response.text)[1]
                detail['applyEndTime'] = ''
            try:
                detail['activityStartTime'] = re.search(r'活动时间：</span>(\d+月\d+日).*(\d+月\d+日).*</li>', response.text)[1]
                detail['activityEndTime'] = re.search(r'活动时间：</span>(\d+月\d+日).*(\d+月\d+日).*</li>', response.text)[2]
            except:
                detail['activityStartTime'] = re.search(r'活动时间：</span>(\d+月\d+日).*</li>', response.text)[1]
                detail['activityEndTime'] = ''
            detail['activityCount'] = re.search(r'活动名额：</span>\s+<strong class="col-digit">(\d+)</strong> 个', response.text)[1]
            try:
                detail['passCount'] = re.search(r'支持pass卡（剩余(\d+)个）', response.text)[1]
            except:
                detail['passCount'] = '不支持'
            detail['applyCount'] = re.search(r'<strong>(\d+)</strong>人报名', response.text)[1]
            detail['attentionCount'] = re.search(r'<strong>(\d+)</strong>人关注', response.text)[1]
            detail['winningRate'] = "{0:.2f}".format(int(detail['activityCount'])/int(detail['applyCount']) * 100)
        return detail
    
    def runBaWangCan(self, activatyID):
        '''
        报名霸王餐
        '''
        url = 'http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
            'Cookie': self.Cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        }
        data = {
            'offlineActivityId': activatyID,
            'phoneNo': '',
            'shippingAddress': '',
            'extraCount': '',
            'birthdayStr': '',
            'email': '',
            'marryDayStr': time.strftime('%Y-%m-%d'),
            'babyBirths': time.strftime('%Y-%m-%d'),
            'pregnant': '',
            'marryStatus': '0',
            'comboId': '',
            'branchId': '',
            'usePassCard': '0',
            'passCardNo': '',
            'isShareSina': 'false',
            'isShareQQ': 'false',
        }
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            msg = response.json()['msg']['html']
            if '报名成功' in msg:
                msg = '报名成功'
                self.PASS += 1
            elif '已经报过名了，不要重复报名' in msg:
                self.SKIP += 1
            else:
                self.FAIL += 1
        else:
            msg = '报名异常'
            self.FAIL += 1
        return msg

    def weixinTrap(self):
        '''
        微信推送
        '''
        # 从http://sc.ftqq.com/?c=code获取微信推送的SCKEY，并绑定官微
        SCKEY = 'SCU155771T3549c0427011a83c02d53a4f054055166012211d21350'    # Server酱申请的SCKEY
        url = 'https://sc.ftqq.com/{}.send'.format(SCKEY)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',}
        data = {
            'text': '大众点评免费试运行结果',
            'desp': self.MESSAGE,
        }
        requests.post(url=url, headers=header, data=data)

    def excelOperate(self):
        '''
        表格数据写入，并保存为.xlsx文件
        return : Excel表格
        '''
        excel = Workbook()
        sheet = excel.active    # 激活表格
        sheet.append(list(self.Rows.keys()))   # 写入首行数据
        for member in self.Database.values():
            sheet.append(list(member.values()))
        excel.save("大众点评免费试报名结果" + time.strftime('%Y-%m-%d %H`%M`%S') + ".xlsx")