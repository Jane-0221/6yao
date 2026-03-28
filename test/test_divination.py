# -*- coding: utf-8 -*-
"""
测试起卦功能
"""

from divination_methods import (
    time_divination,
    get_lunar_datetime,
    get_shi_ke,
    get_yao_description
)
from test import liu_yao_zhuang_gua, print_zhuang_gua_result
import datetime


def test_zishi_cross_day():
    """测试子时跨日功能"""
    print("=" * 60)
    print("测试子时跨日功能")
    print("=" * 60)
    
    # 测试用例：2026年3月27日 23:20（晚子时）
    # 应该算作农历二月十日，而不是二月九日
    test_date = datetime.datetime(2026, 3, 27, 23, 20)
    
    print(f"测试时间: {test_date.strftime('%Y年%m月%d日 %H时%M分')}")
    
    # 获取时辰数
    shi_ke = get_shi_ke(test_date.hour)
    print(f"时辰数: {shi_ke} (子时)")
    
    # 获取农历日期（传入hour参数）
    lunar = get_lunar_datetime(test_date, test_date.hour)
    print(f"农历日期: {lunar.year}年{lunar.month}月{lunar.day}日")
    
    # 验证结果
    expected_day = 10  # 农历二月十日
    if lunar.day == expected_day:
        print(f"✓ 测试通过: 晚子时正确算作下一天（农历{lunar.month}月{lunar.day}日）")
    else:
        print(f"✗ 测试失败: 期望农历{lunar.month}月{expected_day}日，实际{lunar.day}日")
    
    # 测试对比：22:00（亥时）应该还是当天
    test_date_hai = datetime.datetime(2026, 3, 27, 22, 0)
    lunar_hai = get_lunar_datetime(test_date_hai, test_date_hai.hour)
    print(f"\n对比测试: 22:00（亥时）")
    print(f"农历日期: {lunar_hai.year}年{lunar_hai.month}月{lunar_hai.day}日")
    if lunar_hai.day == 9:
        print(f"✓ 测试通过: 亥时正确算作当天（农历{lunar_hai.month}月{lunar_hai.day}日）")
    else:
        print(f"✗ 测试失败: 期望农历{lunar_hai.month}月9日，实际{lunar_hai.day}日")
    
    # 测试完整起卦
    print("\n" + "-" * 60)
    print("测试子时时间起卦")
    result = time_divination(test_date)
    print(f"农历年: {result['lunar']['year']}")
    print(f"农历月: {result['lunar']['month']}")
    print(f"农历日: {result['lunar']['day']}")
    print(f"时辰: {result['lunar']['shi_ke_name']} ({result['lunar']['shi_ke']})")
    print(f"本卦: {result['gua_info']['ben_gua']['name']}")
    if result['gua_info']['bian_gua']:
        print(f"变卦: {result['gua_info']['bian_gua']['name']}")
    
    return lunar.day == expected_day and lunar_hai.day == 9


def test_time_divination():
    """测试时间起卦"""
    print("=" * 60)
    print("测试时间起卦")
    print("=" * 60)
    
    result = time_divination()
    print(f"当前时间: {datetime.datetime.now().strftime('%Y年%m月%d日 %H时')}")
    print(f"农历日期: {result['lunar']['year']}年{result['lunar']['month']}月{result['lunar']['day']}日")
    print(f"时辰: {result['lunar']['shi_ke_name']} ({result['lunar']['shi_ke']})")
    print(f"本卦: {result['gua_info']['ben_gua']['name']}")
    if result['gua_info']['bian_gua']:
        print(f"变卦: {result['gua_info']['bian_gua']['name']}")
        print(f"动爻: {result['moving_yao']}")
    
    return result


def test_number_divination():
    """测试数字起卦"""
    print("\n" + "=" * 60)
    print("测试数字起卦")
    print("=" * 60)
    
    numbers = [1, 3, 5, 7, 9, 2]
    yao_list = number_divination(numbers)
    print(f"输入数字: {numbers}")
    print(f"生成六爻: {yao_list}")
    
    descriptions = get_yao_description(yao_list)
    print("\n六爻详情（从初爻到上爻）：")
    for i, (yao, desc) in enumerate(zip(yao_list, descriptions), 1):
        print(f"  {i}爻: {yao} = {desc}")
    
    return yao_list


def test_manual_divination():
    """测试手动输入"""
    print("\n" + "=" * 60)
    print("测试手动输入")
    print("=" * 60)
    
    yao_input = "3,0,1,2,1,1"
    yao_list = manual_divination(yao_input)
    print(f"输入字符串: {yao_input}")
    print(f"生成六爻: {yao_list}")
    
    descriptions = get_yao_description(yao_list)
    print("\n六爻详情（从初爻到上爻）：")
    for i, (yao, desc) in enumerate(zip(yao_list, descriptions), 1):
        print(f"  {i}爻: {yao} = {desc}")
    
    return yao_list


def test_full_divination(yao_list, method_name):
    """测试完整装卦流程"""
    print("\n" + "=" * 60)
    print(f"测试完整装卦流程 - {method_name}")
    print("=" * 60)
    
    # 使用示例时间参数
    ri_gan, ri_zhi = "甲", "子"
    yue_jian = "寅"
    
    print(f"时间参数: 日干={ri_gan}, 日支={ri_zhi}, 月建={yue_jian}")
    
    # 执行装卦
    result = liu_yao_zhuang_gua(yao_list, ri_gan, ri_zhi, yue_jian)
    
    # 添加起卦信息
    result['divination_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result['divination_method'] = method_name
    result['yao_list'] = yao_list
    result['ri_gan'] = ri_gan
    result['ri_zhi'] = ri_zhi
    result['yue_jian'] = yue_jian
    
    # 显示结果
    print_zhuang_gua_result(result)
    
    # 测试保存功能
    print("\n" + "=" * 60)
    print("测试保存功能...")
    json_path, txt_path = save_result(result, f"test_{method_name}")
    print(f"JSON保存路径: {json_path}")
    print(f"TXT保存路径: {txt_path}")
    
    return result


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("六爻起卦系统 - 功能测试")
    print("=" * 60)
    
    # 测试0: 子时跨日测试
    test_zishi_cross_day()
    
    # 测试1: 时间起卦
    result1 = test_time_divination()
    
    # 测试2: 数字起卦
    yao_list2 = test_number_divination()
    test_full_divination(yao_list2, "数字起卦")
    
    # 测试3: 手动输入
    yao_list3 = test_manual_divination()
    test_full_divination(yao_list3, "手动输入")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
