# -*- coding: utf-8 -*-
"""
硬币起卦功能测试
测试"以少为尊"规则
测试六爻对应关系：索引0=上爻，索引5=初爻
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8，解决Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divination_methods import coin_toss_to_yao, coin_divination, auto_coin_divination


def test_coin_toss_to_yao():
    """测试单次抛硬币转爻功能（以少为尊规则）"""
    print("=" * 60)
    print("测试 coin_toss_to_yao 函数（以少为尊规则）")
    print("=" * 60)
    
    test_cases = [
        # (硬币结果, 期望爻值, 期望是否动爻, 期望爻类型名称, 描述)
        ([True, True, True], 1, True, "老阳", "3正0反 -> 老阳（阳爻动）"),
        ([True, True, False], 2, False, "少阴", "2正1反 -> 少阴（阴爻静，以少为尊）"),
        ([True, False, True], 2, False, "少阴", "2正1反 -> 少阴（阴爻静，以少为尊）"),
        ([False, True, True], 2, False, "少阴", "2正1反 -> 少阴（阴爻静，以少为尊）"),
        ([True, False, False], 1, False, "少阳", "1正2反 -> 少阳（阳爻静，以少为尊）"),
        ([False, True, False], 1, False, "少阳", "1正2反 -> 少阳（阳爻静，以少为尊）"),
        ([False, False, True], 1, False, "少阳", "1正2反 -> 少阳（阳爻静，以少为尊）"),
        ([False, False, False], 2, True, "老阴", "0正3反 -> 老阴（阴爻动）"),
    ]
    
    all_passed = True
    for coin_results, expected_value, expected_moving, expected_type, desc in test_cases:
        yao_value, is_moving, yao_type = coin_toss_to_yao(coin_results)
        
        passed = (yao_value == expected_value and 
                  is_moving == expected_moving and 
                  yao_type == expected_type)
        
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {desc}")
        print(f"    输入: {coin_results} ({sum(coin_results)}正{3-sum(coin_results)}反)")
        print(f"    期望: 爻值={expected_value}, 动爻={expected_moving}, 类型={expected_type}")
        print(f"    实际: 爻值={yao_value}, 动爻={is_moving}, 类型={yao_type}")
        
        if not passed:
            all_passed = False
        print()
    
    return all_passed


def test_coin_divination():
    """测试完整的硬币起卦功能（六爻顺序：索引0=上爻，索引5=初爻）"""
    print("=" * 60)
    print("测试 coin_divination 函数")
    print("六爻顺序：索引0=上爻，索引5=初爻")
    print("=" * 60)
    
    # 模拟6次抛硬币结果
    # 输入顺序：第1个=上爻，第6个=初爻
    coin_results_list = [
        [True, True, True],    # 上爻: 老阳
        [True, True, False],   # 五爻: 少阴（以少为尊）
        [True, False, False],  # 四爻: 少阳（以少为尊）
        [False, False, False], # 三爻: 老阴
        [True, False, True],   # 二爻: 少阴（以少为尊）
        [False, True, False],  # 初爻: 少阳（以少为尊）
    ]
    
    result = coin_divination(coin_results_list)
    
    print(f"六爻列表: {result['yao_list']}")
    print(f"  索引0=上爻, 索引1=五爻, 索引2=四爻, 索引3=三爻, 索引4=二爻, 索引5=初爻")
    print(f"动爻列表: {result['moving_yao_list']}")
    print()
    
    # 验证六爻列表（从上爻到初爻）
    expected_yao_list = [1, 2, 1, 2, 2, 1]  # 上爻=老阳, 五爻=少阴, 四爻=少阳, 三爻=老阴, 二爻=少阴, 初爻=少阳
    if result['yao_list'] == expected_yao_list:
        print("✓ 六爻列表正确")
    else:
        print(f"✗ 六爻列表错误: 期望 {expected_yao_list}, 实际 {result['yao_list']}")
    
    # 验证动爻列表（老阳和老阴为动爻，返回爻位置：上爻=6, 三爻=3）
    expected_moving = [6, 3]  # 上爻(6)和三爻(3)为动爻
    if sorted(result['moving_yao_list']) == sorted(expected_moving):
        print("✓ 动爻列表正确")
    else:
        print(f"✗ 动爻列表错误: 期望 {expected_moving}, 实际 {result['moving_yao_list']}")
    
    print()
    
    # 显示详细信息
    print("详细信息（从上爻到初爻）:")
    for detail in result['coin_details']:
        coin_str = " ".join(["正" if c else "反" for c in detail['coin_results']])
        moving_marker = " ←动爻" if detail['is_moving'] else ""
        print(f"  {detail['yao_name']}: {coin_str} ({detail['heads_count']}正{detail['tails_count']}反) -> {detail['yao_desc']}{moving_marker}")
    
    print()
    
    # 验证卦象信息
    if 'gua_info' in result:
        gua = result['gua_info']
        print(f"本卦: {gua['ben_gua']['name']}")
        if gua['bian_gua']:
            print(f"变卦: {gua['bian_gua']['name']}")
            print(f"变化: {gua['bian_gua']['change_detail']}")
    
    return result['yao_list'] == expected_yao_list and sorted(result['moving_yao_list']) == sorted(expected_moving)


def test_auto_coin_divination():
    """测试自动硬币起卦功能"""
    print("=" * 60)
    print("测试 auto_coin_divination 函数")
    print("=" * 60)
    
    result = auto_coin_divination()
    
    print(f"六爻列表: {result['yao_list']}")
    print(f"  索引0=上爻, 索引1=五爻, 索引2=四爻, 索引3=三爻, 索引4=二爻, 索引5=初爻")
    print(f"动爻列表: {result['moving_yao_list']}")
    
    # 验证六爻列表长度
    if len(result['yao_list']) == 6:
        print("✓ 六爻列表长度正确")
    else:
        print(f"✗ 六爻列表长度错误: 期望 6, 实际 {len(result['yao_list'])}")
    
    # 验证所有爻值都是1或2
    if all(yao in [1, 2] for yao in result['yao_list']):
        print("✓ 所有爻值都是有效的（1或2）")
    else:
        print("✗ 存在无效的爻值")
    
    print()
    print("详细信息（从上爻到初爻）:")
    for detail in result['coin_details']:
        coin_str = " ".join(["正" if c else "反" for c in detail['coin_results']])
        moving_marker = " ←动爻" if detail['is_moving'] else ""
        print(f"  {detail['yao_name']}: {coin_str} ({detail['heads_count']}正{detail['tails_count']}反) -> {detail['yao_desc']}{moving_marker}")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("硬币起卦功能测试")
    print("规则：以少为尊")
    print("六爻顺序：索引0=上爻，索引5=初爻")
    print("=" * 60 + "\n")
    
    # 测试1: 单次抛硬币转爻
    test1_passed = test_coin_toss_to_yao()
    print()
    
    # 测试2: 完整硬币起卦
    test2_passed = test_coin_divination()
    print()
    
    # 测试3: 自动硬币起卦
    test3_passed = test_auto_coin_divination()
    print()
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"coin_toss_to_yao 测试: {'✓ 通过' if test1_passed else '✗ 失败'}")
    print(f"coin_divination 测试: {'✓ 通过' if test2_passed else '✗ 失败'}")
    print(f"auto_coin_divination 测试: {'✓ 通过' if test3_passed else '✗ 失败'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n所有测试通过！")
    else:
        print("\n存在测试失败！")


if __name__ == "__main__":
    main()