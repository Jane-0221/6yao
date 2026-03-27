# -*- coding: utf-8 -*-
"""
六爻起卦系统 - 交互式主程序
四种起卦方式：
1. 时间起卦（梅花易数）
2. 标的物起卦（笔画+日时）
3. 随机起卦
4. 数字起卦（上下卦分开输入）
"""

import sys
from divination import (
    time_divination,
    biao_di_wu_divination,
    random_divination,
    number_divination_v2,
    GUA_NAMES
)


def print_menu():
    """打印菜单"""
    print("\n" + "=" * 50)
    print("       六爻起卦系统")
    print("=" * 50)
    print("1. 时间起卦（梅花易数）")
    print("2. 标的物起卦（笔画+日时）")
    print("3. 随机起卦")
    print("4. 数字起卦（上下卦分开输入）")
    print("0. 退出")
    print("=" * 50)


def time_menu():
    """时间起卦菜单"""
    print("\n--- 时间起卦（梅花易数）---")
    print("算法：上卦=(年+月+日)%8，下卦=(年+月+日+时)%8，动爻=(年+月+日+时)%6")
    
    try:
        result = time_divination()
        
        print("\n" + "=" * 50)
        print("起卦结果")
        print("=" * 50)
        print(f"上卦: {result['upper_gua']} - {GUA_NAMES[result['upper_gua']]}")
        print(f"下卦: {result['lower_gua']} - {GUA_NAMES[result['lower_gua']]}")
        print(f"动爻: 第{result['moving_yao']}爻")
        print(f"六爻: {result['yao_list']}")
        print(f"农历: {result['lunar']['year']}年{result['lunar']['month']}月{result['lunar']['day']}日 时辰{result['lunar']['shi_ke']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def biao_di_wu_menu():
    """标的物起卦菜单"""
    print("\n--- 标的物起卦 ---")
    print("请输入标的物名称（简体），如：股票、婚姻、事业等")
    name = input("标的物名称: ").strip()
    
    if not name:
        print("错误：名称不能为空！")
        return
    
    try:
        result = biao_di_wu_divination(name)
        
        print("\n" + "=" * 50)
        print("起卦结果")
        print("=" * 50)
        print(f"标的物(简体): {result['name']}")
        print(f"标的物(繁体): {result['name_traditional']}")
        print(f"笔画数: {result['stroke']}")
        print(f"上卦: {result['upper_gua']} - {GUA_NAMES[result['upper_gua']]}")
        print(f"下卦: {result['lower_gua']} - {GUA_NAMES[result['lower_gua']]}")
        print(f"动爻: 第{result['moving_yao']}爻")
        print(f"六爻: {result['yao_list']}")
        print(f"农历: {result['lunar']['year']}年{result['lunar']['month']}月{result['lunar']['day']}日 时辰{result['lunar']['shi_ke']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def random_menu():
    """随机起卦菜单"""
    print("\n--- 随机起卦 ---")
    print("正在生成随机六爻...")
    
    try:
        result = random_divination()
        
        print("\n" + "=" * 50)
        print("起卦结果")
        print("=" * 50)
        print(f"六爻: {result['yao_list']}")
        print(f"动爻: 第{result['moving_yao']}爻")
        
        # 显示六爻详情
        print("\n六爻详情（从初爻到上爻）：")
        yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        for i, yao in enumerate(result['yao_list']):
            if yao == 0:
                desc = "少阴（阴爻，静）"
            elif yao == 1:
                desc = "少阳（阳爻，静）"
            elif yao == 2:
                desc = "老阴（阴爻，动→变阳）"
            else:
                desc = "老阳（阳爻，动→变阴）"
            marker = " ←动爻" if i + 1 == result['moving_yao'] else ""
            print(f"  {yao_names[i]}: {yao} = {desc}{marker}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def number_menu():
    """数字起卦菜单"""
    print("\n--- 数字起卦 ---")
    print("八卦对应: 乾1、兑2、离3、震4、巽5、坎6、艮7、坤8")
    print("算法：数字%8=卦数（余数0取8）")
    print("动爻：(上卦数+下卦数)%6（余数0取6）")
    
    try:
        upper_str = input("上卦数字: ").strip()
        lower_str = input("下卦数字: ").strip()
        
        if not upper_str or not lower_str:
            print("错误：数字不能为空！")
            return
        
        upper_num = int(upper_str)
        lower_num = int(lower_str)
        
        result = number_divination_v2(upper_num, lower_num)
        
        print("\n" + "=" * 50)
        print("起卦结果")
        print("=" * 50)
        print(f"上卦: {result['upper_num']} % 8 = {result['upper_gua']} - {GUA_NAMES[result['upper_gua']]}")
        print(f"下卦: {result['lower_num']} % 8 = {result['lower_gua']} - {GUA_NAMES[result['lower_gua']]}")
        print(f"动爻: ({result['upper_num']}+{result['lower_num']}) % 6 = {result['moving_yao']}爻")
        print(f"六爻: {result['yao_list']}")
        
        # 显示六爻详情
        print("\n六爻详情（从初爻到上爻）：")
        yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        for i, yao in enumerate(result['yao_list']):
            if yao == 0:
                desc = "少阴（阴爻，静）"
            elif yao == 1:
                desc = "少阳（阳爻，静）"
            elif yao == 2:
                desc = "老阴（阴爻，动→变阳）"
            else:
                desc = "老阳（阳爻，动→变阴）"
            marker = " ←动爻" if i + 1 == result['moving_yao'] else ""
            print(f"  {yao_names[i]}: {yao} = {desc}{marker}")
        
        print("=" * 50)
        
    except ValueError:
        print("错误：请输入有效的数字！")
    except Exception as e:
        print(f"起卦出错: {e}")


def main():
    """主函数"""
    while True:
        print_menu()
        choice = input("请选择 (0-4): ").strip()
        
        if choice == "1":
            time_menu()
        elif choice == "2":
            biao_di_wu_menu()
        elif choice == "3":
            random_menu()
        elif choice == "4":
            number_menu()
        elif choice == "0":
            print("\n感谢使用，再见！")
            break
        else:
            print("\n无效选择，请重新输入！")


if __name__ == "__main__":
    main()