# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import time, threading, random, requests, json, paramiko

#十六进制个数
hex_dict = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

#取platform的进程号，可以使用其他的telnet工具代替
def get_platform_pid():
    paramiko.util.log_to_file('paramiko_wifidog.log')
    s = paramiko.SSHClient()
    #s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname='192.168.11.1', port=22, username='root', password='xxxxxxxxxxxx')
    stdin, stdout, stderr = s.exec_command('ps | grep platform | grep -v grep')
    return_content = stdout.read()
    s.close()
    return return_content.strip().split(" ")[0]

#取wifidog的进程号，可以使用其他的telnet工具代替
def get_wifidog_pid():
    paramiko.util.log_to_file('paramiko_wifidog.log')
    s = paramiko.SSHClient()
    #s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname='192.168.11.1', port=22, username='root', password='xxxxxxxxxxxx')
    stdin, stdout, stderr = s.exec_command('ps | grep wifidog | grep -v grep')
    return_content = stdout.read()
    s.close()
    return return_content.strip().split(" ")[0]

#发送认证消息的函数，route_mac为路由器的mac，m为线程的编号
def push_auth_pass_info(route_mac, m):
    i, j = 0, 0
    while True:
        # 下面的一大段是为了组织认证的json消息（随机ID，随机用户mac，随机token值）
        ID = random.randint(10000001, 99999999)
        mac_list = ''
        for x in range(12):
            mac_list = mac_list + random.choice(hex_dict)
        user_mac = mac_list[0:2]+':'+mac_list[2:4]+':'+mac_list[4:6]+':'+mac_list[6:8]+':'+mac_list[8:10]+':'+mac_list[10:12]
        token = ''
        for y in range(32):
            token = token + random.choice(hex_dict)
        user_info = {"ID": ID, "Type":1, "Callback":"", "CommandList":[{"Command": "TerminalManagement","CommandID": "","CommandTarget": route_mac,"ParameterList":[{"Type":"pass","Mac":user_mac,"Token":token}]}]}
        r = requests.post("http://xxxxxxxx:9999/cloud/command?token=xxx", json=user_info)
        if r.status_code == 200 and str(ID) in json.dumps(r.text) and "SUCCESS" in json.dumps(r.text):
            i += 1
            print u"第%d号线程下发认证通过消息成功,成功次数%d，时间%s..." % (m, i, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #发包间隔可以自己调节，这里是每隔2s发送一次
            time.sleep(2)
        else:
            j += 1
            print u"第%d号线程下发认证通过消息成功,失败次数%d，时间%s..." % (m, j, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print r.text
            time.sleep(2)
    f = open('auth_info.txt', 'ab')
    f.write('第%d号线程：成功%d, 失败%d\n' % (m, i, j))
    f.close()

if __name__ == "__main__":
    #此mac为路由器的mac
    mac = "84:82:f4:22:6e:c8"
    #脚本开始时，记录platform和wifidog的进程号
    start_platform_pid = get_platform_pid()
    start_wifidog_pid = get_wifidog_pid()
    print u"脚本开始前，platform和wifidog的进程为%s, %s" % (start_platform_pid, start_wifidog_pid)
    #起5个线程，每个线程分别给路由器发送认证通过的消息,想要起几个线程，就把下面的5改成某个数字
    threads = []
    for m in range(5):
        thread = threading.Thread(target=push_auth_pass_info, args=(mac, m))
        threads.append(thread)
    for m in range(5):
        threads[m].start()
    for m in range(5):
        threads[m].join()
    #当5个线程都退出的时候（当一个线程发送认证通过消息失败次数达到n次时，线程就退出），记录此时platform和wifidog的进程号
    end_platform_pid = get_platform_pid()
    end_wifidog_pid = get_wifidog_pid()
    print u"脚本结束后，platform和wifidog的进程为%s, %s" % (end_platform_pid, end_wifidog_pid)
    #做进程号的记录
    f = open('auth_info.txt', 'ab')
    f.write("脚本开始前，platform和wifidog的进程为%s, %s\n" % (start_platform_pid, start_wifidog_pid))
    f.write("脚本结束后，platform和wifidog的进程为%s, %s\n" % (end_platform_pid, end_wifidog_pid))
    f.close()