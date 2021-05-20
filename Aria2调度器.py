'''
Author: Aria2调度器 V0.1
Date: 2021-05-19 14:24:27
LastEditTime: 2021-05-20 13:13:47
LastEditors: Please set LastEditors
Description: 利用WinSW程序辅助调用Aria2程序
FilePath: \Aria2调度器.py
'''
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import os
import re
import subprocess
import ctypes
import sys
import threading
import time
import requests
from requests.models import Response

Path = "./"  # 当前相对路径
# 匹配Aria2、Aria2c、aria2、aria2c
Aria2Regex = "[a|A]+ria2[c]?"
Aria2PathRegex = Aria2Regex + ".exe"
Aria2ConfRegex = Aria2Regex + ".conf"
WinswPathRegex = "([a|A]+ria2[c]?[-])?([w|W]in[s|S][w|W]).exe"


# 翻译
translate = {
    'Started': '已启动',
    'Stopped': '已停止',
    'NonExistent': '已卸载'
}

# COMMAND
services = ['start', 'stop', 'restart', 'install', 'uninstall', 'status']
cmds = None

# iCON


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def _init():
    global cmds, check
    if(isAdmin()):
        files = os.listdir(Path)
        for file in files:
            if re.match(Aria2PathRegex, file):
                print("匹配到Aria2程序")
                int_checkAria2.set(1)
            if re.match(Aria2ConfRegex, file):
                print("匹配到Aria2配置文件")
                int_checkConf.set(1)
            if re.match(WinswPathRegex, file):
                print("匹配到WinSW程序")
                int_checkWinSW.set(1)
                winswPath = os.path.abspath(file)
                cmds = [[winswPath, service] for service in services]
                threading.Thread(target=whileStatus, daemon=True).start()
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def checkAria2_mouseenter(*arg):
    print("CheckAria2鼠标进入")


def checkAria2_keydown(*arg):
    int_checkAria2.set(not int_checkAria2.get())


def checkConf_mouseenter(*arg):
    print("CheckConf鼠标进入")


def checkConf_keydown(*arg):
    int_checkConf.set(not int_checkConf.get())


def checkWinSW_mouseenter(*arg):
    print("CheckWinSW鼠标进入")


def checkWinSW_keydown(*arg):
    int_checkWinSW.set(not int_checkWinSW.get())


def repair(*arg):
    strs = ['Aria2主程序', 'winsw辅助程序', 'Aria2配置文件']
    methods = ['https://gitee.com/acg-q/miscellaneous/raw/master/Aria2/aria2c.exe',
               ['https://gitee.com/acg-q/miscellaneous/raw/master/Aria2/aria2-winsw.exe',
                'https://gitee.com/acg-q/miscellaneous/raw/master/Aria2/aria2-winsw.xml'
                ],
               'https://gitee.com/acg-q/miscellaneous/raw/master/Aria2/aria2.conf'
               ]
    intVars = [int_checkAria2, int_checkWinSW, int_checkConf]
    list = [x.get() for x in intVars]
    if(0 in list):
        sun = list.count(0)
        print(f'需要修复{sun}项')
        try:
            for i in range(sun):
                coordinate = list.index(0)
                print(f"正在修复: {strs[coordinate]}")
                if(coordinate == 1):
                    for j in methods[coordinate]:
                        response = requests.get(j)
                        _, filename = os.path.split(j)
                        with open(filename, mode='wb') as f:
                            f.write(response.content)
                else:
                    response = requests.get(methods[coordinate])
                    _, filename = os.path.split(methods[coordinate])
                    with open(filename, mode='wb') as f:
                        f.write(response.content)
                # 修复成功
                list.pop(coordinate)
                list.insert(coordinate, 1)
            msg.showinfo('成功', '修复成功')
        except:
            msg.showerror('失败', '修复失败')
        _init()
    else:
        msg.showinfo('提示', '暂无需要修复的项目')


def start(*arg):
    if(checkStatus['text'] == '已停止'):
        command = subprocess.Popen(cmds[0],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = command.communicate()
        print(stdout, stderr)

    else:
        msg.showerror('启动失败', f'启动条件不足，Aria2当前状态{checkStatus["text"]}')


def stop(*arg):
    if(checkStatus['text'] == '已启动'):
        command = subprocess.Popen(cmds[1],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = command.communicate()
        print(stdout, stderr)
    else:
        msg.showerror('停止失败', f'停止条件不足，Aria2当前状态{checkStatus["text"]}')


def restart(*arg):
    if(checkStatus['text'] == '已启动' or checkStatus['text'] == '已停止'):
        command = subprocess.Popen(cmds[2],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = command.communicate()
        print(stdout, stderr)
    else:
        msg.showerror('重启失败', f'重启条件不足，Aria2当前状态{checkStatus["text"]}')


def install(*arg):
    if(checkStatus['text'] == '已卸载'):
        command = subprocess.Popen(cmds[3],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = command.communicate()
        print(stdout, stderr)
    else:
        msg.showerror('安装失败', f'安装服务条件不足，Aria2当前状态{checkStatus["text"]}')


def uninstall(*arg):
    if(checkStatus['text'] == '已停止'):
        command = subprocess.Popen(cmds[4],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = command.communicate()
        print(stdout, stderr)
    else:
        msg.showerror('卸载失败', f'卸载服务条件不足，Aria2当前状态{checkStatus["text"]}')


def status(*arg):
    command = subprocess.Popen(cmds[5],
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    stdout, stderr = command.communicate()
    checkStatus['text'] = translate[str(stdout.decode(
        'utf-8')).replace('\r', '').replace('\n', '')]


def whileStatus():
    while(1):
        if(cmds[5]):
            status()
        time.sleep(1)


root = tk.Tk()  # 设定窗体变量
if(not isAdmin()):
    _init()

root.geometry('250x210')  # 格式('宽x高+x+y')其中x、y为位置
root.title('Aria2调度器')
root.iconbitmap("./image/aria2.ico")


multiPage1 = ttk.Notebook(root)
# 标签内的组件需要把Page1作为父变量，其位置则为标签的相对位置
page1 = ttk.Frame(multiPage1)
multiPage1.add(page1, text='操纵器')
# 标签内的组件需要把Page2作为父变量，其位置则为标签的相对位置
page2 = ttk.Frame(multiPage1)
multiPage1.add(page2, text='Aria2资源下载')
multiPage1.place(x=5, y=5, width=240, height=200)

frame1 = ttk.LabelFrame(page1, text='程序检测项')
frame1.place(x=5, y=5, width=223, height=100)

frame2 = ttk.LabelFrame(page1, text='Aria2启动/停止')
frame2.place(x=5, y=110, width=120, height=60)

frame3 = ttk.LabelFrame(page1, text='服务')
frame3.place(x=144, y=110, width=84, height=60)

int_checkAria2 = tk.IntVar()  # 绑定变量
checkAria2 = tk.Checkbutton(
    frame1, text='检测Aria2主程序', variable=int_checkAria2, font=('宋体', '9'))
checkAria2.place(x=7, y=7, height=22)  # 考虑到对齐问题，不列入宽度，需要时手动加入 width=130
checkAria2.bind("<Enter>", checkAria2_mouseenter)
checkAria2.bind("<Button-1>", checkAria2_keydown)
checkAria2.deselect()  # 默认为未选中状态

int_checkWinSW = tk.IntVar()  # 绑定变量
checkWinSW = tk.Checkbutton(
    frame1, text='检测winsw辅助程序', variable=int_checkWinSW, font=('宋体', '9'))
checkWinSW.place(x=7, y=29, height=22)  # 考虑到对齐问题，不列入宽度，需要时手动加入 width=130
checkWinSW.bind("<Enter>",  checkConf_mouseenter)
checkWinSW.bind("<Button-1>", checkWinSW_keydown)
checkWinSW.deselect()  # 默认为未选中状态

int_checkConf = tk.IntVar()  # 绑定变量
checkConf = tk.Checkbutton(
    frame1, text='检测Aria2配置文件', variable=int_checkConf, font=('宋体', '9'))
checkConf.place(x=7, y=50, height=22)  # 考虑到对齐问题，不列入宽度，需要时手动加入 width=130
checkConf.bind("<Enter>", checkConf_mouseenter)
checkConf.bind("<Button-1>", checkConf_keydown)
checkConf.deselect()  # 默认为未选中状态

checkStatus = tk.Label(
    frame1, text='winsw状态', font=('宋体', '9'))
# 考虑到对齐问题，不列入宽度，需要时手动加入 width=130
checkStatus.place(x=150, y=29, height=22)
# checkConf.bind("<Enter>", checkConf_mouseenter)
checkStatus.bind("<Button-1>", status)


# 可在括号内加上调用函数部分 ,command=buttonRepair_clicked
buttonRepair = tk.Button(frame1, text='修复', font=('宋体', '9'), command=repair)
buttonRepair.place(x=144, y=50, width=65, height=22)
# buttonRepair.bind("<Button-1>", repair)

# 可在括号内加上调用函数部分 ,command=buttonStop_clicked
buttonStop = tk.Button(frame2, text='E', font=('宋体', '9'), command=stop)
# image=tk.PhotoImage(file="image/重启.png")
buttonStop.place(x=43, y=7, width=29, height=29)
# buttonStop.bind("<Button-1>", stop)

# 可在括号内加上调用函数部分 ,command=buttonStart_clicked
buttonStart = tk.Button(frame2, text='S', font=('宋体', '9'), command=start)
buttonStart.place(x=7, y=7, width=29, height=29)
# buttonStart.bind("<Button-1>", start)

# 可在括号内加上调用函数部分 ,command=buttonRestart_clicked
buttonRestart = tk.Button(frame2, text='R', font=('宋体', '9'), command=restart)
buttonRestart.place(x=79, y=7, width=29, height=29)
# buttonRestart.bind("<Button-1>", restart)

# 可在括号内加上调用函数部分 ,command=buttonInstall_clicked
buttonInstall = tk.Button(frame3, text='I', font=('宋体', '9'), command=install)
buttonInstall.place(x=7, y=7, width=29, height=29)
# buttonInstall.bind("<Button-1>", install)

# 可在括号内加上调用函数部分 ,command=buttonUninstall_clicked
buttonUninstall = tk.Button(
    frame3, text='U', font=('宋体', '9'), command=uninstall)
buttonUninstall.place(x=43, y=7, width=29, height=29)
# buttonUninstall.bind("<Button-1>", uninstall)

textBox1 = tk.Text(page2, font=('宋体', '9'))

textBox1.place(x=7, y=7, width=216, height=120)
textBox1.insert(
    tk.END, 'Aria2下载地址：https://github.com/aria2/aria2/releases/latest\nWinSW下载地址：https://github.com/winsw/winsw/releases/latest\n\n作者：吾爱论坛 By六记')
textBox1.configure(state='disabled')
_init()
root.mainloop()
