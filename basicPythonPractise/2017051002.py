# !usr/bin/python
# -*- coding:UTF-8 -*-

from __future__ import division

def append(args=[]):
	if len(args) <=0:
		args = []
	args.append(0)
	print args

append()
append([1])
append()

#下面定义的函数类似于c中的switch方法，通过字典来实现
def switch(x=1, y=1, operator="+"):
	result = {
		"+" : x + y,
		"-" : x - y,
		"*" : x * y,
		"/" : x / y
	}
	return result.get(operator)

print switch(1, 2)
print switch(1, 2, operator="-")
print switch(y=2, operator="/")


def switch(args=[], operator="+"):
	x = args[0];y = args[1]
	result = {
		"+" : x + y,
		"-" : x - y,
		"*" : x * y,
		"/" : x / y
	}
	return result.get(operator)

print switch([1,2])

# *t表示列表， **d表示字典
def search(*t, **d):
	keys = d.keys()
	value = d.values()
	print keys
	print value
	for arg in t:
		for key in keys:
			if arg == key:
				print "find:",d[key]

search("one", "two",one="1",two="2",three="3")


#lambda
def func():
	x = 1; y = 2; m = 3; n = 4
	sum = lambda x,y : x + y
	print sum
	sub = lambda m,n : m - n
	print sub
	return sum(x,n) *sub(y,m)
print func()

print (lambda x: -x)(-2)
print (lambda x,y:[x,y])(1,2)