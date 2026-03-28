# -*- coding: utf-8 -*-
"""
数字起卦模块（上下卦分开输入）

算法：
- 上卦 = 输入数字 % 8，余数0取8
- 下卦 = 输入数字 % 8，余数0取8
- 动爻 = (上卦数 + 下卦数) % 6，余数0取6
"""

from gua64 import calculate_gua
from .utils import gua_to_yao_list


def number_divination_v2(upper_num: int, lower_num: int):
    """
    数字起卦（上下卦分开输入）
    
    算法：
    - 上卦 = 输入数字 % 8，余数0取8
    - 下卦 = 输入数字 % 8，余数0取8
    - 动爻 = (上卦数 + 下卦数) % 6，余数0取6
    
    Args:
        upper_num: 上卦数字
        lower_num: 下卦数字
    
    Returns:
        dict: {
            'upper_num': 输入的上卦数字,
            'lower_num': 输入的下卦数字,
            'upper_gua': 上卦(1-8),
            'lower_gua': 下卦(1-8),
            'yao_list': 六爻列表,
            'moving_yao': 动爻位置(1-6),
            'gua_info': 卦象信息
        }
    """
    # 计算卦数
    upper_gua = upper_num % 8
    upper_gua = upper_gua if upper_gua != 0 else 8
    
    lower_gua = lower_num % 8
    lower_gua = lower_gua if lower_gua != 0 else 8
    
    # 计算动爻
    moving_num = (upper_num + lower_num) % 6
    moving_yao = moving_num if moving_num != 0 else 6
    
    # 生成六爻列表
    yao_list = gua_to_yao_list(upper_gua, lower_gua)
    
    # 计算卦象
    gua_info = calculate_gua(yao_list, moving_yao)
    
    return {
        'upper_num': upper_num,
        'lower_num': lower_num,
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'yao_list': yao_list,
        'moving_yao': moving_yao,
        'gua_info': gua_info,
    }