# !/usr/bin/dev python
# coding=utf-8
import pexpect

def sshclient_execmd():
    usr='xxxxxx'
    ip ='xxxxxx'
    pwd ='xxxxxx'
    cmd ='ls'
    client = pexpect.spawn('ssh %s@%s "%s"' % (usr, ip, cmd), timeout=10)
    index=client.expect(['password: ', pexpect.TIMEOUT, pexpect.EOF])
    if index ==0:
        print str(0)
        client.sendline(pwd)
        client.expect(pexpect.EOF)
        # 输出命令结果.
        print client.before
    elif index ==2:
        print "EOF"
        client.close()
    elif index ==1:
        print "TIMEOUT"
        client.close()
        


if __name__ == '__main__':
    sshclient_execmd()

