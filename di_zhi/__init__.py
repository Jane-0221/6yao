# -*- coding: utf-8 -*-
"""
六爻地支模块

根据上下经卦计算六爻固定地支。

核心规则：
1. 六爻地支终身固定：同一卦的地支永远不变，与动爻、日辰、六神无关
2. 下卦（内卦）决定初爻、二爻、三爻
3. 上卦（外卦）决定四爻、五爻、上爻

使用方法：
    from di_zhi import get_six_yao_di_zhi, format_di_zhi_simple
    
    # 基本用法
    result = get_six_yao_di_zhi("乾", "乾")
    print(format_di_zhi_simple(result))
    # 输出: 地支: 初爻子 二爻寅 三爻辰 四爻午 五爻申 上爻戌
    
    # 与 gua64 模块集成
    from gua64 import calculate_gua
    gua = calculate_gua([1, 1, 1, 1, 1, 1])
    result = get_six_yao_di_zhi(
        gua["ben_gua"]["upper_gua"],
        gua["ben_gua"]["lower_gua"]
    )
"""

from .core import (
    # 常量
    TRIGRAM_NAZHI,
    VALID_TRIGRAMS,
    YAO_NAMES,
    # 核心函数
    validate_trigram,
    get_six_yao_di_zhi,
    get_yao_di_zhi,
)

from .utils import (
    # 格式化函数
    format_di_zhi_result,
    print_di_zhi_result,
    format_di_zhi_table,
    format_di_zhi_with_gua_name,
    format_di_zhi_simple,
    format_di_zhi_inline,
)


__all__ = [
    # 常量
    'TRIGRAM_NAZHI',
    'VALID_TRIGRAMS',
    'YAO_NAMES',
    # 核心函数
    'validate_trigram',
    'get_six_yao_di_zhi',
    'get_yao_di_zhi',
    # 格式化函数
    'format_di_zhi_result',
    'print_di_zhi_result',
    'format_di_zhi_table',
    'format_di_zhi_with_gua_name',
    'format_di_zhi_simple',
    'format_di_zhi_inline',
]

__version__ = '1.0.0'
__author__ = '六爻起卦系统'