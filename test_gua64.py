# -*- coding: utf-8 -*-
"""
64卦算法模块单元测试

测试用例覆盖：
1. 基本功能测试（八卦映射、64卦命名）
2. 本卦计算测试
3. 变卦计算测试（单动爻、多动爻）
4. 边界条件测试（八纯卦、无动爻）
5. 输入验证测试
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8，解决Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gua64 import (
    calculate_gua,
    calculate_ben_gua,
    calculate_bian_gua,
    parse_yao_list,
    validate_yao_list,
    normalize_moving_yao,
    get_trigram_name,
    get_trigram_nature,
    get_gua64_name,
    format_gua_full_name,
    flip_yao,
    format_gua_result,
    format_gua_table,
    format_yao_visual,
    TRIGRAM_NAMES,
    TRIGRAM_NATURES,
    GUA64_NAMES,
)


def test_trigram_mapping():
    """测试八卦映射"""
    print("\n【测试】八卦映射")
    
    # 测试所有八卦
    test_cases = [
        ((1, 1, 1), "乾", "天"),
        ((1, 1, 2), "兑", "泽"),
        ((1, 2, 1), "离", "火"),
        ((1, 2, 2), "震", "雷"),
        ((2, 1, 1), "巽", "风"),
        ((2, 1, 2), "坎", "水"),
        ((2, 2, 1), "艮", "山"),
        ((2, 2, 2), "坤", "地"),
    ]
    
    for trigram, expected_name, expected_nature in test_cases:
        name = get_trigram_name(trigram)
        nature = get_trigram_nature(name)
        assert name == expected_name, f"卦名错误: {trigram} -> {name}, 期望 {expected_name}"
        assert nature == expected_nature, f"自然象错误: {name} -> {nature}, 期望 {expected_nature}"
        print(f"  ✓ {trigram} -> {name} ({nature})")
    
    print("  八卦映射测试通过！")


def test_gua64_naming():
    """测试64卦命名"""
    print("\n【测试】64卦命名")
    
    # 测试异卦命名
    test_cases = [
        ("乾", "艮", "天山遁卦"),
        ("巽", "乾", "风天小畜卦"),
        ("乾", "坤", "天地否卦"),
        ("坎", "离", "水火既济卦"),
    ]
    
    for upper, lower, expected_suffix in test_cases:
        full_name = format_gua_full_name(upper, lower)
        assert full_name.endswith(expected_suffix), f"卦名错误: {full_name}, 期望以 {expected_suffix} 结尾"
        print(f"  ✓ 上{upper}下{lower} -> {full_name}")
    
    # 测试八纯卦命名
    pure_cases = [
        ("乾", "乾为天卦"),
        ("坤", "坤为地卦"),
        ("震", "震为雷卦"),
        ("巽", "巽为风卦"),
        ("坎", "坎为水卦"),
        ("离", "离为火卦"),
        ("艮", "艮为山卦"),
        ("兑", "兑为泽卦"),
    ]
    
    for gua, expected_suffix in pure_cases:
        full_name = format_gua_full_name(gua, gua)
        assert full_name.endswith(expected_suffix), f"八纯卦名错误: {full_name}, 期望以 {expected_suffix} 结尾"
        print(f"  ✓ 上{gua}下{gua} -> {full_name}")
    
    print("  64卦命名测试通过！")


def test_parse_yao_list():
    """测试六爻解析"""
    print("\n【测试】六爻解析")
    
    # 测试用例1: [1,1,1,2,1,1]
    result = parse_yao_list([1, 1, 1, 2, 1, 1])
    assert result['lower_gua_name'] == "乾", f"下卦错误: {result['lower_gua_name']}"
    assert result['upper_gua_name'] == "巽", f"上卦错误: {result['upper_gua_name']}"
    assert result['lower_nature'] == "天", f"下卦自然象错误: {result['lower_nature']}"
    assert result['upper_nature'] == "风", f"上卦自然象错误: {result['upper_nature']}"
    print(f"  ✓ [1,1,1,2,1,1] -> 下乾(天) 上巽(风)")
    
    # 测试用例2: [2,2,2,1,1,1]
    result = parse_yao_list([2, 2, 2, 1, 1, 1])
    assert result['lower_gua_name'] == "坤", f"下卦错误: {result['lower_gua_name']}"
    assert result['upper_gua_name'] == "乾", f"上卦错误: {result['upper_gua_name']}"
    print(f"  ✓ [2,2,2,1,1,1] -> 下坤(地) 上乾(天)")
    
    print("  六爻解析测试通过！")


def test_ben_gua():
    """测试本卦计算"""
    print("\n【测试】本卦计算")
    
    # 测试用例1: 风天小畜卦
    result = calculate_ben_gua([1, 1, 1, 2, 1, 1])
    assert result['name'] == "上巽下乾 风天小畜卦", f"本卦名错误: {result['name']}"
    print(f"  ✓ [1,1,1,2,1,1] -> {result['name']}")
    
    # 测试用例2: 天地否卦
    result = calculate_ben_gua([2, 2, 2, 1, 1, 1])
    assert result['name'] == "上乾下坤 天地否卦", f"本卦名错误: {result['name']}"
    print(f"  ✓ [2,2,2,1,1,1] -> {result['name']}")
    
    # 测试用例3: 乾为天卦（八纯卦）
    result = calculate_ben_gua([1, 1, 1, 1, 1, 1])
    assert result['name'] == "上乾下乾 乾为天卦", f"八纯卦名错误: {result['name']}"
    print(f"  ✓ [1,1,1,1,1,1] -> {result['name']}")
    
    print("  本卦计算测试通过！")


def test_bian_gua_single():
    """测试变卦计算（单动爻）"""
    print("\n【测试】变卦计算（单动爻）")
    
    # 测试用例: 天地否卦 -> 天山遁卦（三爻动）
    result = calculate_bian_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    assert result is not None, "变卦不应为None"
    assert result['name'] == "上乾下艮 天山遁卦", f"变卦名错误: {result['name']}"
    assert result['changed_yao'] == [3], f"动爻位置错误: {result['changed_yao']}"
    print(f"  ✓ 天地否卦(三爻动) -> {result['name']}")
    print(f"    变化详情: {result['change_detail']}")
    
    # 测试用例: 风天小畜卦 -> 风火家人卦（二爻动）
    # 原六爻 [1,1,1,2,1,1]，二爻动后变为 [1,2,1,2,1,1]
    # 下卦 [1,2,1]=离(火)，上卦 [2,1,1]=巽(风)
    result = calculate_bian_gua([1, 1, 1, 2, 1, 1], moving_yao=2)
    assert result is not None, "变卦不应为None"
    assert result['name'] == "上巽下离 风火家人卦", f"变卦名错误: {result['name']}"
    print(f"  ✓ 风天小畜卦(二爻动) -> {result['name']}")
    print(f"    变化详情: {result['change_detail']}")
    
    print("  变卦计算（单动爻）测试通过！")


def test_bian_gua_multiple():
    """测试变卦计算（多动爻）"""
    print("\n【测试】变卦计算（多动爻）")
    
    # 测试用例: 天地否卦 -> 火山旅卦（三爻、五爻动）
    # 原六爻 [2,2,2,1,1,1]，三爻动后变为 [2,2,1,1,1,1]，五爻动后变为 [2,2,1,1,2,1]
    # 下卦 [2,2,1]=艮(山)，上卦 [1,2,1]=离(火)
    result = calculate_bian_gua([2, 2, 2, 1, 1, 1], moving_yao=[3, 5])
    assert result is not None, "变卦不应为None"
    assert result['name'] == "上离下艮 火山旅卦", f"变卦名错误: {result['name']}"
    assert result['changed_yao'] == [3, 5], f"动爻位置错误: {result['changed_yao']}"
    print(f"  ✓ 天地否卦(三、五爻动) -> {result['name']}")
    print(f"    变化详情: {result['change_detail']}")
    
    print("  变卦计算（多动爻）测试通过！")


def test_bian_gua_none():
    """测试无动爻情况"""
    print("\n【测试】无动爻情况")
    
    # 测试无动爻
    result = calculate_bian_gua([1, 1, 1, 2, 1, 1], moving_yao=None)
    assert result is None, "无动爻时变卦应为None"
    print(f"  ✓ 无动爻 -> 变卦为None")
    
    # 测试空列表
    result = calculate_bian_gua([1, 1, 1, 2, 1, 1], moving_yao=[])
    assert result is None, "空动爻列表时变卦应为None"
    print(f"  ✓ 空动爻列表 -> 变卦为None")
    
    print("  无动爻测试通过！")


def test_calculate_gua():
    """测试主函数"""
    print("\n【测试】主函数 calculate_gua()")
    
    # 测试用例1: 无动爻
    result = calculate_gua([1, 1, 1, 2, 1, 1])
    assert result['ben_gua']['name'] == "上巽下乾 风天小畜卦"
    assert result['bian_gua'] is None
    assert result['moving_yao'] is None
    print(f"  ✓ 无动爻测试通过")
    
    # 测试用例2: 有动爻
    result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    assert result['ben_gua']['name'] == "上乾下坤 天地否卦"
    assert result['bian_gua']['name'] == "上乾下艮 天山遁卦"
    assert result['moving_yao'] == [3]
    print(f"  ✓ 有动爻测试通过")
    
    # 测试用例3: 多动爻
    result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=[3, 5])
    assert result['moving_yao'] == [3, 5]
    print(f"  ✓ 多动爻测试通过")
    
    print("  主函数测试通过！")


def test_input_validation():
    """测试输入验证"""
    print("\n【测试】输入验证")
    
    # 测试无效爻值
    try:
        validate_yao_list([1, 2, 3, 1, 1, 1])
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 无效爻值检测: {e}")
    
    # 测试数组长度错误
    try:
        validate_yao_list([1, 1, 1])
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 数组长度错误检测: {e}")
    
    # 测试无效动爻位置
    try:
        normalize_moving_yao(7)
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 无效动爻位置检测: {e}")
    
    # 测试无效类型
    try:
        normalize_moving_yao("三")
        assert False, "应该抛出异常"
    except ValueError as e:
        print(f"  ✓ 无效类型检测: {e}")
    
    print("  输入验证测试通过！")


def test_flip_yao():
    """测试爻值反转"""
    print("\n【测试】爻值反转")
    
    # 测试单爻反转
    yao_list = [1, 1, 1, 2, 1, 1]
    new_list = flip_yao(yao_list, [3])
    assert new_list[2] == 2, f"三爻应从1变为2，实际为{new_list[2]}"
    print(f"  ✓ 单爻反转: {yao_list} -> {new_list}")
    
    # 测试多爻反转
    yao_list = [1, 2, 1, 2, 1, 2]
    new_list = flip_yao(yao_list, [1, 3, 5])
    assert new_list[0] == 2, f"初爻应从1变为2"
    assert new_list[2] == 2, f"三爻应从1变为2"
    assert new_list[4] == 2, f"五爻应从1变为2"
    print(f"  ✓ 多爻反转: {yao_list} -> {new_list}")
    
    # 验证原数组不变
    assert yao_list == [1, 2, 1, 2, 1, 2], "原数组不应被修改"
    print(f"  ✓ 原数组未被修改")
    
    print("  爻值反转测试通过！")


def test_format_output():
    """测试格式化输出"""
    print("\n【测试】格式化输出")
    
    result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    
    # 测试简单格式
    output = format_gua_result(result)
    assert "本卦" in output and "变卦" in output
    print(f"  ✓ 简单格式输出正常")
    
    # 测试表格格式
    output = format_gua_table(result)
    assert "【本卦】" in output and "【变卦】" in output
    print(f"  ✓ 表格格式输出正常")
    
    # 测试可视化图形
    output = format_yao_visual([1, 2, 1, 2, 1, 2], [3])
    assert "初爻" in output and "上爻" in output
    print(f"  ✓ 可视化图形输出正常")
    
    print("  格式化输出测试通过！")


def test_user_examples():
    """测试用户提供的示例"""
    print("\n【测试】用户提供的示例")
    
    # 示例1: 输入 [1,1,1,2,1,1]，无动爻
    print("\n  示例1:")
    result1 = calculate_gua([1, 1, 1, 2, 1, 1])
    print(f"    六爻: {result1['yao_list']}")
    print(f"    本卦: {result1['ben_gua']['name']}")
    print(f"    变卦: {'无' if result1['bian_gua'] is None else result1['bian_gua']['name']}")
    
    assert result1['ben_gua']['name'] == "上巽下乾 风天小畜卦", "示例1本卦名错误"
    assert result1['bian_gua'] is None, "示例1变卦应为None"
    print("    ✓ 示例1测试通过")
    
    # 示例2: 输入 [2,2,2,1,1,1]，三爻动
    print("\n  示例2:")
    result2 = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    print(f"    六爻: {result2['yao_list']}")
    print(f"    本卦: {result2['ben_gua']['name']}")
    print(f"    变卦: {result2['bian_gua']['name']}")
    print(f"    解析: {result2['bian_gua']['change_detail']}")
    
    assert result2['ben_gua']['name'] == "上乾下坤 天地否卦", "示例2本卦名错误"
    assert result2['bian_gua']['name'] == "上乾下艮 天山遁卦", "示例2变卦名错误"
    assert "三爻阴变阳" in result2['bian_gua']['change_detail'], "示例2变化详情错误"
    print("    ✓ 示例2测试通过")
    
    print("\n  用户示例测试通过！")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("         64卦算法模块单元测试")
    print("=" * 60)
    
    tests = [
        ("八卦映射测试", test_trigram_mapping),
        ("64卦命名测试", test_gua64_naming),
        ("六爻解析测试", test_parse_yao_list),
        ("本卦计算测试", test_ben_gua),
        ("变卦计算测试（单动爻）", test_bian_gua_single),
        ("变卦计算测试（多动爻）", test_bian_gua_multiple),
        ("无动爻测试", test_bian_gua_none),
        ("主函数测试", test_calculate_gua),
        ("输入验证测试", test_input_validation),
        ("爻值反转测试", test_flip_yao),
        ("格式化输出测试", test_format_output),
        ("用户示例测试", test_user_examples),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n  ✗ {name} 失败: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: 通过 {passed}/{len(tests)}，失败 {failed}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)