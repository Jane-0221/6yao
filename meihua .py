# -*- coding: utf-8 -*-
"""
梅花易数起卦模块
时间起卦算法：
- 上卦 = (年+月+日) % 8，余数0取8
- 下卦 = (年+月+日+时) % 8，余数0取8
- 动爻 = (年+月+日+时) % 6，余数0取6
"""

import datetime
from lunarcalendar import Converter, Solar, Lunar

# 八卦对应表
GUA_NAMES = {
    1: "乾", 2: "兑", 3: "离", 4: "震",
    5: "巽", 6: "坎", 7: "艮", 8: "坤"
}

# 八卦二进制表示（从下到上）
GUA_BINARIES = {
    1: "111",  # 乾
    2: "110",  # 兑
    3: "101",  # 离
    4: "100",  # 震
    5: "011",  # 巽
    6: "010",  # 坎
    7: "001",  # 艮
    8: "000",  # 坤
}


def get_lunar_datetime(solar_date=None):
    """
    获取农历日期
    
    Args:
        solar_date: 阳历日期，默认为当前时间
    
    Returns:
        Lunar对象
    """
    if solar_date is None:
        solar_date = datetime.datetime.now()
    
    # 转换为农历
    solar = Solar(solar_date.year, solar_date.month, solar_date.day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar


def get_shi_ke(hour=None):
    """
    获取时辰数（1-12）
    
    Args:
        hour: 小时数，默认为当前小时
    
    Returns:
        时辰数（1-12），子时=1, 丑时=2, ..., 亥时=12
    """
    if hour is None:
        hour = datetime.datetime.now().hour
    
    # 将小时转换为时辰数（23-1点为子时=1，1-3点为丑时=2，以此类推）
    # 23点 -> 1, 0点 -> 1, 1点 -> 2, 2点 -> 2, ...
    if hour == 23 or hour == 0:
        return 1  # 子时
    else:
        return (hour + 1) // 2 + 1 if hour % 2 == 1 else (hour + 1) // 2


def time_divination(solar_date=None):
    """
    时间起卦（梅花易数）
    
    算法：
    - 上卦 = (年+月+日) % 8，余数0取8
    - 下卦 = (年+月+日+时) % 8，余数0取8
    - 动爻 = (年+月+日+时) % 6，余数0取6
    
    Args:
        solar_date: 阳历日期，默认为当前时间
    
    Returns:
        dict: {
            'upper_gua': 上卦(1-8),
            'lower_gua': 下卦(1-8),
            'moving_yao': 动爻位置(1-6),
            'yao_list': 六爻列表,
            'lunar': 农历日期信息
        }
    """
    # 获取农历日期
    lunar = get_lunar_datetime(solar_date)
    
    # 获取农历时间
    lunar_year = lunar.year
    lunar_month = lunar.month
    lunar_day = lunar.day
    
    # 获取时辰
    hour = datetime.datetime.now().hour if solar_date is None else solar_date.hour
    shi_ke = get_shi_ke(hour)
    
    # 计算上卦：(年 + 月 + 日) % 8
    upper_num = (lunar_year + lunar_month + lunar_day) % 8
    upper_gua = upper_num if upper_num != 0 else 8
    
    # 计算下卦：(年 + 月 + 日 + 时) % 8
    lower_num = (lunar_year + lunar_month + lunar_day + shi_ke) % 8
    lower_gua = lower_num if lower_num != 0 else 8
    
    # 计算动爻：(年 + 月 + 日 + 时) % 6
    moving_num = (lunar_year + lunar_month + lunar_day + shi_ke) % 6
    moving_yao = moving_num if moving_num != 0 else 6
    
    # 生成六爻列表
    yao_list = gua_to_yao_list(upper_gua, lower_gua)
    
    return {
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'moving_yao': moving_yao,
        'yao_list': yao_list,
        'lunar': {
            'year': lunar_year,
            'month': lunar_month,
            'day': lunar_day,
            'shi_ke': shi_ke
        }
    }


def gua_to_yao_list(upper_gua: int, lower_gua: int):
    """
    将上下卦转换为六爻列表
    
    Args:
        upper_gua: 上卦(1-8)
        lower_gua: 下卦(1-8)
    
    Returns:
        list: 六爻列表，0=阴爻，1=阳爻
    """
    # 获取上下卦的二进制表示
    upper_bin = GUA_BINARIES.get(upper_gua, "000")
    lower_bin = GUA_BINARIES.get(lower_gua, "000")
    
    # 组合成六爻（从下到上：下卦三位 + 上卦三位）
    yao_list = []
    
    # 下卦三位（初爻、二爻、三爻）
    for bit in lower_bin:
        yao_list.append(int(bit))
    
    # 上卦三位（四爻、五爻、上爻）
    for bit in upper_bin:
        yao_list.append(int(bit))
    
    return yao_list


def number_divination(upper_num: int, lower_num: int):
    """
    数字起卦
    
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
            'moving_yao': 动爻位置(1-6)
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
    
    return {
        'upper_num': upper_num,
        'lower_num': lower_num,
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'yao_list': yao_list,
        'moving_yao': moving_yao
    }


if __name__ == "__main__":
    # 测试时间起卦
    print("=" * 60)
    print("梅花易数时间起卦测试")
    print("=" * 60)
    
    result = time_divination()
    print(f"上卦: {result['upper_gua']} ({GUA_NAMES[result['upper_gua']]})")
    print(f"下卦: {result['lower_gua']} ({GUA_NAMES[result['lower_gua']]})")
    print(f"动爻: {result['moving_yao']}爻")
    print(f"六爻: {result['yao_list']}")
    print(f"农历: {result['lunar']['year']}年{result['lunar']['month']}月{result['lunar']['day']}日 时辰{result['lunar']['shi_ke']}")
    
    # 测试数字起卦
    print("\n" + "=" * 60)
    print("数字起卦测试")
    print("=" * 60)
    
    result = number_divination(9, 9)
    print(f"上卦数字: {result['upper_num']} -> {result['upper_gua']} ({GUA_NAMES[result['upper_gua']]})")
    print(f"下卦数字: {result['lower_num']} -> {result['lower_gua']} ({GUA_NAMES[result['lower_gua']]})")
    print(f"动爻: {result['moving_yao']}爻")
    print(f"六爻: {result['yao_list']}")