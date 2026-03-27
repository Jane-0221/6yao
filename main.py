# -*- coding: utf-8 -*-
"""
六爻起卦系统 - 交互式主程序
四种起卦方式：
1. 标的物起卦（笔画+日时）
2. 硬币起卦
3. 数字起卦（上下卦分开输入）
4. 六神排盘（根据日天干）
"""

import sys
import io
import datetime

# 设置标准输出编码为UTF-8，解决Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from divination import (
    biao_di_wu_divination,
    coin_divination,
    auto_coin_divination,
    number_divination_v2,
    get_day_tiangan,
    GUA_NAMES
)

from six_gods import (
    calculate_six_gods,
    format_six_gods_result,
    validate_tiangan,
)


def print_menu():
    """打印菜单"""
    print("\n" + "=" * 50)
    print("       六爻起卦系统")
    print("=" * 50)
    print("1. 标的物起卦（笔画+日时）")
    print("2. 硬币起卦")
    print("3. 数字起卦（上下卦分开输入）")
    print("4. 六神排盘（根据日天干）")
    print("0. 退出")
    print("=" * 50)


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
        
        # 显示卦象信息
        if 'gua_info' in result:
            gua = result['gua_info']
            print("-" * 50)
            print(f"本卦: {gua['ben_gua']['name']}")
            if gua['bian_gua']:
                print(f"变卦: {gua['bian_gua']['name']}")
                print(f"变化: {gua['bian_gua']['change_detail']}")
            else:
                print("变卦: 无")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def coin_menu():
    """硬币起卦菜单"""
    print("\n--- 硬币起卦 ---")
    print("1. 系统自动抛硬币")
    print("2. 手动输入硬币结果")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == "1":
        auto_coin_menu()
    elif choice == "2":
        manual_coin_menu()
    else:
        print("无效选择！")


def auto_coin_menu():
    """系统自动抛硬币"""
    print("\n系统正在自动抛硬币...")
    
    try:
        result = auto_coin_divination()
        display_coin_result(result)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def manual_coin_menu():
    """手动输入硬币结果"""
    print("\n--- 手动输入硬币结果 ---")
    print("请输入6次抛硬币结果，每次3枚硬币")
    print("输入格式：3个数字，1=正面，0=反面，用空格分隔")
    print("例如：1 1 0 表示两个正面一个反面")
    print()
    
    coin_results_list = []
    
    for i in range(6):
        while True:
            try:
                input_str = input(f"第{i+1}次抛硬币结果: ").strip()
                parts = input_str.split()
                
                if len(parts) != 3:
                    print("错误：请输入3个数字！")
                    continue
                
                coin_results = []
                valid = True
                for p in parts:
                    if p == '1':
                        coin_results.append(True)  # 正面
                    elif p == '0':
                        coin_results.append(False)  # 反面
                    else:
                        print("错误：只能输入0或1！")
                        valid = False
                        break
                
                if valid:
                    coin_results_list.append(coin_results)
                    break
                    
            except Exception as e:
                print(f"输入错误: {e}")
    
    try:
        result = coin_divination(coin_results_list)
        display_coin_result(result)
        
    except Exception as e:
        print(f"起卦出错: {e}")


def display_coin_result(result):
    """显示硬币起卦结果"""
    print("\n" + "=" * 50)
    print("起卦结果")
    print("=" * 50)
    
    # 显示每次抛硬币的详情
    print("\n硬币详情：")
    for detail in result['coin_details']:
        coin_str = " ".join(["正" if c else "反" for c in detail['coin_results']])
        moving_marker = " ←动爻" if detail['is_moving'] else ""
        print(f"  {detail['yao_name']}: {coin_str} ({detail['heads_count']}正{detail['tails_count']}反) -> {detail['yao_desc']}{moving_marker}")
    
    # 显示六爻列表
    print(f"\n六爻: {result['yao_list']}")
    
    # 显示动爻
    if result['moving_yao_list']:
        print(f"动爻: 第{', '.join(map(str, result['moving_yao_list']))}爻")
    else:
        print("动爻: 无")
    
    # 显示卦象信息
    if 'gua_info' in result:
        gua = result['gua_info']
        print("-" * 50)
        print(f"本卦: {gua['ben_gua']['name']}")
        if gua['bian_gua']:
            print(f"变卦: {gua['bian_gua']['name']}")
            print(f"变化: {gua['bian_gua']['change_detail']}")
        else:
            print("变卦: 无")
    
    print("=" * 50)


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
        
        # 显示卦象信息
        if 'gua_info' in result:
            gua = result['gua_info']
            print("-" * 50)
            print(f"本卦: {gua['ben_gua']['name']}")
            if gua['bian_gua']:
                print(f"变卦: {gua['bian_gua']['name']}")
                print(f"变化: {gua['bian_gua']['change_detail']}")
            else:
                print("变卦: 无")
        
        print("=" * 50)
        
    except ValueError:
        print("错误：请输入有效的数字！")
    except Exception as e:
        print(f"起卦出错: {e}")


def six_gods_menu():
    """六神排盘菜单"""
    print("\n--- 六神排盘 ---")
    print("根据《卜筮正宗》六爻六神排盘的正统规则")
    print("六神顺序：青龙、朱雀、勾陈、螣蛇、白虎、玄武")
    print()
    print("1. 使用当前日期的天干")
    print("2. 手动输入天干")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == "1":
        auto_six_gods_menu()
    elif choice == "2":
        manual_six_gods_menu()
    else:
        print("无效选择！")


def auto_six_gods_menu():
    """使用当前日期的天干进行六神排盘"""
    print("\n--- 使用当前日期的天干 ---")
    
    try:
        # 获取当前日期的天干
        day_tiangan = get_day_tiangan()
        today = datetime.datetime.now()
        
        print(f"当前日期: {today.strftime('%Y-%m-%d')}")
        print(f"日天干: {day_tiangan}")
        print()
        
        # 计算六神排盘
        result = calculate_six_gods(day_tiangan)
        
        # 显示结果
        print("=" * 50)
        print("六神排盘结果")
        print("=" * 50)
        print(format_six_gods_result(result))
        print("=" * 50)
        
    except Exception as e:
        print(f"排盘出错: {e}")


def manual_six_gods_menu():
    """手动输入天干进行六神排盘"""
    print("\n--- 手动输入天干 ---")
    print("请输入十天干之一：甲、乙、丙、丁、戊、己、庚、辛、壬、癸")
    
    tiangan = input("日天干: ").strip()
    
    if not tiangan:
        print("错误：天干不能为空！")
        return
    
    # 验证天干
    if not validate_tiangan(tiangan):
        print(f"错误：无效的天干'{tiangan}'")
        print("请输入十天干之一：甲、乙、丙、丁、戊、己、庚、辛、壬、癸")
        return
    
    try:
        # 计算六神排盘
        result = calculate_six_gods(tiangan)
        
        # 显示结果
        print("\n" + "=" * 50)
        print("六神排盘结果")
        print("=" * 50)
        print(format_six_gods_result(result))
        print("=" * 50)
        
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"排盘出错: {e}")


def main():
    """主函数"""
    while True:
        print_menu()
        choice = input("请选择 (0-4): ").strip()
        
        if choice == "1":
            biao_di_wu_menu()
        elif choice == "2":
            coin_menu()
        elif choice == "3":
            number_menu()
        elif choice == "4":
            six_gods_menu()
        elif choice == "0":
            print("\n感谢使用，再见！")
            break
        else:
            print("\n无效选择，请重新输入！")


if __name__ == "__main__":
    main()