# -*- coding: utf-8 -*-
"""
64卦算法模块

根据六爻数组计算本卦和变卦。

使用示例:
    from gua64 import calculate_gua, format_gua_result
    
    # 计算卦象
    result = calculate_gua([1, 1, 1, 2, 1, 1])
    print(f"本卦: {result['ben_gua']['name']}")
    
    # 带动爻
    result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    print(f"本卦: {result['ben_gua']['name']}")
    print(f"变卦: {result['bian_gua']['name']}")
    
    # 格式化输出
    print(format_gua_result(result))
"""

from .core import (
    # 核心函数
    calculate_gua,
    calculate_ben_gua,
    calculate_bian_gua,
    parse_yao_list,
    
    # 辅助函数
    validate_yao_list,
    normalize_moving_yao,
    get_trigram_name,
    get_trigram_nature,
    get_gua64_name,
    format_gua_full_name,
    flip_yao,
    
    # 常量
    TRIGRAM_NAMES,
    TRIGRAM_NATURES,
    GUA64_NAMES,
    YAO_NAMES,
)

from .utils import (
    # 格式化函数
    format_gua_result,
    format_gua_table,
    format_yao_visual,
    format_full_output,
    get_gua_symbol,
)

# 版本号
__version__ = "1.0.0"

# 公开API
__all__ = [
    # 核心函数
    "calculate_gua",
    "calculate_ben_gua", 
    "calculate_bian_gua",
    "parse_yao_list",
    
    # 辅助函数
    "validate_yao_list",
    "normalize_moving_yao",
    "get_trigram_name",
    "get_trigram_nature",
    "get_gua64_name",
    "format_gua_full_name",
    "flip_yao",
    
    # 格式化函数
    "format_gua_result",
    "format_gua_table",
    "format_yao_visual",
    "format_full_output",
    "get_gua_symbol",
    
    # 常量
    "TRIGRAM_NAMES",
    "TRIGRAM_NATURES",
    "GUA64_NAMES",
    "YAO_NAMES",
    
    # 版本
    "__version__",
]