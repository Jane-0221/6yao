# -*- coding: utf-8 -*-
"""
六神排盘功能测试文件

验证四个测试用例：
1. 天干="甲"：初爻青龙，顺排
2. 天干="己"：初爻螣蛇，顺排
3. 天干="癸"：初爻玄武，顺排
4. 无效天干="子"：抛出异常
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8，解决Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from six_gods import (
    calculate_six_gods,
    format_six_gods_result,
    print_six_gods_result,
    get_tiangan_index,
    validate_tiangan,
    get_six_god_for_yao,
    SIX_GODS,
    YAO_NAMES,
)


def test_case_1():
    """
    测试用例1：天干="甲"
    
    预期输出：
    初爻：青龙
    二爻：朱雀
    三爻：勾陈
    四爻：螣蛇
    五爻：白虎
    上爻：玄武
    """
    print("\n" + "=" * 60)
    print("测试用例1：天干='甲'")
    print("=" * 60)
    
    result = calculate_six_gods("甲")
    
    # 验证基本信息
    assert result['day_tiangan'] == "甲", "天干应为'甲'"
    assert result['start_god'] == "青龙", "起始六神应为'青龙'"
    assert result['start_index'] == 0, "起始索引应为0"
    
    # 验证六神列表
    expected = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]
    assert result['six_gods_list'] == expected, f"六神列表应为{expected}"
    
    # 打印结果
    print(format_six_gods_result(result))
    print("\n[PASS] 测试用例1通过")
    
    return True


def test_case_2():
    """
    测试用例2：天干="己"
    
    预期输出：
    初爻：螣蛇
    二爻：白虎
    三爻：玄武
    四爻：青龙
    五爻：朱雀
    上爻：勾陈
    """
    print("\n" + "=" * 60)
    print("测试用例2：天干='己'")
    print("=" * 60)
    
    result = calculate_six_gods("己")
    
    # 验证基本信息
    assert result['day_tiangan'] == "己", "天干应为'己'"
    assert result['start_god'] == "螣蛇", "起始六神应为'螣蛇'"
    assert result['start_index'] == 3, "起始索引应为3"
    
    # 验证六神列表
    expected = ["螣蛇", "白虎", "玄武", "青龙", "朱雀", "勾陈"]
    assert result['six_gods_list'] == expected, f"六神列表应为{expected}"
    
    # 打印结果
    print(format_six_gods_result(result))
    print("\n[PASS] 测试用例2通过")
    
    return True


def test_case_3():
    """
    测试用例3：天干="癸"
    
    预期输出：
    初爻：玄武
    二爻：青龙
    三爻：朱雀
    四爻：勾陈
    五爻：螣蛇
    上爻：白虎
    """
    print("\n" + "=" * 60)
    print("测试用例3：天干='癸'")
    print("=" * 60)
    
    result = calculate_six_gods("癸")
    
    # 验证基本信息
    assert result['day_tiangan'] == "癸", "天干应为'癸'"
    assert result['start_god'] == "玄武", "起始六神应为'玄武'"
    assert result['start_index'] == 5, "起始索引应为5"
    
    # 验证六神列表
    expected = ["玄武", "青龙", "朱雀", "勾陈", "螣蛇", "白虎"]
    assert result['six_gods_list'] == expected, f"六神列表应为{expected}"
    
    # 打印结果
    print(format_six_gods_result(result))
    print("\n[PASS] 测试用例3通过")
    
    return True


def test_case_4():
    """
    测试用例4：无效天干="子"
    
    预期：抛出 ValueError，提示"无效的天干，请输入十天干之一：甲、乙、丙、丁、戊、己、庚、辛、壬、癸"
    """
    print("\n" + "=" * 60)
    print("测试用例4：天干='子'（无效天干）")
    print("=" * 60)
    
    try:
        result = calculate_six_gods("子")
        print("[FAIL] 测试失败：应该抛出 ValueError 异常")
        return False
    except ValueError as e:
        error_msg = str(e)
        print(f"正确抛出异常: {error_msg}")
        
        # 验证错误信息包含关键内容
        assert "无效的天干" in error_msg, "错误信息应包含'无效的天干'"
        assert "子" in error_msg, "错误信息应包含输入的天干'子'"
        
        print("\n[PASS] 测试用例4通过")
        return True


def test_all_tiangan():
    """测试所有天干的映射"""
    print("\n" + "=" * 60)
    print("测试所有天干映射")
    print("=" * 60)
    
    # 天干到起始六神的映射
    expected_mapping = {
        "甲": ("青龙", 0),
        "乙": ("青龙", 0),
        "丙": ("朱雀", 1),
        "丁": ("朱雀", 1),
        "戊": ("勾陈", 2),
        "己": ("螣蛇", 3),
        "庚": ("白虎", 4),
        "辛": ("白虎", 4),
        "壬": ("玄武", 5),
        "癸": ("玄武", 5),
    }
    
    for tiangan, (expected_god, expected_index) in expected_mapping.items():
        result = calculate_six_gods(tiangan)
        assert result['start_god'] == expected_god, f"{tiangan}的起始六神应为{expected_god}"
        assert result['start_index'] == expected_index, f"{tiangan}的起始索引应为{expected_index}"
        print(f"  {tiangan} -> {result['start_god']} (索引{result['start_index']}) [OK]")
    
    print("\n[PASS] 所有天干映射测试通过")
    return True


def test_with_yao_list():
    """测试带六爻列表的情况"""
    print("\n" + "=" * 60)
    print("测试带六爻列表")
    print("=" * 60)
    
    # 测试数据
    yao_list = [1, 2, 1, 2, 1, 2]  # 阳阴阳阴阳阴
    
    result = calculate_six_gods("甲", yao_list=yao_list)
    
    # 验证结果包含六爻信息
    assert 'yao_details' in result, "结果应包含yao_details"
    assert 'yao_list' in result, "结果应包含yao_list"
    assert result['yao_list'] == yao_list, "yao_list应与输入一致"
    
    # 验证爻位详情
    assert len(result['yao_details']) == 6, "应有6个爻位详情"
    
    # 打印结果
    print(format_six_gods_result(result))
    
    # 验证每个爻位
    for i, detail in enumerate(result['yao_details']):
        assert detail['yao_index'] == i + 1, f"爻位序号应为{i + 1}"
        assert detail['yao_name'] == YAO_NAMES[i], f"爻位名称应为{YAO_NAMES[i]}"
        print(f"  {detail['yao_name']}: {detail['six_god']} - {detail['yin_yang']} [OK]")
    
    print("\n[PASS] 带六爻列表测试通过")
    return True


def test_helper_functions():
    """测试辅助函数"""
    print("\n" + "=" * 60)
    print("测试辅助函数")
    print("=" * 60)
    
    # 测试 get_tiangan_index
    print("\n【测试 get_tiangan_index】")
    assert get_tiangan_index("甲") == 0
    assert get_tiangan_index("己") == 3
    assert get_tiangan_index("癸") == 5
    print("  get_tiangan_index 测试通过 [OK]")
    
    # 测试 validate_tiangan
    print("\n【测试 validate_tiangan】")
    assert validate_tiangan("甲") == True
    assert validate_tiangan("子") == False
    assert validate_tiangan("") == False
    assert validate_tiangan(123) == False
    print("  validate_tiangan 测试通过 [OK]")
    
    # 测试 get_six_god_for_yao
    print("\n【测试 get_six_god_for_yao】")
    assert get_six_god_for_yao("甲", 1) == "青龙"  # 初爻
    assert get_six_god_for_yao("甲", 2) == "朱雀"  # 二爻
    assert get_six_god_for_yao("甲", 6) == "玄武"  # 上爻
    print("  get_six_god_for_yao 测试通过 [OK]")
    
    print("\n[PASS] 辅助函数测试通过")
    return True


def test_formula_verification():
    """
    验证核心计算公式：六神索引 = (起始索引 + 爻位偏移量) % 6
    
    详细验证每个天干、每个爻位的六神计算是否正确
    """
    print("\n" + "=" * 60)
    print("验证核心计算公式")
    print("=" * 60)
    
    # 测试几个典型天干
    test_cases = [
        ("甲", 0),  # 青龙
        ("丙", 1),  # 朱雀
        ("戊", 2),  # 勾陈
        ("己", 3),  # 螣蛇
        ("庚", 4),  # 白虎
        ("壬", 5),  # 玄武
    ]
    
    for tiangan, start_index in test_cases:
        print(f"\n天干'{tiangan}'（起始索引={start_index}）:")
        result = calculate_six_gods(tiangan)
        
        for yao_offset in range(6):
            # 核心公式：六神索引 = (起始索引 + 爻位偏移量) % 6
            expected_index = (start_index + yao_offset) % 6
            expected_god = SIX_GODS[expected_index]
            actual_god = result['six_gods_list'][yao_offset]
            
            assert actual_god == expected_god, \
                f"第{yao_offset + 1}爻六神应为{expected_god}，实际为{actual_god}"
            
            print(f"  第{yao_offset + 1}爻: 索引=({start_index}+{yao_offset})%6={expected_index} -> {actual_god} [OK]")
    
    print("\n[PASS] 核心计算公式验证通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("       六神排盘功能测试")
    print("=" * 60)
    
    tests = [
        ("测试用例1：天干='甲'", test_case_1),
        ("测试用例2：天干='己'", test_case_2),
        ("测试用例3：天干='癸'", test_case_3),
        ("测试用例4：无效天干='子'", test_case_4),
        ("所有天干映射测试", test_all_tiangan),
        ("带六爻列表测试", test_with_yao_list),
        ("辅助函数测试", test_helper_functions),
        ("核心公式验证", test_formula_verification),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n[FAIL] {name} 失败")
        except Exception as e:
            failed += 1
            print(f"\n[FAIL] {name} 异常: {e}")
    
    # 测试总结
    print("\n" + "=" * 60)
    print(f"测试完成：通过 {passed}/{len(tests)}，失败 {failed}/{len(tests)}")
    print("=" * 60)
    
    if failed == 0:
        print("\n[SUCCESS] 所有测试通过！六神排盘功能实现正确。")
    else:
        print(f"\n[WARNING] 有 {failed} 个测试失败，请检查。")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)