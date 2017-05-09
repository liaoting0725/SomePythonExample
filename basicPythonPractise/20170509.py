# !/usr/bin/python
# -*- coding:UTF-8 -*-

print "%s, %(a)s, %(b)s" %{"a":"apple","b":"banana"}


list0 = [1,2,3,4,5,4,3,2,1,0]
list1 = [1,2,3]
list2 = [i for i in list0 if i not in list1]
list3 = []
list3 = [i for i in list0 if i not in list3]
print list2
print list3


tuple = (('apple','banana'),('grape','orange'),('watermelon',),('grapefruit',))
for i in range(len(tuple)):
	print "tuple[%d]:" %i,"",
	for j in range(len(tuple[i])):
		print tuple[i][j],"",
	print



k =0
for a in map(None, tuple):
	print "tuple[%d]:"%k,"",
	for x in a:
		print x,"",
	print
	k+=1



