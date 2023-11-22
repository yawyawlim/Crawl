import re
import  tkinter
from  tkinter import ttk  #导入内部包
import openpyxl
from tkinter import *
from PIL import ImageTk,Image

from main import Get_data

data = Get_data()
data.parse_data()

# 创建窗口
import requests

window = tkinter.Tk()
# 设置标题
window.title('全国疫情统计')
# 设置窗口大小
window.geometry("1050x500+40+30")  # x是字母x不是符号叉
shuju = []


image2 =Image.open(r'./tupian.png')
background_image = ImageTk.PhotoImage(image2)
w = background_image.width()
h = background_image.height()
window.geometry('%dx%d+0+0' % (w,h))

background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# 目标url
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
# 伪装请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36 '
}
# 发出get请求
response = requests.get(url, headers=headers)
# 获取更新时间
time_in = re.findall('"mapLastUpdatedTime":"(.*?)"', response.text)[0]  # 国内疫情更新时间
time_ = '国内疫情更新时间为' + str(time_in)
#添加标签
label = tkinter.Label(window,text =time_,fg='blue',anchor='w',font=('黑体',12),width=30,height=2)
label.place(x=50,y=40,width=280,height=35)

def data():
    global shuju
    # 表格
    tree = ttk.Treeview(window)
    tree.pack()
    # 定义列
    tree["columns"] = ("省份","累计确诊","死亡","治愈","现有确诊","累计确诊增量","死亡增量","治愈增量","现有确诊增量")
    tree.column("省份", width=85)  # 表示列,不显示
    tree.column("累计确诊", width=85)
    tree.column("死亡", width=85)
    tree.column("治愈", width=85)
    tree.column("现有确诊", width=85)
    tree.column("累计确诊增量", width=85)
    tree.column("死亡增量", width=85)
    tree.column("治愈增量", width=85)
    tree.column("现有确诊增量", width=85)
    # 设置表头
    tree.heading("省份",text="省份")  # 显示表头
    tree.heading("累计确诊",text="累计确诊")
    tree.heading("死亡",text="死亡")
    tree.heading("治愈",text="治愈")
    tree.heading("现有确诊",text="现有确诊")
    tree.heading("累计确诊增量",text="累计确诊增量")
    tree.heading("死亡增量",text="死亡增量")
    tree.heading("治愈增量",text="治愈增量")
    tree.heading("现有确诊增量",text="现有确诊增量")
    #插入数据
    wb = openpyxl.load_workbook('data.xlsx')
    ws = wb['国内疫情']
    # 按行读取内容转化为列表
    rows_data = list(ws.rows)
    for case in rows_data[1:]:
        data = []
        for cell in case:  # 获取单元格对象
            data.append(cell.value)
        data = tuple(data)
        shuju.append([data[0],data[4]])
        print(data)
        tree.insert("",0,text="",values=data)



#1按钮
button1 = tkinter.Button(window,text ='点击爬取全国疫情数据',bg='red',fg='black',command=data)
button1.pack()   # 把按钮添加到窗口中去

#2输入框
e1 = tkinter.Entry(window) # 把输入窗口加载到window里
e1.pack()


#3显示框
var = tkinter.StringVar()
b2 = tkinter.Label(window,textvariable=var)
b2.pack() # 把标签放到窗口上去
def  hit_me():
    data = []
    EN1 = e1.get()
    for i in shuju:
        if i[1] >EN1:
            data.append(i[0])
    var.set(','.join(data))


#4按钮
button = tkinter.Button(window,text ='现有确诊大于填入数字的省份并点击确定',bg='red',fg='black',command=hit_me)
button.pack()


# 进入消息循环，窗口持久化
window.mainloop()