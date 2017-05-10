# !usr/bin/python
# -*- coding:UTF-8 -*-

#apply()
def sum(x=1, y=2):
	return x + y
print apply(sum,(3,4)) #参数个数要和function中参数个数一致

#filter()，筛选的作用
def func(x):
	if x >0:
		return x
print filter(func, range(-9,10))

#reduce(),累计的作用
print reduce(sum, range(0,10))
print reduce(sum, range(0,10),10)
print reduce(sum, range(0,0),10)
print reduce(sum, (3,4,5))

#map(),列表进行重复的操作
def power(x): return x ** x
print map(power, range(1, 5))
def power1(x,y): return x ** y
print map(power1, range(1, 5), range(5, 1, -1))

print

#bool()判断
print bool(0)
print bool(1)

#buffer(),取字符，不能反向
print buffer("abcde",1,3)
print buffer("adbde",0, 5)

#cmp(),比较函数，小于=-1，相等=0，大于=1
print cmp(0, 1)
print cmp("c", "a")
print cmp("a", "a")

#coerce(),对参数进行组合，返回元祖
print coerce(1, 2)

#zip()打包生成元组
print zip((1, 2), (3, 4))
print zip((1, 2), (1, 2), (1, 2))
#错误如下,前后相对比的元组的元素个数要相同
#print zip((1,2,3),(1,2)) 

