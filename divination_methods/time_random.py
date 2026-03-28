# -*- coding: utf-8 -*-
"""
时间起卦和随机起卦模块

包含：
1. 时间起卦（梅花易数）
2. 随机起卦
"""

import random
import datetime
from lunarcalendar import Converter, Solar, Lunar
from gua64 import calculate_gua

from .lunar_utils import (
    get_lunar_datetime,
    get_year_zhi,
    get_shi_ke,
    DI_ZHI_LIST
)
from .utils import gua_to_yao_list


def time_divination(solar_date=None):
    """
    时间起卦（梅花易数）
    
    算法：
    - 上卦 = (Xi + Xj + Xy) % 8，余数0取8
    - 下卦 = (Xi + Xj + Xy + Xu) % 8，余数0取8
    - 动爻 = (Xi + Xj + Xy + Xu) % 6，余数0取6
    
    其中：
    - Xi = 年支数（子1、丑2、寅3、卯4、辰5、巳6、午7、未8、申9、酉10、戌11、亥12）
    - Xj = 农历月数
    - Xy = 农历日数
    - Xu = 时辰数（子1、丑2、...、亥12）
    
    注意：子时（23:00-01:00）属于下一天，晚子时（23:00-23:59）使用下一天的农历日期
    
    Args:
        solar_date: 阳历日期，默认为当前时间
    
    Returns:
        dict: {
            'upper_gua': 上卦(1-8),
            'lower_gua': 下卦(1-8),
            'moving_yao': 动爻位置(1-6),
            'yao_list': 六爻列表,
            'lunar': 农历日期信息,
            'gua_info': 卦象信息
        }
    """
    # 获取小时数
    hour = datetime.datetime.now().hour if solar_date is None else solar_date.hour
    
    # 获取农历日期（传入hour参数以支持子时跨日）
    lunar = get_lunar_datetime(solar_date, hour)
    
    # 获取农历时间
    lunar_year = lunar.year
    lunar_month = lunar.month
    lunar_day = lunar.day
    
    # 获取年支数 Xi
    year_zhi = get_year_zhi(lunar_year)
    
    # 获取时辰数 Xu
    shi_ke = get_shi_ke(hour)
    
    # 计算上卦：(Xi + Xj + Xy) % 8
    upper_num = (year_zhi + lunar_month + lunar_day) % 8
    upper_gua = upper_num if upper_num != 0 else 8
    
    # 计算下卦：(Xi + Xj + Xy + Xu) % 8
    lower_num = (year_zhi + lunar_month + lunar_day + shi_ke) % 8
    lower_gua = lower_num if lower_num != 0 else 8
    
    # 计算动爻：(Xi + Xj + Xy + Xu) % 6
    moving_num = (year_zhi + lunar_month + lunar_day + shi_ke) % 6
    moving_yao = moving_num if moving_num != 0 else 6
    
    # 生成六爻列表
    yao_list = gua_to_yao_list(upper_gua, lower_gua)
    
    # 计算卦象
    gua_info = calculate_gua(yao_list, moving_yao)
    
    return {
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'moving_yao': moving_yao,
        'yao_list': yao_list,
        'lunar': {
            'year': lunar_year,
            'year_zhi': year_zhi,
            'year_zhi_name': DI_ZHI_LIST[year_zhi - 1],
            'month': lunar_month,
            'day': lunar_day,
            'shi_ke': shi_ke,
            'shi_ke_name': DI_ZHI_LIST[shi_ke - 1]
        },
        'gua_info': gua_info,
    }


def random_divination():
    """
    随机起卦
    
    生成6个随机数（0-3）作为六爻
    
    Returns:
        dict: {
            'yao_list': 六爻列表,
            'moving_yao': 动爻位置(1-6)
        }
    """
    # 生成6个随机数
    yao_list = [random.randint(0, 3) for _ in range(6)]
    
    # 找出动爻（值为2或3的爻）
    moving_yao_list = [i + 1 for i, yao in enumerate(yao_list) if yao >= 2]
    
    # 如果没有动爻，随机选择一个
    if not moving_yao_list:
        moving_yao = random.randint(1, 6)
    else:
        moving_yao = random.choice(moving_yao_list)
    
    return {
        'yao_list': yao_list,
        'moving_yao': moving_yao
    }