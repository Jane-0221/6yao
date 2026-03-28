# -*- coding: utf-8 -*-
"""
标的物起卦模块（笔画+日时）

使用梅花易数算法，笔画数作为额外参数加入计算

算法：
- 上卦 = (Xo + Xi + Xj + Xy) % 8，余数0取8
- 下卦 = (Xo + Xi + Xj + Xy + Xu) % 8，余数0取8
- 动爻 = (Xo + Xi + Xj + Xy + Xu) % 6，余数0取6

其中：
- Xo = 繁体笔画数
- Xi = 年支数（子1、丑2、寅3、卯4、辰5、巳6、午7、未8、申9、酉10、戌11、亥12）
- Xj = 农历月数
- Xy = 农历日数
- Xu = 时辰数（子1、丑2、...、亥12）
"""

import datetime
from gua64 import calculate_gua
from .lunar_utils import get_lunar_datetime, get_year_zhi, get_shi_ke, DI_ZHI_LIST
from .stroke_counter import get_text_stroke, get_traditional
from .utils import gua_to_yao_list, GUA_NAMES


def biao_di_wu_divination(name: str, solar_date=None):
    """
    标的物起卦（笔画+日时）
    
    使用梅花易数算法，笔画数作为额外参数加入计算
    
    算法：
    - 上卦 = (Xo + Xi + Xj + Xy) % 8，余数0取8
    - 下卦 = (Xo + Xi + Xj + Xy + Xu) % 8，余数0取8
    - 动爻 = (Xo + Xi + Xj + Xy + Xu) % 6，余数0取6
    
    其中：
    - Xo = 繁体笔画数
    - Xi = 年支数（子1、丑2、寅3、卯4、辰5、巳6、午7、未8、申9、酉10、戌11、亥12）
    - Xj = 农历月数
    - Xy = 农历日数
    - Xu = 时辰数（子1、丑2、...、亥12）
    
    Args:
        name: 标的物名称（简体）
        solar_date: 阳历日期，默认为当前时间
    
    Returns:
        dict: {
            'name': 标的物名称(简体),
            'name_traditional': 标的物名称(繁体),
            'stroke': 笔画数,
            'upper_gua': 上卦(1-8),
            'lower_gua': 下卦(1-8),
            'yao_list': 六爻列表,
            'moving_yao': 动爻位置(1-6),
            'lunar': 农历日期信息,
            'gua_info': 卦象信息
        }
    """
    # 获取小时数
    hour = datetime.datetime.now().hour if solar_date is None else solar_date.hour
    
    # 获取农历日期（传入hour参数以支持子时跨日）
    lunar = get_lunar_datetime(solar_date, hour)
    
    # 转换为繁体字
    name_traditional = get_traditional(name)
    
    # 计算笔画数 Xo
    stroke = get_text_stroke(name)
    
    # 获取农历时间
    lunar_year = lunar.year
    lunar_month = lunar.month
    lunar_day = lunar.day
    
    # 获取年支数 Xi
    year_zhi = get_year_zhi(lunar_year)
    
    # 获取时辰数 Xu
    shi_ke = get_shi_ke(hour)
    
    # 计算上卦：(Xo + Xi + Xj + Xy) % 8
    upper_num = (stroke + year_zhi + lunar_month + lunar_day) % 8
    upper_gua = upper_num if upper_num != 0 else 8
    
    # 计算下卦：(Xo + Xi + Xj + Xy + Xu) % 8
    lower_num = (stroke + year_zhi + lunar_month + lunar_day + shi_ke) % 8
    lower_gua = lower_num if lower_num != 0 else 8
    
    # 计算动爻：(Xo + Xi + Xj + Xy + Xu) % 6
    moving_num = (stroke + year_zhi + lunar_month + lunar_day + shi_ke) % 6
    moving_yao = moving_num if moving_num != 0 else 6
    
    # 生成六爻列表
    yao_list = gua_to_yao_list(upper_gua, lower_gua)
    
    # 计算卦象
    gua_info = calculate_gua(yao_list, moving_yao)
    
    return {
        'name': name,
        'name_traditional': name_traditional,
        'stroke': stroke,
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'yao_list': yao_list,
        'moving_yao': moving_yao,
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