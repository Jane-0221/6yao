# -*- coding: utf-8 -*-
"""
测试子时跨日功能
"""

import sys
sys.path.insert(0, '.')

import datetime
from divination import get_lunar_datetime, get_shi_ke, time_divination


def test_zishi_cross_day():
    """测试子时跨日功能"""
    print("=" * 60)
    print("测试子时跨日功能")
    print("=" * 60)
    
    # 测试用例：2026年3月27日 23:20（晚子时）
    # 应该算作农历二月十日，而不是二月九日
    test_date = datetime.datetime(2026, 3, 27, 23, 20)
    
    print(f"\n测试时间: {test_date.strftime('%Y年%m月%d日 %H时%M分')}")
    
    # 获取时辰数
    shi_ke = get_shi_ke(test_date.hour)
    print(f"时辰数: {shi_ke} (子时)")
    
    # 获取农历日期（传入hour参数）
    lunar = get_lunar_datetime(test_date, test_date.hour)
    print(f"农历日期: {lunar.year}年{lunar.month}月{lunar.day}日")
    
    # 验证结果
    expected_day = 10  # 农历二月十日
    if lunar.day == expected_day:
        print(f"[PASS] 测试通过: 晚子时正确算作下一天（农历{lunar.month}月{lunar.day}日）")
    else:
        print(f"[FAIL] 测试失败: 期望农历{lunar.month}月{expected_day}日，实际{lunar.day}日")
    
    # 测试对比：22:00（亥时）应该还是当天
    print("\n" + "-" * 60)
    test_date_hai = datetime.datetime(2026, 3, 27, 22, 0)
    lunar_hai = get_lunar_datetime(test_date_hai, test_date_hai.hour)
    print(f"对比测试时间: {test_date_hai.strftime('%Y年%m月%d日 %H时%M分')}（亥时）")
    print(f"农历日期: {lunar_hai.year}年{lunar_hai.month}月{lunar_hai.day}日")
    if lunar_hai.day == 9:
        print(f"[PASS] 测试通过: 亥时正确算作当天（农历{lunar_hai.month}月{lunar_hai.day}日）")
    else:
        print(f"[FAIL] 测试失败: 期望农历{lunar_hai.month}月9日，实际{lunar_hai.day}日")
    
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
        print(f"动爻: {result['moving_yao']}")
    
    # 最终结果
    print("\n" + "=" * 60)
    if lunar.day == expected_day and lunar_hai.day == 9:
        print("[PASS] 所有测试通过！子时跨日功能正常")
    else:
        print("[FAIL] 测试失败，请检查代码")
    print("=" * 60)
    
    return lunar.day == expected_day and lunar_hai.day == 9


if __name__ == "__main__":
    test_zishi_cross_day()