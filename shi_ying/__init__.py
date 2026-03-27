# -*- coding: utf-8 -*-
"""
世应推算模块

根据六爻正统规则，实现64卦世应位置自动推算。

核心规则：
1. 世应唯一绑定卦象：同一个卦，世爻、应爻位置永远固定不变
2. 应爻计算公式：应爻位置 = 世爻位置 + 3（若结果 > 6，则减 6）
3. 八宫卦序与世位固定对应

使用方法：
    from shi_ying import get_shi_ying, format_shi_ying_result
    
    # 基本用法
    result = get_shi_ying("乾为天")
    print(result)  # {"shi": 6, "ying": 3}
    
    # 格式化输出
    print(format_shi_ying_result(result, "乾为天"))
    
    # 获取完整信息
    from shi_ying import get_gua_info
    info = get_gua_info("风天小畜")
    print(info)
    # {
    #     "gua_name": "风天小畜",
    #     "gong": "巽宫",
    #     "shi": 1,
    #     "ying": 4,
    #     "shi_name": "初爻",
    #     "ying_name": "四爻"
    # }
"""

from .core import (
    # 常量
    SHIYING_MAP,
    YAO_NAMES,
    GONG_NAMES,
    GONG_GUA_MAP,
    # 核心函数
    get_shi_ying,
    calculate_ying,
    normalize_gua_name,
    validate_gua_name,
    get_yao_name,
    get_gong_name,
    get_all_gua_names,
    get_gua_info,
)

from .utils import (
    # 格式化函数
    format_shi_ying_result,
    format_shi_ying_table,
    format_shi_ying_simple,
    # 打印函数
    print_shi_ying_result,
    print_shi_ying_table,
    # 查询函数
    get_shi_ying_info,
    find_gua_by_shi,
    get_guas_by_gong,
    # 验证函数
    validate_shi_ying_consistency,
    print_all_shi_ying,
)

__all__ = [
    # 常量
    'SHIYING_MAP',
    'YAO_NAMES',
    'GONG_NAMES',
    'GONG_GUA_MAP',
    # 核心函数
    'get_shi_ying',
    'calculate_ying',
    'normalize_gua_name',
    'validate_gua_name',
    'get_yao_name',
    'get_gong_name',
    'get_all_gua_names',
    'get_gua_info',
    # 格式化函数
    'format_shi_ying_result',
    'format_shi_ying_table',
    'format_shi_ying_simple',
    # 打印函数
    'print_shi_ying_result',
    'print_shi_ying_table',
    # 查询函数
    'get_shi_ying_info',
    'find_gua_by_shi',
    'get_guas_by_gong',
    # 验证函数
    'validate_shi_ying_consistency',
    'print_all_shi_ying',
]

__version__ = '1.0.0'
__author__ = '6yao'