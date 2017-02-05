# !/usr/bin/env python
# coding: utf-8

import datetime
import hmac
import uuid
from hashlib import sha1
import sys
import urllib
import urllib2
import base64
import json

def get_utctime():
    # 获取现在时间的iso8601时间标准格式输出
    dtnow = datetime.datetime.utcnow()
    now_time = dtnow.strftime(format="%Y-%m-%dT%H:%M:%SZ")
    return now_time

def get_signature(parameters):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0]) # 排列顺序
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])  # 使用get请求方法
    h = hmac.new(yourAccessSecret + "&", stringToSign, sha1) # sha1加密
    signature = base64.encodestring(h.digest()).strip() # base64处理
    return signature


def percent_encode(encodeStr): #utf8编码
    encodeStr = str(encodeStr)
    res = urllib.quote(encodeStr.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def make_url(params=None):
    timestamp = get_utctime()
    parameters = {
        'Format': 'JSON',
        'Version': '2014-05-26',
        'AccessKeyId': yourAccessKeyId,
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'Timestamp': timestamp
    }
    for key in params.keys():
        parameters[key] = params[key]
    signature = get_signature(parameters)
    parameters['Signature'] = signature
    url = 'https://ecs.aliyuncs.com' + "/?" + urllib.urlencode(parameters)
    return url

def do_request(params):
    url = make_url(params)
    request = urllib2.Request(url)
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        raise SystemExit(e)
    try:
        obj = json.loads(response)
    except ValueError, e:
        raise SystemExit(e)
    print obj

if __name__ == '__main__':
    do_request({"Action": "ModifyEipAddressAttribute", 'AllocationId': yourAllocationId, 'Bandwidth': yourBandwidth})

