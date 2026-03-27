# -*- coding: utf-8 -*-
"""
六神排盘模块

根据《卜筮正宗》六爻六神排盘的正统规则实现六神自动排盘功能。

六神固定循环顺序：青龙、朱雀、勾陈、螣蛇、白虎、玄武
排盘唯一依据：起卦当日的天干

使用方法：
    from six_gods import calculate_six_gods, format_six_gods_result
    
    # 基本用法
    result = calculate_six_gods("甲")
    print(format_six_gods_result(result))
    
    # 带六爻信息
    result = calculate_six_gods("甲", yao_list=[1, 2, 1, 2, 1, 2])
    print(format_six_gods_result(result))
"""

from .core import (
    SIX_GODS,
    TIANGAN_TO_INDEX,
    YAO_NAMES,
    VALID_TIANGAN,
    get_tiangan_index,
    calculate_six_gods,
    get_yao_yin_yang,
)

from .utils import (
    format_six_gods_result,
    print_six_gods_result,
    format_six_gods_table,
    get_six_god_for_yao,
    validate_tiangan,
)

__all__ = [
    # 常量
    'SIX_GODS',
    'TIANGAN_TO_INDEX',
    'YAO_NAMES',
    'VALID_TIANGAN',
    # 核心函数
    'get_tiangan_index',
    'calculate_six_gods',
    'get_yao_yin_yang',
    # 辅助函数
    'format_six_gods_result',
    'print_six_gods_result',
    'format_six_gods_table',
    'get_six_god_for_yao',
    'validate_tiangan',
]

__version__ = '1.0.0'
__author__ = '六爻起卦系统'