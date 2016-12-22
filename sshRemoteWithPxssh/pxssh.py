#!/usr/bin/env python
import pexpect.pxssh
import os
def action():
    try:
        s = pexpect.pxssh.pxssh()
        hostname='xxxxxxx'
        username='xxxxxxx'
        password='xxxxxxx'
        port=xxxxxxx
        s.login(hostname=hostname, username=username, password=password, port=port)
        s.sendline('cat /proc/meminfo')
        s.prompt()
        result_str=s.before
        parse_result(result_str)
        s.sendline('df -lh')
        s.prompt()
        result_str1=s.before
        parse_result(result_str1)
    except Exception, e:
        print e

def parse_result(str):
    list=[x for x in str.split('\r\n')]
    list.pop(0) #去除分割出来的命令行显示
    for sub in list:
        print sub

if __name__ == '__main__':
        action()





