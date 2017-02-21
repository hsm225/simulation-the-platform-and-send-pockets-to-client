# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import time, threading, random, paramiko
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

hex_dict = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

def push_auth_pass_info(route_mac, m):
    i, j = 1, 1
    driver = webdriver.Firefox()
    while j <= 5:
        driver.get('http://xxxxxxxxxx:9999/static/index.html')
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/input[2]').clear()
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/textarea[1]').clear()
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/textarea[3]').clear()
        time.sleep(1)
        mac_list = ''
        for x in range(12):
            mac_list = mac_list + random.choice(hex_dict)
        user_mac = mac_list[0:2]+':'+mac_list[2:4]+':'+mac_list[4:6]+':'+mac_list[6:8]+':'+mac_list[8:10]+':'+mac_list[10:12]
        print user_mac
        token = ''
        for y in range(32):
            token = token + random.choice(hex_dict)
        print token
        send_info = '{"Command": "TerminalManagement","CommandID": "","CommandTarget": "%s","ParameterList":[{"Type":"pass","Mac":"%s","Token":"%s"}]}' % (route_mac, user_mac, token)
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/input[2]').send_keys(route_mac)
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/textarea[1]').send_keys(send_info)
        driver.find_element_by_xpath('html/body/div[1]/div/div[2]/button[1]').click()
        time.sleep(3)
        if '"Status": "SUCCESS"' in str(driver.find_element_by_xpath('html/body/div[1]/div/div[2]/textarea[3]').get_attribute('value')):
            print u"第%d号线程消息发送成功，成功次数%d..." % (m, i)
            i += 1
            time.sleep(3)
        else:
            print u"第%d号线程消息发送失败，失败次数%d..." % (m, j)
            j += 1
            time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    mac = '84:82:f4:22:6e:c8'
    threads = []
    for m in range(5):
        thread = threading.Thread(target=push_auth_pass_info, args=(mac, m))
        threads.append(thread)
    for m in range(5):
        threads[m].start()

    for m in range(5):
        threads[m].join()