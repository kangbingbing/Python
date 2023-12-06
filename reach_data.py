# coding:utf-8

import pandas as pd

def check_and_assign(value):
    if '携程' in str(value):
        return '携程' 
    elif '东丽' in str(value):
        return '东丽' 
    elif '佳农' in str(value):
        return '佳农食品'
    elif '中石化' in str(value) or '中国石化' in str(value):
        return '中国石化' 
    elif '怡宝' in str(value) or '魔力' in str(value):
        return '华润怡宝' 
    elif '京东运动' in str(value):
        return '京东运动' 
    elif '明治' in str(value) or 'Meiji' in str(value) or 'ZAVAS' in str(value) or '匝巴斯' in str(value):
        return '匝巴斯' 
    elif '豫园股份' in str(value) or '上海表' in str(value):
        return '豫园股份'
    elif '上海贵酒' in str(value):
        return '上海贵酒'  
    elif '上海体彩' in str(value) or '上海市体育彩票' in str(value) or '上海体育彩票' in str(value):
        return '上海体彩' 
    elif '上海外服' in str(value):
        return '上海外服' 
    elif '蒂芙尼' in str(value) or 'Tiffany' in str(value) or 'TIFFANY' in str(value):
        return '蒂芙尼'   
    elif '耐克' in str(value) or 'nike' in str(value) or 'NIKE' in str(value):
        return '耐克' 
    elif '银联' in str(value):
        return '中国银联' 
    elif '浦发' in str(value):
        return '浦发银行' 
    elif '沃尔沃' in str(value) or 'VOLVO' in str(value):
        return '沃尔沃' 
    elif '汇添富' in str(value):
        return '汇添富' 
    elif '太平洋' in str(value) or '太保' in str(value):
        return '太平洋保险' 
    elif '东方证券' in str(value) or '东方投行' in str(value):
        return '东方证券' 
    else :
        return ""

if __name__ == '__main__':

	# 读取Excel文件
    input_file = "上马数据.xlsx"
    df = pd.read_excel(input_file)

    # 使用apply方法遍历列并将结果写入C列
    df['name'] = df["title"].apply(check_and_assign)
    df['name'] = df["content"].apply(check_and_assign)


    # 反写到同一个Excel文件
    output_file = "output.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
