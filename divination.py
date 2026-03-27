# -*- coding: utf-8 -*-
"""
六爻起卦模块
四种起卦方式：
1. 时间起卦（梅花易数）
2. 标的物起卦（笔画+日时）
3. 随机起卦
4. 数字起卦（上下卦分开输入）

梅花易数算法：
- 上卦 = (Xo+Xi+Xj+Xy) % 8，余数0取8
- 下卦 = (Xo+Xi+Xj+Xy+Xu) % 8，余数0取8
- 动爻 = (Xo+Xi+Xj+Xy+Xu) % 6，余数0取6

其中：
- Xo = 繁体笔画数
- Xi = 年支数（子1、丑2、寅3、卯4、辰5、巳6、午7、未8、申9、酉10、戌11、亥12）
- Xj = 农历月数
- Xy = 农历日数
- Xu = 时辰数（子1、丑2、寅3、卯4、辰5、巳6、午7、未8、申9、酉10、戌11、亥12）
"""

import random
import datetime
from lunarcalendar import Converter, Solar, Lunar
from stroke_counter import get_text_stroke, get_traditional
from gua64 import calculate_gua

# 八卦对应表（先天八卦数）
GUA_NAMES = {
    1: "乾", 2: "兑", 3: "离", 4: "震",
    5: "巽", 6: "坎", 7: "艮", 8: "坤"
}

# 八卦二进制表示（从下到上，0=阴爻，1=阳爻）
GUA_BINARIES = {
    1: "111",  # 乾 ☰
    2: "110",  # 兑 ☱
    3: "101",  # 离 ☲
    4: "100",  # 震 ☳
    5: "011",  # 巽 ☴
    6: "010",  # 坎 ☵
    7: "001",  # 艮 ☶
    8: "000",  # 坤 ☷
}

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
            'lunar': 农历日期信息
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
            'lunar': 农历日期信息
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


def coin_toss_to_yao(coin_results):
    """
    将一次抛三枚硬币的结果转换为一爻
    
    六爻金钱卦规则（以少为尊）：
    - 3个阳面（正面）= 老阳（阳爻动）→ 爻值=1（阳），is_moving=True
    - 2个阳面（正面）= 少阴（阴爻静）→ 爻值=2（阴），is_moving=False
      （2正1反，反为少，故阴）
    - 1个阳面（正面）= 少阳（阳爻静）→ 爻值=1（阳），is_moving=False
      （1正2反，正为少，故阳）
    - 0个阳面（正面）= 老阴（阴爻动）→ 爻值=2（阴），is_moving=True
    
    Args:
        coin_results: list[bool] - 三个布尔值，True=正面（阳），False=反面（阴）
    
    Returns:
        tuple: (爻值, 是否动爻, 爻类型名称)
            爻值: 1=阳爻, 2=阴爻
            是否动爻: True=动爻, False=静爻
            爻类型名称: "老阳"/"少阳"/"少阴"/"老阴"
    """
    heads_count = sum(coin_results)  # 正面（阳面）数量
    
    if heads_count == 3:
        return (1, True, "老阳")   # 老阳：阳爻动
    elif heads_count == 2:
        return (2, False, "少阴")  # 少阴：阴爻静（以少为尊，2正1反，反为少，故阴）
    elif heads_count == 1:
        return (1, False, "少阳")  # 少阳：阳爻静（以少为尊，1正2反，正为少，故阳）
    else:  # heads_count == 0
        return (2, True, "老阴")   # 老阴：阴爻动


def coin_divination(coin_results_list):
    """
    硬币起卦
    
    Args:
        coin_results_list: list[list[bool]] - 6次抛硬币结果，每次3个布尔值
            例如: [[True, True, False], [True, False, False], ...]
            True=正面，False=反面
            顺序：第1个列表=上爻，第6个列表=初爻（从上到下）
    
    Returns:
        dict: {
            'yao_list': 六爻列表 [上爻, 五爻, 四爻, 三爻, 二爻, 初爻],
            'moving_yao_list': 动爻位置列表,
            'coin_details': 每次抛硬币的详细信息
        }
    """
    yao_list = []
    coin_details = []
    
    # 硬币起卦的爻名顺序：从上爻到初爻
    yao_names = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
    
    for i, coin_results in enumerate(coin_results_list):
        yao_value, is_moving, yao_type = coin_toss_to_yao(coin_results)
        yao_list.append(yao_value)
        
        # 记录详细信息
        heads_count = sum(coin_results)
        tails_count = 3 - heads_count
        
        # 根据爻类型生成描述
        if yao_type == "老阳":
            yao_desc = "老阳（阳爻，动→变阴）"
        elif yao_type == "少阳":
            yao_desc = "少阳（阳爻，静）"
        elif yao_type == "少阴":
            yao_desc = "少阴（阴爻，静）"
        else:  # 老阴
            yao_desc = "老阴（阴爻，动→变阳）"
        
        # 爻位置：上爻=6, 五爻=5, 四爻=4, 三爻=3, 二爻=2, 初爻=1
        yao_position = 6 - i
        
        coin_details.append({
            'yao_name': yao_names[i],
            'yao_index': yao_position,
            'coin_results': coin_results,
            'heads_count': heads_count,
            'tails_count': tails_count,
            'yao_value': yao_value,
            'yao_type': yao_type,
            'yao_desc': yao_desc,
            'is_moving': is_moving
        })
    
    # 找出所有动爻（返回爻位置，如6=上爻, 1=初爻）
    moving_yao_list = [detail['yao_index'] for detail in coin_details if detail['is_moving']]
    
    # 计算卦象 - 需要将yao_list转换为从初爻到上爻的顺序
    yao_list_reversed = list(reversed(yao_list))
    moving_yao_list_reversed = [7 - y for y in moving_yao_list] if moving_yao_list else None
    gua_info = calculate_gua(yao_list_reversed, moving_yao_list_reversed)
    
    return {
        'yao_list': yao_list,
        'moving_yao_list': moving_yao_list,
        'coin_details': coin_details,
        'gua_info': gua_info,
    }


def auto_coin_divination():
    """
    系统自动抛硬币起卦
    
    自动模拟三枚硬币抛6次
    
    Returns:
        dict: 同 coin_divination
    """
    coin_results_list = []
    for _ in range(6):
        # 每次抛三枚硬币，True=正面，False=反面
        coin_results = [random.choice([True, False]) for _ in range(3)]
        coin_results_list.append(coin_results)
    
    return coin_divination(coin_results_list)


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


def gua_to_yao_list(upper_gua: int, lower_gua: int):
    """
    将上下卦转换为六爻列表
    
    六爻排盘规则：
    - 从下往上数：初爻（1爻）为最下方，上爻（6爻）为最上方
    - 下卦（内卦）是初、二、三爻
    - 上卦（外卦）是四、五、上爻
    
    Args:
        upper_gua: 上卦(1-8)，对应外卦（四、五、上爻）
        lower_gua: 下卦(1-8)，对应内卦（初、二、三爻）
    
    Returns:
        list: 六爻列表 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
              1=少阳（阳爻）, 2=少阴（阴爻）
    """
    # 获取上下卦的二进制表示（从下到上）
    # 例如：乾=111（三阳爻），坤=000（三阴爻）
    upper_bin = GUA_BINARIES.get(upper_gua, "000")
    lower_bin = GUA_BINARIES.get(lower_gua, "000")
    
    # 组合成六爻（从下到上：下卦三位 + 上卦三位）
    yao_list = []
    
    # 下卦三位（初爻、二爻、三爻）
    # 二进制中：1=阳爻->少阳(1), 0=阴爻->少阴(2)
    for bit in lower_bin:
        if bit == '1':
            yao_list.append(1)  # 阳爻 -> 少阳
        else:
            yao_list.append(2)  # 阴爻 -> 少阴
    
    # 上卦三位（四爻、五爻、上爻）
    for bit in upper_bin:
        if bit == '1':
            yao_list.append(1)  # 阳爻 -> 少阳
        else:
            yao_list.append(2)  # 阴爻 -> 少阴
    
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
    print("时间起卦测试（梅花易数）")
    print("=" * 60)
    
    result = time_divination()
    print(f"上卦: {result['upper_gua']} ({GUA_NAMES[result['upper_gua']]})")
    print(f"下卦: {result['lower_gua']} ({GUA_NAMES[result['lower_gua']]})")
    print(f"动爻: {result['moving_yao']}爻")
    print(f"六爻: {result['yao_list']}")
    print(f"农历: {result['lunar']}")
    
    print("\n" + "=" * 60)
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