# -*- coding: utf-8 -*-
"""
六神排盘辅助函数模块

提供格式化输出和显示功能。
"""

from .core import YAO_NAMES, SIX_GODS


def format_six_gods_result(result: dict) -> str:
    """
    格式化输出六神排盘结果
    
    Args:
        result: calculate_six_gods() 返回的结果字典
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = calculate_six_gods("甲")
        >>> print(format_six_gods_result(result))
        日天干：甲
        初爻起始六神：青龙
        ────────────────
        初爻：青龙
        二爻：朱雀
        三爻：勾陈
        四爻：螣蛇
        五爻：白虎
        上爻：玄武
    """
    lines = []
    
    # 基本信息
    lines.append(f"日天干：{result['day_tiangan']}")
    lines.append(f"初爻起始六神：{result['start_god']}")
    lines.append("─" * 20)
    
    # 六神排盘
    if 'yao_details' in result:
        # 带六爻信息
        for detail in result['yao_details']:
            lines.append(f"{detail['yao_name']}：{detail['six_god']} - {detail['yin_yang']}")
    else:
        # 仅六神
        for yao_name, god in zip(YAO_NAMES, result['six_gods_list']):
            lines.append(f"{yao_name}：{god}")
    
    return "\n".join(lines)


def print_six_gods_result(result: dict):
    """
    打印六神排盘结果
    
    Args:
        result: calculate_six_gods() 返回的结果字典
    """
    print(format_six_gods_result(result))


def format_six_gods_table(result: dict) -> str:
    """
    以表格形式格式化六神排盘结果
    
    Args:
        result: calculate_six_gods() 返回的结果字典
    
    Returns:
        str: 表格形式的字符串
    """
    lines = []
    
    # 表头
    lines.append("┌" + "─" * 8 + "┬" + "─" * 8 + "┬" + "─" * 20 + "┐")
    lines.append("│  爻位  │  六神  │      阴阳属性      │")
    lines.append("├" + "─" * 8 + "┼" + "─" * 8 + "┼" + "─" * 20 + "┤")
    
    # 内容
    if 'yao_details' in result:
        for detail in result['yao_details']:
            yao_name = detail['yao_name'].center(6)
            god = detail['six_god'].center(6)
            yin_yang = detail['yin_yang'].center(18)
            lines.append(f"│{yao_name}│{god}│{yin_yang}│")
    else:
        for yao_name, god in zip(YAO_NAMES, result['six_gods_list']):
            yao_name_fmt = yao_name.center(6)
            god_fmt = god.center(6)
            lines.append(f"│{yao_name_fmt}│{god_fmt}│{''.center(18)}│")
    
    # 表尾
    lines.append("└" + "─" * 8 + "┴" + "─" * 8 + "┴" + "─" * 20 + "┘")
    
    # 添加天干信息
    lines.append(f"\n日天干：{result['day_tiangan']}，初爻起始六神：{result['start_god']}")
    
    return "\n".join(lines)


def format_six_gods_simple(result: dict) -> str:
    """
    简洁格式输出六神（与六亲显示风格一致）
    
    Args:
        result: calculate_six_gods() 返回的结果字典
    
    Returns:
        str: 简洁格式的字符串
    
    Examples:
        >>> result = calculate_six_gods("甲")
        >>> print(format_six_gods_simple(result))
        六神: 青龙 朱雀 勾陈 螣蛇 白虎 玄武
    """
    return f"六神: {' '.join(result['six_gods_list'])}"


def get_six_god_for_yao(day_tiangan: str, yao_position: int) -> str:
    """
    获取指定爻位的六神
    
    Args:
        day_tiangan: 天干
        yao_position: 爻位（1-6，1=初爻，6=上爻）
    
    Returns:
        str: 六神名称
    
    Raises:
        ValueError: 无效天干或爻位
    """
    from .core import get_tiangan_index
    
    # 参数校验
    if not 1 <= yao_position <= 6:
        raise ValueError(f"无效的爻位{yao_position}，爻位必须在1-6之间")
    
    # 获取起始索引
    start_index = get_tiangan_index(day_tiangan)
    
    # 计算六神索引
    # 爻位偏移量 = 爻位 - 1（初爻偏移量为0）
    yao_offset = yao_position - 1
    god_index = (start_index + yao_offset) % 6
    
    return SIX_GODS[god_index]


def validate_tiangan(day_tiangan: str) -> bool:
    """
    验证天干是否有效
    
    Args:
        day_tiangan: 天干字符串
    
    Returns:
        bool: 是否有效
    """
    from .core import VALID_TIANGAN
    
    if not isinstance(day_tiangan, str):
        return False
    
    return day_tiangan.strip() in VALID_TIANGAN


# =============================================================================
# 测试函数
# =============================================================================

def test_utils():
    """测试辅助函数"""
    from .core import calculate_six_gods
    
    print("=" * 60)
    print("辅助函数测试")
    print("=" * 60)
    
    # 测试 format_six_gods_result
    print("\n【测试 format_six_gods_result】")
    result = calculate_six_gods("甲")
    print(format_six_gods_result(result))
    
    # 测试带六爻信息
    print("\n【测试带六爻信息】")
    result = calculate_six_gods("甲", yao_list=[1, 2, 1, 2, 1, 2])
    print(format_six_gods_result(result))
    
    # 测试表格形式
    print("\n【测试 format_six_gods_table】")
    result = calculate_six_gods("己", yao_list=[1, 0, 1, 0, 1, 0])
    print(format_six_gods_table(result))
    
    # 测试 get_six_god_for_yao
    print("\n【测试 get_six_god_for_yao】")
    for pos in range(1, 7):
        god = get_six_god_for_yao("甲", pos)
        print(f"  第{pos}爻：{god}")
    
    # 测试 validate_tiangan
    print("\n【测试 validate_tiangan】")
    print(f"  '甲' 有效: {validate_tiangan('甲')}")
    print(f"  '子' 有效: {validate_tiangan('子')}")
    
    print("\n" + "=" * 60)
    print("辅助函数测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_utils()