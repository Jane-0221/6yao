# -*- coding: utf-8 -*-
"""
六爻地支辅助函数模块

提供格式化输出和显示功能。
"""

from typing import Dict

from .core import YAO_NAMES, get_six_yao_di_zhi


# =============================================================================
# 格式化输出函数
# =============================================================================

def format_di_zhi_result(result: Dict) -> str:
    """
    格式化输出六爻地支结果
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = get_six_yao_di_zhi("乾", "乾")
        >>> print(format_di_zhi_result(result))
        上卦：乾 | 下卦：乾
        ────────────────
        初爻：子
        二爻：寅
        三爻：辰
        四爻：午
        五爻：申
        上爻：戌
    """
    lines = []
    
    # 基本信息
    lines.append(f"上卦：{result['upper_gua']} | 下卦：{result['lower_gua']}")
    lines.append("─" * 20)
    
    # 六爻地支
    for yao_name, di_zhi in zip(YAO_NAMES, result['di_zhi']):
        lines.append(f"{yao_name}：{di_zhi}")
    
    return "\n".join(lines)


def print_di_zhi_result(result: Dict):
    """
    打印六爻地支结果
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
    """
    print(format_di_zhi_result(result))


def format_di_zhi_table(result: Dict) -> str:
    """
    以表格形式格式化六爻地支结果
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
    
    Returns:
        str: 表格形式的字符串
    
    Examples:
        >>> result = get_six_yao_di_zhi("乾", "乾")
        >>> print(format_di_zhi_table(result))
        ┌────────┬────────┐
        │  爻位  │  地支  │
        ├────────┼────────┤
        │ 初爻   │  子    │
        │ 二爻   │  寅    │
        │ 三爻   │  辰    │
        │ 四爻   │  午    │
        │ 五爻   │  申    │
        │ 上爻   │  戌    │
        └────────┴────────┘
    """
    lines = []
    
    # 表头
    lines.append("┌" + "─" * 8 + "┬" + "─" * 8 + "┐")
    lines.append("│  爻位  │  地支  │")
    lines.append("├" + "─" * 8 + "┼" + "─" * 8 + "┤")
    
    # 表体
    for yao_name, di_zhi in zip(YAO_NAMES, result['di_zhi']):
        lines.append(f"│ {yao_name:^6} │ {di_zhi:^6} │")
    
    # 表尾
    lines.append("└" + "─" * 8 + "┴" + "─" * 8 + "┘")
    
    return "\n".join(lines)


def format_di_zhi_with_gua_name(result: Dict, gua_name: str) -> str:
    """
    带卦名的格式化输出
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
        gua_name: 64卦名称
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = get_six_yao_di_zhi("乾", "乾")
        >>> print(format_di_zhi_with_gua_name(result, "乾为天"))
        卦象：乾为天
        上卦：乾 | 下卦：乾
        六爻地支：
        初爻：子
        二爻：寅
        三爻：辰
        四爻：午
        五爻：申
        上爻：戌
    """
    lines = []
    
    lines.append(f"卦象：{gua_name}")
    lines.append(f"上卦：{result['upper_gua']} | 下卦：{result['lower_gua']}")
    lines.append("六爻地支：")
    
    for yao_name, di_zhi in zip(YAO_NAMES, result['di_zhi']):
        lines.append(f"{yao_name}：{di_zhi}")
    
    return "\n".join(lines)


def format_di_zhi_simple(result: Dict) -> str:
    """
    简洁格式输出（用于 main.py 集成）
    
    格式：地支: 初爻子 二爻寅 三爻辰 四爻午 五爻申 上爻戌
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
    
    Returns:
        str: 简洁格式的字符串
    
    Examples:
        >>> result = get_six_yao_di_zhi("乾", "乾")
        >>> print(format_di_zhi_simple(result))
        地支: 初爻子 二爻寅 三爻辰 四爻午 五爻申 上爻戌
    """
    parts = []
    for yao_name, di_zhi in zip(YAO_NAMES, result['di_zhi']):
        parts.append(f"{yao_name}{di_zhi}")
    
    return f"地支: {' '.join(parts)}"


def format_di_zhi_inline(result: Dict) -> str:
    """
    单行格式输出
    
    格式：地支: 子 寅 辰 午 申 戌
    
    Args:
        result: get_six_yao_di_zhi() 返回的结果字典
    
    Returns:
        str: 单行格式的字符串
    
    Examples:
        >>> result = get_six_yao_di_zhi("乾", "乾")
        >>> print(format_di_zhi_inline(result))
        地支: 子 寅 辰 午 申 戌
    """
    return f"地支: {' '.join(result['di_zhi'])}"