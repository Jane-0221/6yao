# -*- coding: utf-8 -*-
"""
六亲辅助函数模块

提供格式化输出和显示功能。
"""

from typing import Dict

from .core import YAO_NAMES, get_six_yao_liu_qin


# =============================================================================
# 格式化输出函数
# =============================================================================

def format_liu_qin_result(result: Dict) -> str:
    """
    格式化输出六亲结果
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> print(format_liu_qin_result(result))
        宫位：乾宫（金）
        ──────────────────────
        初爻：子（水）→ 子孙
        二爻：寅（木）→ 妻财
        三爻：辰（土）→ 兄弟
        四爻：午（火）→ 官鬼
        五爻：申（金）→ 父母
        上爻：戌（土）→ 兄弟
    """
    lines = []
    
    # 基本信息
    lines.append(f"宫位：{result['gong']}（{result['gong_element']}）")
    lines.append("─" * 25)
    
    # 六爻六亲
    for yao_name, di_zhi, element, liu_qin in zip(
        YAO_NAMES, result['di_zhi'], result['yao_elements'], result['liu_qin']
    ):
        lines.append(f"{yao_name}：{di_zhi}（{element}）→ {liu_qin}")
    
    return "\n".join(lines)


def format_liu_qin_simple(result: Dict) -> str:
    """
    简洁格式输出六亲（与世应、地支显示风格一致）
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
    
    Returns:
        str: 简洁格式的字符串
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> print(format_liu_qin_simple(result))
        六亲: 子孙 妻财 兄弟 官鬼 父母 兄弟
    """
    return f"六亲: {' '.join(result['liu_qin'])}"


def print_liu_qin_result(result: Dict):
    """
    打印六亲结果
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
    """
    print(format_liu_qin_result(result))


def format_liu_qin_table(result: Dict) -> str:
    """
    以表格形式格式化六亲结果
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
    
    Returns:
        str: 表格形式的字符串
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> print(format_liu_qin_table(result))
        ┌──────┬──────┬──────┬────────┐
        │ 爻位 │ 地支 │ 五行 │  六亲  │
        ├──────┼──────┼──────┼────────┤
        │ 初爻 │  子  │  水  │  子孙  │
        │ 二爻 │  寅  │  木  │  妻财  │
        │ 三爻 │  辰  │  土  │  兄弟  │
        │ 四爻 │  午  │  火  │  官鬼  │
        │ 五爻 │  申  │  金  │  父母  │
        │ 上爻 │  戌  │  土  │  兄弟  │
        └──────┴──────┴──────┴────────┘
    """
    lines = []
    
    # 表头
    lines.append("┌" + "─" * 6 + "┬" + "─" * 6 + "┬" + "─" * 6 + "┬" + "─" * 8 + "┐")
    lines.append("│  爻位  │  地支  │  五行  │  六亲  │")
    lines.append("├" + "─" * 6 + "┼" + "─" * 6 + "┼" + "─" * 6 + "┼" + "─" * 8 + "┤")
    
    # 表体
    for yao_name, di_zhi, element, liu_qin in zip(
        YAO_NAMES, result['di_zhi'], result['yao_elements'], result['liu_qin']
    ):
        lines.append(f"│ {yao_name:^4} │ {di_zhi:^4} │ {element:^4} │ {liu_qin:^6} │")
    
    # 表尾
    lines.append("└" + "─" * 6 + "┴" + "─" * 6 + "┴" + "─" * 6 + "┴" + "─" * 8 + "┘")
    
    return "\n".join(lines)


def format_liu_qin_with_gua_name(result: Dict, gua_name: str) -> str:
    """
    带卦名的格式化输出
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
        gua_name: 64卦名称
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> print(format_liu_qin_with_gua_name(result, "乾为天"))
        卦象：乾为天
        宫位：乾宫（金）
        六爻六亲：
        初爻：子（水）→ 子孙
        二爻：寅（木）→ 妻财
        三爻：辰（土）→ 兄弟
        四爻：午（火）→ 官鬼
        五爻：申（金）→ 父母
        上爻：戌（土）→ 兄弟
    """
    lines = []
    
    lines.append(f"卦象：{gua_name}")
    lines.append(f"宫位：{result['gong']}（{result['gong_element']}）")
    lines.append("六爻六亲：")
    
    for yao_name, di_zhi, element, liu_qin in zip(
        YAO_NAMES, result['di_zhi'], result['yao_elements'], result['liu_qin']
    ):
        lines.append(f"{yao_name}：{di_zhi}（{element}）→ {liu_qin}")
    
    return "\n".join(lines)


def format_liu_qin_compact(result: Dict) -> str:
    """
    紧凑格式输出（一行显示所有六亲）
    
    Args:
        result: get_six_yao_liu_qin() 返回的结果字典
    
    Returns:
        str: 紧凑格式的字符串
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> print(format_liu_qin_compact(result))
        初爻子孙 二爻妻财 三爻兄弟 四爻官鬼 五爻父母 上爻兄弟
    """
    parts = []
    for yao_name, liu_qin in zip(YAO_NAMES, result['liu_qin']):
        parts.append(f"{yao_name}{liu_qin}")
    return " ".join(parts)