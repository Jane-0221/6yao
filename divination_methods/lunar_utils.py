# -*- coding: utf-8 -*-
"""
农历辅助函数模块

包含：
- 农历日期转换
- 年支数计算
- 日天干计算
- 时辰数计算
- 地支/天干常量
"""

import datetime
from lunarcalendar import Converter, Solar, Lunar

# 地支对应数字
DI_ZHI = {
    "子": 1, "丑": 2, "寅": 3, "卯": 4, "辰": 5, "巳": 6,
    "午": 7, "未": 8, "申": 9, "酉": 10, "戌": 11, "亥": 12
}

# 地支列表（用于计算年支）
DI_ZHI_LIST = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干列表（用于计算日天干）
TIAN_GAN_LIST = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]


def get_lunar_datetime(solar_date=None, hour=None):
    """
    获取农历日期（支持子时跨日）
    
    子时规则：23:00-01:00 属于下一天
    - 23:00-23:59（晚子时）→ 使用下一天的农历日期
    - 00:00-00:59（早子时）→ 使用当天的农历日期
    
    Args:
        solar_date: 阳历日期，默认为当前时间
        hour: 小时数，默认从solar_date提取
    
    Returns:
        Lunar对象
    """
    if solar_date is None:
        solar_date = datetime.datetime.now()
    
    if hour is None:
        hour = solar_date.hour
    
    # 子时晚子时（23:00-23:59）属于下一天
    if hour == 23:
        solar_date = solar_date + datetime.timedelta(days=1)
    
    # 转换为农历
    solar = Solar(solar_date.year, solar_date.month, solar_date.day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar


def get_year_zhi(lunar_year):
    """
    获取年支数（地支数）
    
    Args:
        lunar_year: 农历年份
    
    Returns:
        年支数（1-12），子=1, 丑=2, ..., 亥=12
    """
    # 年支计算：(年份 - 4) % 12
    # 1984年是甲子年，所以用 (year - 4) % 12
    zhi_index = (lunar_year - 4) % 12
    return zhi_index + 1  # 返回1-12


def get_day_tiangan(solar_date=None):
    """
    获取日天干
    
    用于六神排盘，根据日期计算当日的天干。
    
    天干计算公式：
    - 使用公历日期计算日干支
    - 日天干 = (日数 + 偏移量) % 10
    
    Args:
        solar_date: 阳历日期，默认为当前时间
    
    Returns:
        str: 天干（甲、乙、丙、丁、戊、己、庚、辛、壬、癸）
    """
    if solar_date is None:
        solar_date = datetime.datetime.now()
    
    # 使用lunarcalendar库获取农历日期的干支信息
    solar = Solar(solar_date.year, solar_date.month, solar_date.day)
    lunar = Converter.Solar2Lunar(solar)
    
    # 获取日干支（lunarcalendar库提供的方法）
    # 日天干计算：基于公历日期
    # 参考公式：G = 4C + [C/4] + 5y + [y/4] + [3*(M+1)/5] + d - 3
    # 简化：使用lunarcalendar库的干支计算
    
    # 计算日天干索引（0-9对应甲-癸）
    # 使用基准日期1900年1月1日（甲戌日，天干索引0）
    base_date = datetime.datetime(1900, 1, 1)
    delta_days = (solar_date - base_date).days
    
    # 1900年1月1日是甲日，天干索引从0开始
    # 由于1900年1月1日实际是甲戌日，天干为甲（索引0）
    tiangan_index = delta_days % 10
    
    return TIAN_GAN_LIST[tiangan_index]


def get_shi_ke(hour=None):
    """
    获取时辰数（1-12）
    
    Args:
        hour: 小时数，默认为当前小时
    
    Returns:
        时辰数（1-12），子=1, 丑=2, ..., 亥=12
    """
    if hour is None:
        hour = datetime.datetime.now().hour
    
    # 将小时转换为时辰数
    # 23-1点为子时=1，1-3点为丑时=2，...，21-23点为亥时=12
    if hour == 23:
        return 1  # 子时
    else:
        return (hour // 2) + 1