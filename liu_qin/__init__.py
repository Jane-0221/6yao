# -*- coding: utf-8 -*-
"""
六亲模块

根据本宫五行和爻地支五行计算六亲。

核心规则：
1. 生我者为父母
2. 我生者为子孙
3. 克我者为官鬼
4. 我克者为妻财
5. 同我者为兄弟

使用方法：
    from liu_qin import get_six_yao_liu_qin, format_liu_qin_simple
    
    # 基本用法
    result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
    print(format_liu_qin_simple(result))
    
    # 与其他模块集成
    from shi_ying import get_gong_name
    from di_zhi import get_six_yao_di_zhi
    
    gua_name = "乾为天"
    gong = get_gong_name(gua_name)
    di_zhi_result = get_six_yao_di_zhi("乾", "乾")
    liu_qin_result = get_six_yao_liu_qin(gong, di_zhi_result["di_zhi"])
"""

from .core import (
    WUXING_LIST,
    LIU_QIN_LIST,
    SHENG_KE,
    DI_ZHI_ELEMENT,
    GONG_ELEMENT,
    YAO_NAMES,
    validate_wuxing,
    validate_di_zhi,
    validate_gong,
    get_element_by_di_zhi,
    get_element_by_gong,
    get_liu_qin_by_element,
    get_six_yao_liu_qin,
    get_yao_liu_qin,
)

from .utils import (
    format_liu_qin_result,
    format_liu_qin_simple,
    print_liu_qin_result,
    format_liu_qin_table,
    format_liu_qin_with_gua_name,
    format_liu_qin_compact,
)

__all__ = [
    # 常量
    'WUXING_LIST',
    'LIU_QIN_LIST',
    'SHENG_KE',
    'DI_ZHI_ELEMENT',
    'GONG_ELEMENT',
    'YAO_NAMES',
    # 核心函数
    'validate_wuxing',
    'validate_di_zhi',
    'validate_gong',
    'get_element_by_di_zhi',
    'get_element_by_gong',
    'get_liu_qin_by_element',
    'get_six_yao_liu_qin',
    'get_yao_liu_qin',
    # 辅助函数
    'format_liu_qin_result',
    'format_liu_qin_simple',
    'print_liu_qin_result',
    'format_liu_qin_table',
    'format_liu_qin_with_gua_name',
    'format_liu_qin_compact',
]

__version__ = '1.0.0'
__author__ = '六爻起卦系统'