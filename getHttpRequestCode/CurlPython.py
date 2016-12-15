# !/usr/bin/dev python
# coding=utf-8
import subprocess

net = 'http://www.baidu.com'
url = 'curl --connect-timeout 10 -m 20 -s -w %{http_code} -o /dev/null ' + net
result = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
c = result.stdout.readline()
print c
if c == '200':
	print 'status ok'
else:
	print 'status error'