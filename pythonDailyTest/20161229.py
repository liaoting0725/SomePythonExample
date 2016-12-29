# !usr/bin/env python
# coding:utf-8
# 从键盘输入一个字符串，统计出该字符串中出现的字母及对应个数。

def letter_count_method(str):
    result_dict = {}
    # 分割字符串
    letter_list = list(str)
    # 列表排序
    letter_list.sort()
    # 设置比较默认值
    last_item = ''
    for x in letter_list:
        # 判断是否和默认值相同并且是字母
        if x != last_item and x.isalpha():
            count = letter_list.count(x)
            # 填充字典
            result_dict[x] = count
            # 重置比较默认值
            last_item = x
    return result_dict


if __name__ == '__main__':
    input_string = raw_input('请输入字符串:\n')
    result_dict = letter_count_method(input_string)
    print result_dict