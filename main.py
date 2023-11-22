import requests
from lxml import etree
import json
import re
import openpyxl
from pymysql import *

class Get_data():

    def __init__(self):
        # 连接数据库            #ip                                 #mysql密码                #数据库密码         #数据库编码格式
        self.con_obj = connect(host='192.168.1.192', user='root', password='wennyaw14083', database="yiqing", charset='utf8')#flush privileges
        print('连接数据库成功')

        # 创建游标对象
        self.mysql_ = self.con_obj.cursor()

        # 创建news新闻表，用来保存数据
        sql = '''create table IF NOT EXISTS data(
        省份 varchar(50) NOT NULL,
        累计确诊 varchar(1000) NOT NULL,
        死亡 varchar(1000) NOT NULL,
        治愈 varchar(1000) NOT NULL,
        现有确诊 varchar(1000) NOT NULL,
        累计确诊增量 varchar(1000) NOT NULL,
        死亡增量 varchar(1000) NOT NULL,
        治愈增量 varchar(1000) NOT NULL,
        现有确诊增量 varchar(1000) NOT NULL
        )'''
        # 在py里执行sql语句,创建news新闻表
        self.mysql_.execute(sql)

    def get_time(self):
        # 目标url
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
        # 伪装请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36 '
        }
        # 发出get请求
        response = requests.get(url,headers=headers)
        # 获取更新时间
        time_in = re.findall('"mapLastUpdatedTime":"(.*?)"',response.text)[0] #国内疫情更新时间
        time_out = re.findall('"foreignLastUpdatedTime":"(.*?)"',response.text)[0] #国外疫情更新时间
        print('国内疫情更新时间为 '+time_in)
        print('国外疫情更新时间为 '+time_out)
        return time_in,time_out

    def parse_data(self):
        self.get_time()
        response = requests.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/")
        # 生成HTML对象
        html = etree.HTML(response.text)
        # 解析数据
        result = html.xpath('//script[@type="application/json"]/text()')[0]
        # 将json格式转换为python字典格式
        result = json.loads(result)
        # 以每个省的数据为一个字典
        data_in = result['component'][0]['caseList']
        for each in data_in:
            print(each)
            print("\n" + '*' * 20)

        data_out = result['component'][0]['globalList']
        for each in data_out:
            print(each)
            print("\n" + '*' * 20)

        # 将得到的数据写入excel文件
        # 创建一个工作簿
        wb = openpyxl.Workbook()
        # 创建工作表,每一个工作表代表一个area
        ws_in = wb.active
        ws_in.title = "国内疫情"
        title = ['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量']
        ws_in.append(title)
        for each in data_in:
            temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],each['confirmedRelative'], each['diedRelative'], each['curedRelative'],each['curConfirmRelative']]
            for i in range(len(temp_list)):
                if temp_list[i] == '':
                    temp_list[i] = '0'
            # print(temp_list)
            data = dict(zip(title,temp_list))
            print(data)
            keys = ', '.join(data.keys())
            values = ', '.join(['% s'] * len(data))
            sql2 = "INSERT INTO data({keys}) VALUES({values})".format(keys=keys,values=values)
            print(sql2)
            ws_in.append(temp_list)
            # 提交事务
            try:
                if self.mysql_.execute(sql2, tuple(data.values())):
                    print('Successful')
                    self.con_obj.commit()
            except Exception as e:
                print(e)
                self.con_obj.rollback()



        # 保存excel文件
        wb.save('./data.xlsx')
        # 关闭与数据库的连接
        self.mysql_.close()
        self.con_obj.close()

if __name__ == '__main__':

    data = Get_data()
    data.parse_data()
