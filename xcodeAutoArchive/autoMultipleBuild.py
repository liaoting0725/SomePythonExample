#coding=utf-8
#!usr/bin/python

import sys
import os
import shutil
import commands

#configuration for iOS build setting
CHANNEL_PLIST				 = 'Channel.plist'
PRODUCT_NAME				 = 'YangDongXi'
#赋值是否打Release包，是的话设True,Debug则设置成False
RELEASE_OR_NOT				 = False
#Release版本多渠道序列
RELEASE_CHANNEL_LIST         = ['AppStore','91','PP', 'KuaiYong','TongBuTui','iTools', 'XY','HAIMA', 'HULU']
#Debug版本多渠道序列，默认为iostest
DEBUG_CHANNEL_LIST			 = ['iostest']

DEBUG_XCODE_BUILD			 = 'xcodebuild -workspace YangDongXi.xcworkspace -scheme YangDongXi -configuration Debug -sdk iphoneos build CODE_SIGN_IDENTITY="iPhone Developer: Kangshuang Jin (284NRC8MDE)" PROVISIONING_PROFILE="7a6fb4f0-45a2-4ed9-869d-e98bd3c8294f"'

RELEASE_XCODE_BUILD			 = ''

#channel在工程中的路劲
CHANNEL_PATH         		 = 'MultiChannels'


# configuration for pgyer
#如果需要提交至蒲公英则需要设成True，反之设成False
UPLOAD_PGYER_NEED = False
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "15d6xxxxxxxxxxxxxxxxxx"
API_KEY = "efxxxxxxxxxxxxxxxxxxxx"


#打包机型，默认是真机打包
BUILD_SDK = "iphoneos"

def build(buildmode):
	print '编译中，请稍等...'
	status ,output = commands.getstatusoutput(buildmode)
	print output

def clean():
	status ,output = commands.getstatusoutput('xcodebuild clean')
	print output

# 替换文件
def replaceflies(channel):
	workspacepath = os.getcwd()
	srcpath = os.path.join(workspacepath, CHANNEL_PATH)
	srcpath = os.path.join(srcpath, channel)
	despath = os.path.join(workspacepath, PRODUCT_NAME)
	# 替换资源
	srcfullpath = os.path.join(srcpath, CHANNEL_PLIST)
	desfullpath = os.path.join(despath, CHANNEL_PLIST)
	print(channel)
	if os.path.exists(srcfullpath):
		if os.path.exists(desfullpath):
			shutil.copy(srcfullpath, desfullpath)
			print("Copy '" + srcfullpath + "' to '" + desfullpath + "'.")
		else :
			print("'" + desfullpath + "'" + '不存在')
	else :
		print("'" + srcfullpath + "'" + '不存在')


def xcbuild(argvs):
	if len(argvs) <1:
		print('至少输入一个渠道名称')
		return
	else :
		count = len(argvs)
		if RELEASE_OR_NOT:
			for i in xrange(0,count):
				channel = argvs[i]
				if not channel in RELEASE_CHANNEL_LIST:
					print('没有'+channel+'此渠道名称')
				else :
					return
		else :
			if count >1:
				print('Debug版本只有一个渠道号')
				return
			else :
				channel = argvs[0]
				if not channel in DEBUG_CHANNEL_LIST:
					print('Debug渠道列表没有该渠道'+channel)
				else :
					#先替换channel.plist文件，打渠道包
					replaceflies(channel)
					# clean
					clean()

					
					# 编译
					if RELEASE_OR_NOT:
						return
					else :
						build(DEBUG_XCODE_BUILD)

if __name__ == '__main__':
	buildlist = ['iostest']
	xcbuild(buildlist)

