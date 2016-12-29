# !usr/bin/env python
# coding:utf-8

#两次遍历循环，在第一层遍历的位置遍历之后的列表
def del_all_same_element_in_list_mothod1(arg=None):
    if isinstance(arg, list):
        repeat_list = []
        simple_list = []
        for index in xrange(len(arg)):
            x = arg[index]
            if x in repeat_list:
                continue
            else:
                same = False
                for value in arg[index+1:]:
                    if x == value:
                        repeat_list.append(value)
                        same = True
                        break
                    else:
                        pass
                if not same:
                    simple_list.append(x)
        print 'repeat_list'
        print repeat_list
        print 'simple_list'
        print simple_list
    else:
        print 'input element is not list type'

#将列表排序，遍历列表时，判断当前值和last_item不同时，获取当前值在列表中的个数
def del_all_same_element_in_list_mothod2(arg=None):
    if isinstance(arg, list):
        simple_list = []
        repeat_list = []
        arg_sorted = sorted(arg)
        last_item = ''
        for x in arg_sorted:
            if x != last_item:
                if arg.count(x) == 1:
                    simple_list.append(x)
                else:
                    repeat_list.append(x)
                last_item = x
        print 'repeat_list'
        print repeat_list
        print 'simple_list'
        print simple_list
    else:
        print 'input element is not list type'

if __name__ == '__main__':
    arg = [1, 2, 3, 4, 1, 23, 4, 2, 1, 'str', 'str', 'string', 'string1']
    del_all_same_element_in_list_mothod2(arg)