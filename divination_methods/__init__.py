# -*- coding: utf-8 -*-
"""
起卦方式模块

包含五种起卦方式：
1. 标的物起卦（笔画+日时）- biao_di_wu_divination
2. 硬币起卦 - coin_divination, auto_coin_divination, coin_toss_to_yao
3. 数字起卦 - number_divination_v2
4. 时间起卦（梅花易数）- time_divination
5. 随机起卦 - random_divination

辅助模块：
- lunar_utils: 农历辅助函数
- stroke_counter: 繁体字笔画计算
- utils: 公共辅助函数（GUA_NAMES, GUA_BINARIES, gua_to_yao_list, get_yao_description）
"""

# 公共常量和函数
from .utils import GUA_NAMES, GUA_BINARIES, gua_to_yao_list, get_yao_description

# 农历辅助函数
from .lunar_utils import (
    get_lunar_datetime,
    get_year_zhi,
    get_day_tiangan,
    get_shi_ke,
    DI_ZHI,
    DI_ZHI_LIST,
    TIAN_GAN_LIST
)

# 繁体字笔画计算
from .stroke_counter import (
    get_traditional,
    get_simplified,
    get_char_stroke,
    get_text_stroke
)

# 标的物起卦
from .biao_di_wu import biao_di_wu_divination

# 硬币起卦
from .coin import coin_toss_to_yao, coin_divination, auto_coin_divination

# 数字起卦
from .number import number_divination_v2

# 时间起卦和随机起卦
from .time_random import time_divination, random_divination

__all__ = [
    # 公共常量和函数
    'GUA_NAMES',
    'GUA_BINARIES',
    'gua_to_yao_list',
    'get_yao_description',
    # 农历辅助函数
    'get_lunar_datetime',
    'get_year_zhi',
    'get_day_tiangan',
    'get_shi_ke',
    'DI_ZHI',
    'DI_ZHI_LIST',
    'TIAN_GAN_LIST',
    # 繁体字笔画计算
    'get_traditional',
    'get_simplified',
    'get_char_stroke',
    'get_text_stroke',
    # 标的物起卦
    'biao_di_wu_divination',
    # 硬币起卦
    'coin_toss_to_yao',
    'coin_divination',
    'auto_coin_divination',
    # 数字起卦
    'number_divination_v2',
    # 时间起卦和随机起卦
    'time_divination',
    'random_divination',
]