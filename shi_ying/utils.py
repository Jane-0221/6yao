# -*- coding: utf-8 -*-
"""
世应推算工具函数模块

提供格式化输出、打印等辅助功能。
"""

from typing import Dict, Optional

from .core import (
    SHIYING_MAP,
    YAO_NAMES,
    get_shi_ying,
    get_yao_name,
    get_gong_name,
    get_gua_info,
    normalize_gua_name,
    validate_gua_name,
)


# =============================================================================
# 格式化输出函数
# =============================================================================

def format_shi_ying_result(result: Dict[str, int], gua_name: str = None) -> str:
    """
    格式化输出世应结果
    
    Args:
        result: get_shi_ying返回的结果字典 {"shi": int, "ying": int}
        gua_name: 可选的卦名，用于显示
    
    Returns:
        str: 格式化后的字符串
    
    Examples:
        >>> result = {"shi": 6, "ying": 3}
        >>> print(format_shi_ying_result(result, "乾为天"))
        卦象：乾为天
        世爻：上爻（6）
        应爻：三爻（3）
    """
    lines = []
    
    if gua_name:
        lines.append(f"卦象：{gua_name}")
    
    shi = result["shi"]
    ying = result["ying"]
    
    lines.append(f"世爻：{get_yao_name(shi)}（{shi}）")
    lines.append(f"应爻：{get_yao_name(ying)}（{ying}）")
    
    return "\n".join(lines)


def format_shi_ying_table(gua_name: str) -> str:
    """
    格式化为表格形式输出
    
    Args:
        gua_name: 卦名
    
    Returns:
        str: 表格形式的字符串
    
    Examples:
        >>> print(format_shi_ying_table("乾为天"))
        ═════════════════════
        卦象：乾为天
        宫位：乾宫
        ─────────────────────
        世爻：上爻（第6爻）
        应爻：三爻（第3爻）
        ═════════════════════
    """
    info = get_gua_info(gua_name)
    
    lines = [
        "═" * 21,
        f"卦象：{info['gua_name']}",
        f"宫位：{info['gong']}",
        "─" * 21,
        f"世爻：{info['shi_name']}（第{info['shi']}爻）",
        f"应爻：{info['ying_name']}（第{info['ying']}爻）",
        "═" * 21,
    ]
    
    return "\n".join(lines)


def format_shi_ying_simple(result: Dict[str, int]) -> str:
    """
    简洁格式输出
    
    Args:
        result: get_shi_ying返回的结果字典
    
    Returns:
        str: 简洁格式的字符串
    
    Examples:
        >>> format_shi_ying_simple({"shi": 6, "ying": 3})
        '世6应3'
    """
    return f"世{result['shi']}应{result['ying']}"


# =============================================================================
# 打印函数
# =============================================================================

def print_shi_ying_result(gua_name: str) -> None:
    """
    打印世应结果（便捷函数）
    
    Args:
        gua_name: 卦名
    
    Examples:
        >>> print_shi_ying_result("乾为天")
        卦象：乾为天
        世爻：上爻（6）
        应爻：三爻（3）
    """
    result = get_shi_ying(gua_name)
    print(format_shi_ying_result(result, gua_name))


def print_shi_ying_table(gua_name: str) -> None:
    """
    打印表格形式的世应结果
    
    Args:
        gua_name: 卦名
    """
    print(format_shi_ying_table(gua_name))


# =============================================================================
# 查询函数
# =============================================================================

def get_shi_ying_info(gua_name: str) -> Dict:
    """
    获取完整的世应信息（包含名称）
    
    这是 get_gua_info 的别名，提供更直观的函数名。
    
    Args:
        gua_name: 卦名
    
    Returns:
        dict: {
            "gua_name": "卦名",
            "gong": "宫位",
            "shi": 世位,
            "ying": 应位,
            "shi_name": "世爻名称",
            "ying_name": "应爻名称"
        }
    
    Examples:
        >>> info = get_shi_ying_info("风天小畜")
        >>> info['gong']
        '巽宫'
        >>> info['shi_name']
        '初爻'
    """
    return get_gua_info(gua_name)


def find_gua_by_shi(shi_position: int) -> list:
    """
    查找所有世爻在指定位置的卦
    
    Args:
        shi_position: 世爻位置（1-6）
    
    Returns:
        list: 卦名列表
    
    Raises:
        ValueError: 位置不在1-6范围内
    
    Examples:
        >>> guas = find_gua_by_shi(6)
        >>> len(guas)
        8
        >>> "乾为天" in guas
        True
    """
    if not 1 <= shi_position <= 6:
        raise ValueError(f"世爻位置必须在1-6之间，当前值: {shi_position}")
    
    return [gua for gua, shi in SHIYING_MAP.items() if shi == shi_position]


def get_guas_by_gong(gong_name: str) -> list:
    """
    获取指定宫位的所有卦
    
    Args:
        gong_name: 宫位名称（如"乾宫"、"坤宫"等）
    
    Returns:
        list: 该宫位的8个卦名列表
    
    Examples:
        >>> guas = get_guas_by_gong("乾宫")
        >>> len(guas)
        8
        >>> guas[0]
        '乾为天'
    """
    from .core import GONG_GUA_MAP
    
    # 规范化宫位名称（去除"宫"字后重新添加）
    normalized = gong_name.replace("宫", "").strip() + "宫"
    
    if normalized not in GONG_GUA_MAP:
        valid_gongs = list(GONG_GUA_MAP.keys())
        raise ValueError(
            f"无效的宫位名称: '{gong_name}'。\n"
            f"有效宫位: {', '.join(valid_gongs)}"
        )
    
    return GONG_GUA_MAP[normalized]


# =============================================================================
# 验证函数
# =============================================================================

def validate_shi_ying_consistency() -> bool:
    """
    验证世应映射的一致性
    
    检查：
    1. 所有64卦都有映射
    2. 世应位置计算正确
    
    Returns:
        bool: 是否通过验证
    """
    # 检查卦数量
    if len(SHIYING_MAP) != 64:
        print(f"错误：卦数量不正确，应为64，实际为{len(SHIYING_MAP)}")
        return False
    
    # 检查每个卦的世应计算
    for gua_name, shi in SHIYING_MAP.items():
        ying = (shi + 3) if shi <= 3 else (shi - 3)
        result = get_shi_ying(gua_name)
        if result["shi"] != shi or result["ying"] != ying:
            print(f"错误：{gua_name} 世应计算不一致")
            return False
    
    return True


def print_all_shi_ying() -> None:
    """
    打印所有64卦的世应信息
    
    用于调试和验证。
    """
    from .core import GONG_GUA_MAP
    
    for gong, gua_list in GONG_GUA_MAP.items():
        print(f"\n{'=' * 20}")
        print(f"{gong}八卦")
        print('=' * 20)
        
        for gua in gua_list:
            info = get_gua_info(gua)
            print(f"{gua}: 世{info['shi']}({info['shi_name']}) 应{info['ying']}({info['ying_name']})")