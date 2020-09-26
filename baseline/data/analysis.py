#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_loader
# @Author   : 张志毅
# @Time     : 2020/9/12 19:14
import json
from random import shuffle

from baseline.config.config import config
import matplotlib.pyplot as plt

def get_lengths(path = config.train_path):
    texts = []
    with open(path, 'r', encoding='utf-8') as f:

        lines = f.readlines()
        for line in lines:

            line = line.split('|||', 1)
            text = line[0]
            if len(text)>300:
                print(line)
                print(len(text))
            texts.append(len(text))
    f.close()
    sen_in_inter = []
    interval = 20
    min_len = min(texts)
    max_len = max(texts)
    print(max_len)
    start = min_len // interval * interval
    interval_num = max_len // interval - min_len // interval + 1
    for i in range(interval_num):
        sen_in_inter.append(0)
    for i in range(len(texts)):
        sen_in_inter[(texts[i] - start) // interval] += 1
    print('区间个数：{}   每个区间数目：{}'.format(interval_num, sen_in_inter))
    print("区间为：", end='')
    x_names = []
    for i in range(interval_num):
        x_names.append('{}-{}'.format(start + interval * i, start + interval * (i + 1) - 1))
    print(x_names)

    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    bar_width = 0.5  # 条形宽度
    # index_support = np.arange(len(x_name)) * 10  # support条形图的横坐标
    # 使用两次 bar 函数画出两组条形图
    rects = plt.bar(x_names, height=sen_in_inter, width=bar_width, color='b', label='句子数')
    # 显示对应柱状图的数值
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
    plt.legend()  # 显示图例
    x = []
    for i in range(interval_num):
        x.append(i)
    plt.xticks(x, x_names, rotation=0)
    plt.ylabel('该范围句子个数')  # 纵坐标轴标题
    plt.title('句子长度分布')  # 图形标题
    plt.show()

def get_all_data():

    file = open("train_data.json", 'r', encoding='utf-8')
    papers = []
    for line in file.readlines():
        dic = json.loads(line)
        papers.append(dic)
    files = open("val_data.json", 'r', encoding='utf-8')
    for line1 in files.readlines():
        dic1 = json.loads(line1)
        papers.append(dic1)
    files.close()
    file.close()
    with open("all_data.json", 'w', encoding='utf-8') as fw:
        for paper in papers:
            fw.write(json.dumps(paper, ensure_ascii=False) + '\n')
    fw.close()


def sub_data(path = './all_data.json'):
    with open(path,'r', encoding='utf-8') as f:
        n = 0
        all= []
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)
            all.append(jsonstr)
            n+=1
        indexs = list(range(n))
        shuffle(indexs)
        with open('./sub_train_data.json', 'w', encoding='utf-8') as ft:
            with open('./sub_val_data.json', 'w', encoding='utf-8') as fv:
                mid = len(indexs) // 10 * 8

                for i in range(len(indexs)-1):
                    print(indexs[i])
                    if i <mid:

                        ft.write(json.dumps(all[indexs[i]],ensure_ascii=False) + '\n')
                    else:
                        fv.write(json.dumps(all[indexs[i]],ensure_ascii=False) + '\n')
                ft.close()
                fv.close()
                f.close()

if __name__ == '__main__':
    # get_lengths()
    sub_data()
