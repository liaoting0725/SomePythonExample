# !/usr/bin/dev python
# coding:utf-8
from CfgManager import *
import Schedu
import Email
import SmsAlidayu
import paramiko
import threading

global manager
manager = CfgManager('Linux.cfg')

class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        threadLock.acquire()
        hostname = manager.getValue(sectionHeader=self.name, key='hostname')
        port = manager.getIntValue(sectionHeader=self.name, key='port')
        username = manager.getValue(sectionHeader=self.name, key='username')
        password = manager.getValue(sectionHeader=self.name, key='password')
        all_info(hostname=hostname, port=port, username=username, password=password, obsever_name=self.name)
        threadLock.release()

threadLock = threading.Lock()

def cpuUsage(sshclient):
    try:
        stdin, stdout, stderr = sshclient.exec_command('cat /proc/stat')
        lines = stdout.readlines()
        for line in lines:
            line = line.lstrip()
            counters = line.split()
            if len(counters) < 5:
                continue
            if counters[0].startswith('cpu'):
                break
        total = 0
        for i in xrange(1, len(counters)):
            total += long(counters[i])
        idle = long(counters[4])
        return 100 - (idle * 100 / total)
    except Exception as e:
        print '错误原因:' + str(e)
        return 0


def memUsage(sshclient):
    res = {'total': 0, 'free': 0, 'buffers': 0, 'cached': 0}
    try:
        stdin, stdout, stderr = sshclient.exec_command('cat /proc/meminfo')
        lines = stdout.readlines()
        i = 0
        for line in lines:
            if i == 4:
                break
            line = line.lstrip()
            memitem = line.lower().split()
            i += 1
            if memitem[0] == 'memtotal:':
                res['total'] = long(memitem[1])
                continue
            elif memitem[0] == 'memfree:':
                res['free'] = long(memitem[1])
                continue
            elif memitem[0] == 'buffers:':
                res['buffers'] = long(memitem[1])
                continue
            elif memitem[0] == 'cached:':
                res['cached'] = long(memitem[1])
                continue
        used = res['total'] - res['free'] - res['buffers'] - res['cached']
        total = res['total']
        return used * 100 / total
    except Exception as e:
        print '错误原因:' + str(e)
        return 0


def diskInfo(sshclient):
    global manager
    diskStnd = manager.getIntValue(sectionHeader='setup', key='disk')
    stdin, stdout, stderr = sshclient.exec_command('df -lh')
    lines = stdout.readlines()
    length = len(lines)
    errorstring = ''
    if length > 1:
        for i in range(1, length):
            mes = lines[i]
            meslist = mes.split()
            submes = meslist[4]
            num = float(submes[:-1])
            if num > diskStnd:
                errorstring = '磁盘占用过多'
                break
    return errorstring


def all_info(hostname=None, port=22, username=None, password=None, obsever_name=None):
    error = False
    #ssh remote here
    s = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    s.set_missing_host_key_policy(policy)
    try:
        s.connect(hostname=hostname, port=port, username=username, password=password, timeout=20)
        global manager
        cpuStnd = manager.getIntValue(sectionHeader=obsever_name, key='cpu')
        memStnd = manager.getIntValue(sectionHeader=obsever_name, key='mem')
        error_string = diskInfo(sshclient=s)
        if len(error_string):
            error = True
        mem = memUsage(sshclient=s)
        if mem > memStnd or mem == 0:
            error = True
            error_string += '内存占用过多,'
        cpu = cpuUsage(sshclient=s)
        if cpu > cpuStnd or cpu == 0:
            error = True
            error_string += 'cpu占用过多'
        print(error_string)
    except Exception as e:
        error = True
        error_string = e
        print(error_string)
    finally:
        s.close
        curTime = manager.getIntValue(sectionHeader=obsever_name, key='curtime')
        first_time = manager.getValue(sectionHeader=obsever_name, key='first_time')
        if error:
            curTime += 1
            maxTime = manager.getIntValue(sectionHeader=obsever_name, key='maxtime')
            if curTime >= maxTime:
                curTime = 0
                notice(error_string=error_string, error=True, obsever_name=obsever_name)
            else:
                pass
            manager.setValue(sectionHeader=obsever_name, key='curtime', value=curTime)
        else:
            if first_time:
                notice(error=False, obsever_name=obsever_name)
            manager.setValue(sectionHeader=obsever_name, key='curtime', value=0)
        manager.setValue(sectionHeader=obsever_name, key='first_time', value=False)


def notice(error_string=None, error=False, obsever_name=None):
    email_to_addr = manager.getValue(sectionHeader=obsever_name, key='emailto')
    sms_to_addr = manager.getValue(sectionHeader=obsever_name, key='smsto')
    subject_name = obsever_name +'服务器检测'
    if error:
        email_content = error_string
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=True, message=email_content)
    else:
        email_content = subject_name + '恢复正常'
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=False)


def action():
    global manager
    apps = manager.getSections()
    appsNum = len(apps)
    if appsNum:
        for i in xrange(0, appsNum):
            section = apps[i]
            if section == 'setup':
                pass
            else:
                thread = myThread(name=section)
                thread.setDaemon(True)
                thread.start()


def reset():
    apps = manager.getSections()
    apps_num = len(apps)
    if apps_num:
        for i in xrange(0, apps_num):
            section = apps[i]
            if section == 'setup':
                pass
            else:
                manager.setValue(sectionHeader=section, key='curtime', value=0)
                manager.setValue(sectionHeader=section, key='first_time', value=True)


if __name__ == '__main__':
    reset()
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(action, second=time)
