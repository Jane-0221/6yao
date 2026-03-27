# -*- coding: utf-8 -*-
"""
六爻起卦模块
三种起卦方式：
1. 标的物起卦（笔画+日时）
2. 随机起卦
3. 数字起卦（上下卦分开输入）
"""

import random
import datetime
from lunarcalendar import Converter, Solar, Lunar
from stroke_counter import get_text_stroke, get_traditional

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


def biao_di_wu_divination(name: str, solar_date=None):
    """
    标的物起卦（笔画+日时）
    
    算法：
    - 上卦 = (笔画数 + 农历年 + 农历月 + 农历日) % 8，余数0取8
    - 下卦 = (笔画数 + 农历时) % 8，余数0取8
    - 动爻 = (笔画数 + 农历年 + 农历月 + 农历日 + 农历时) % 6，余数0取6
    
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
            'lunar': 农历日期信息
        }
    """
    # 获取农历日期
    lunar = get_lunar_datetime(solar_date)
    
    # 转换为繁体字
    name_traditional = get_traditional(name)
    
    # 计算笔画数
    stroke = get_text_stroke(name)
    
    # 获取农历时间
    lunar_year = lunar.year
    lunar_month = lunar.month
    lunar_day = lunar.day
    
    # 获取当前时辰（简化：使用小时）
    hour = datetime.datetime.now().hour
    # 将小时转换为时辰（23-1点为子时，1-3点为丑时，以此类推）
    shi_ke = (hour + 1) // 2 % 12  # 0-11对应子-亥
    
    # 计算上下卦和动爻
    # 上卦：(笔画 + 年 + 月 + 日) % 8
    upper_num = (stroke + lunar_year + lunar_month + lunar_day) % 8
    upper_gua = upper_num if upper_num != 0 else 8
    
    # 下卦：(笔画 + 时辰) % 8
    lower_num = (stroke + shi_ke) % 8
    lower_gua = lower_num if lower_num != 0 else 8
    
    # 动爻：(笔画 + 年 + 月 + 日 + 时辰) % 6
    moving_num = (stroke + lunar_year + lunar_month + lunar_day + shi_ke) % 6
    moving_yao = moving_num if moving_num != 0 else 6
    
    # 生成六爻列表
    yao_list = gua_to_yao_list(upper_gua, lower_gua)
    
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
            'month': lunar_month,
            'day': lunar_day,
            'shi_ke': shi_ke
        }
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


def gua_to_yao_list(upper_gua: int, lower_gua: int):
    """
    将上下卦转换为六爻列表
    
    Args:
        upper_gua: 上卦(1-8)
        lower_gua: 下卦(1-8)
    
    Returns:
        list: 六爻列表 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
              0=少阴, 1=少阳, 2=老阴, 3=老阳
    """
    # 获取上下卦的二进制表示
    upper_bin = GUA_BINARIES.get(upper_gua, "000")
    lower_bin = GUA_BINARIES.get(lower_gua, "000")
    
    # 组合成六爻（从下到上：下卦三位 + 上卦三位）
    # lower_bin是下卦，从下往上是 low->mid->high
    # upper_bin是上卦，从下往上是 low->mid->high
    # 六爻顺序：初爻(二爻) -> 二爻 -> 三爻 -> 四爻 -> 五爻 -> 上爻(六爻)
    
    yao_list = []
    
    # 下卦三位（初爻、二爻、三爻）
    for bit in lower_bin:
        yao_list.append(int(bit) + 1)  # 0->1(少阳), 1->2(少阴)
    
    # 上卦三位（四爻、五爻、上爻）
    for bit in upper_bin:
        yao_list.append(int(bit) + 1)
    
    return yao_list


def get_yao_description(yao_list):
    """
    获取六爻描述
    
    Args:
        yao_list: 六爻列表
    
    Returns:
        list: 描述列表
    """
    descriptions = []
    yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
    
    for i, yao in enumerate(yao_list):
        if yao == 0:
            desc = "少阴（阴爻，静）"
        elif yao == 1:
            desc = "少阳（阳爻，静）"
        elif yao == 2:
            desc = "老阴（阴爻，动→变阳）"
        elif yao == 3:
            desc = "老阳（阳爻，动→变阴）"
        else:
            desc = "未知"
        
        descriptions.append(f"{yao_names[i]}: {desc}")
    
    return descriptions


def test_divination():
    """测试所有起卦方式"""
    print("=" * 60)
    print("标的物起卦测试")
    print("=" * 60)
    
    result = biao_di_wu_divination("股票")
    print(f"标的物(简体): {result['name']}")
    print(f"标的物(繁体): {result['name_traditional']}")
    print(f"笔画数: {result['stroke']}")
    print(f"上卦: {result['upper_gua']} ({GUA_NAMES[result['upper_gua']]})")
    print(f"下卦: {result['lower_gua']} ({GUA_NAMES[result['lower_gua']]})")
    print(f"动爻: {result['moving_yao']}爻")
    print(f"六爻: {result['yao_list']}")
    print(f"农历: {result['lunar']}")
    
    print("\n" + "=" * 60)
    print("随机起卦测试")
    print("=" * 60)
    
    result = random_divination()
    print(f"六爻: {result['yao_list']}")
    print(f"动爻: {result['moving_yao']}爻")
    
    print("\n" + "=" * 60)
    print("数字起卦测试")
    print("=" * 60)
    
    result = number_divination_v2(9, 9)
    print(f"上卦数字: {result['upper_num']} -> {result['upper_gua']} ({GUA_NAMES[result['upper_gua']]})")
    print(f"下卦数字: {result['lower_num']} -> {result['lower_gua']} ({GUA_NAMES[result['lower_gua']]})")
    print(f"动爻: {result['moving_yao']}爻")
    print(f"六爻: {result['yao_list']}")


if __name__ == "__main__":
    test_divination()