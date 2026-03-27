# -*- coding: utf-8 -*-
"""
64卦核心算法模块

根据六爻数组计算本卦和变卦。

核心规则：
1. 六爻数组格式：[初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
2. 爻值定义：1 = 阳爻，2 = 阴爻
3. 卦象拆分：下卦 = [0:3]，上卦 = [3:6]
4. 动爻位置：1-6（1=初爻，6=上爻），支持单动爻和多动爻
"""

from typing import Union, List, Dict, Tuple, Optional

# =============================================================================
# 常量定义
# =============================================================================

# 八卦二进制到卦名映射（严格按照用户提供的对应表）
# 格式：(初爻, 二爻, 三爻) -> 卦名
TRIGRAM_NAMES = {
    (1, 1, 1): "乾",  # ☰ 天
    (1, 1, 2): "兑",  # ☱ 泽
    (1, 2, 1): "离",  # ☲ 火
    (1, 2, 2): "震",  # ☳ 雷
    (2, 1, 1): "巽",  # ☴ 风
    (2, 1, 2): "坎",  # ☵ 水
    (2, 2, 1): "艮",  # ☶ 山
    (2, 2, 2): "坤",  # ☷ 地
}

# 八卦到自然象映射
TRIGRAM_NATURES = {
    "乾": "天",
    "兑": "泽",
    "离": "火",
    "震": "雷",
    "巽": "风",
    "坎": "水",
    "艮": "山",
    "坤": "地",
}

# 64卦名称映射表
# 格式：(上卦名, 下卦名) -> 64卦专名
GUA64_NAMES = {
    # 乾宫八卦（上卦为乾）
    ("乾", "乾"): "乾为天",
    ("乾", "兑"): "天泽履",
    ("乾", "离"): "天火同人",
    ("乾", "震"): "天雷无妄",
    ("乾", "巽"): "天风姤",
    ("乾", "坎"): "天水讼",
    ("乾", "艮"): "天山遁",
    ("乾", "坤"): "天地否",
    
    # 兑宫八卦（上卦为兑）
    ("兑", "乾"): "泽天夬",
    ("兑", "兑"): "兑为泽",
    ("兑", "离"): "泽火革",
    ("兑", "震"): "泽雷随",
    ("兑", "巽"): "泽风大过",
    ("兑", "坎"): "泽水困",
    ("兑", "艮"): "泽山咸",
    ("兑", "坤"): "泽地萃",
    
    # 离宫八卦（上卦为离）
    ("离", "乾"): "火天大有",
    ("离", "兑"): "火泽睽",
    ("离", "离"): "离为火",
    ("离", "震"): "火雷噬嗑",
    ("离", "巽"): "火风鼎",
    ("离", "坎"): "火水未济",
    ("离", "艮"): "火山旅",
    ("离", "坤"): "火地晋",
    
    # 震宫八卦（上卦为震）
    ("震", "乾"): "雷天大壮",
    ("震", "兑"): "雷泽归妹",
    ("震", "离"): "雷火丰",
    ("震", "震"): "震为雷",
    ("震", "巽"): "雷风恒",
    ("震", "坎"): "雷水解",
    ("震", "艮"): "雷山小过",
    ("震", "坤"): "雷地豫",
    
    # 巽宫八卦（上卦为巽）
    ("巽", "乾"): "风天小畜",
    ("巽", "兑"): "风泽中孚",
    ("巽", "离"): "风火家人",
    ("巽", "震"): "风雷益",
    ("巽", "巽"): "巽为风",
    ("巽", "坎"): "风水涣",
    ("巽", "艮"): "风山渐",
    ("巽", "坤"): "风地观",
    
    # 坎宫八卦（上卦为坎）
    ("坎", "乾"): "水天需",
    ("坎", "兑"): "水泽节",
    ("坎", "离"): "水火既济",
    ("坎", "震"): "水雷屯",
    ("坎", "巽"): "水风井",
    ("坎", "坎"): "坎为水",
    ("坎", "艮"): "水山蹇",
    ("坎", "坤"): "水地比",
    
    # 艮宫八卦（上卦为艮）
    ("艮", "乾"): "山天大畜",
    ("艮", "兑"): "山泽损",
    ("艮", "离"): "山火贲",
    ("艮", "震"): "山雷颐",
    ("艮", "巽"): "山风蛊",
    ("艮", "坎"): "山水蒙",
    ("艮", "艮"): "艮为山",
    ("艮", "坤"): "山地剥",
    
    # 坤宫八卦（上卦为坤）
    ("坤", "乾"): "地天泰",
    ("坤", "兑"): "地泽临",
    ("坤", "离"): "地火明夷",
    ("坤", "震"): "地雷复",
    ("坤", "巽"): "地风升",
    ("坤", "坎"): "地水师",
    ("坤", "艮"): "地山谦",
    ("坤", "坤"): "坤为地",
}

# 爻位名称
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


# =============================================================================
# 核心函数
# =============================================================================

def validate_yao_list(yao_list: list) -> bool:
    """
    验证六爻数组是否有效
    
    Args:
        yao_list: 六爻数组
    
    Returns:
        bool: 是否有效
    
    Raises:
        ValueError: 无效时抛出异常
    """
    if not isinstance(yao_list, list):
        raise ValueError(f"六爻数组必须是列表类型，当前类型: {type(yao_list)}")
    
    if len(yao_list) != 6:
        raise ValueError(f"六爻数组必须包含6个元素，当前数量: {len(yao_list)}")
    
    for i, yao in enumerate(yao_list):
        if yao not in (1, 2):
            raise ValueError(
                f"爻值必须是1(阳)或2(阴)，第{i+1}爻值为: {yao}"
            )
    
    return True


def normalize_moving_yao(moving_yao: Union[int, List[int], None]) -> List[int]:
    """
    标准化动爻参数为列表格式
    
    支持三种输入格式：
    - int: 单个动爻位置（1-6）
    - list[int]: 多个动爻位置
    - None: 无动爻
    
    Args:
        moving_yao: 动爻位置
    
    Returns:
        list: 动爻位置列表（可能为空列表）
    
    Examples:
        >>> normalize_moving_yao(3)
        [3]
        >>> normalize_moving_yao([3, 5])
        [3, 5]
        >>> normalize_moving_yao(None)
        []
    """
    if moving_yao is None:
        return []
    
    if isinstance(moving_yao, int):
        if moving_yao < 1 or moving_yao > 6:
            raise ValueError(f"动爻位置必须在1-6之间，当前值: {moving_yao}")
        return [moving_yao]
    
    if isinstance(moving_yao, list):
        for pos in moving_yao:
            if not isinstance(pos, int):
                raise ValueError(f"动爻位置必须是整数，当前类型: {type(pos)}")
            if pos < 1 or pos > 6:
                raise ValueError(f"动爻位置必须在1-6之间，当前值: {pos}")
        # 去重并排序
        return sorted(list(set(moving_yao)))
    
    raise ValueError(
        f"动爻参数类型错误，支持int/list/None，当前类型: {type(moving_yao)}"
    )


def get_trigram_name(trigram: Tuple[int, int, int]) -> str:
    """
    根据三爻数组获取卦名
    
    Args:
        trigram: 三爻数组，如 (1, 1, 1)
    
    Returns:
        str: 卦名，如 "乾"
    
    Raises:
        ValueError: 无效的三爻数组
    """
    if trigram not in TRIGRAM_NAMES:
        raise ValueError(f"无效的三爻数组: {trigram}")
    return TRIGRAM_NAMES[trigram]


def get_trigram_nature(gua_name: str) -> str:
    """
    根据卦名获取自然象
    
    Args:
        gua_name: 卦名，如 "乾"
    
    Returns:
        str: 自然象，如 "天"
    """
    if gua_name not in TRIGRAM_NATURES:
        raise ValueError(f"无效的卦名: {gua_name}")
    return TRIGRAM_NATURES[gua_name]


def parse_yao_list(yao_list: list) -> dict:
    """
    解析六爻数组，返回上下卦信息
    
    Args:
        yao_list: 六爻数组 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
    
    Returns:
        dict: 包含上下卦信息的字典
    
    Examples:
        >>> parse_yao_list([1, 1, 1, 2, 1, 1])
        {
            'lower_trigram': (1, 1, 1),
            'upper_trigram': (2, 1, 1),
            'lower_gua_name': '乾',
            'upper_gua_name': '巽',
            'lower_nature': '天',
            'upper_nature': '风',
        }
    """
    # 验证输入
    validate_yao_list(yao_list)
    
    # 拆分上下卦
    lower_trigram = tuple(yao_list[0:3])  # 下卦（内卦）
    upper_trigram = tuple(yao_list[3:6])  # 上卦（外卦）
    
    # 获取卦名和自然象
    lower_gua_name = get_trigram_name(lower_trigram)
    upper_gua_name = get_trigram_name(upper_trigram)
    lower_nature = get_trigram_nature(lower_gua_name)
    upper_nature = get_trigram_nature(upper_gua_name)
    
    return {
        'lower_trigram': lower_trigram,
        'upper_trigram': upper_trigram,
        'lower_gua_name': lower_gua_name,
        'upper_gua_name': upper_gua_name,
        'lower_nature': lower_nature,
        'upper_nature': upper_nature,
    }


def get_gua64_name(upper_gua: str, lower_gua: str) -> str:
    """
    根据上下卦名获取64卦专名
    
    Args:
        upper_gua: 上卦名
        lower_gua: 下卦名
    
    Returns:
        str: 64卦专名，如 "小畜"
    """
    key = (upper_gua, lower_gua)
    if key not in GUA64_NAMES:
        raise ValueError(f"无效的卦组合: 上卦={upper_gua}, 下卦={lower_gua}")
    return GUA64_NAMES[key]


def format_gua_full_name(upper_gua: str, lower_gua: str) -> str:
    """
    生成完整的卦名
    
    命名规则：
    - 异卦（上下卦不同）：上{上卦名}下{下卦名} {GUA64_NAMES中的名称}卦
    - 八纯卦（上下卦相同）：上{上卦名}下{下卦名} {卦名}为{自然象}卦
    
    Args:
        upper_gua: 上卦名
        lower_gua: 下卦名
    
    Returns:
        str: 完整卦名
    """
    upper_nature = get_trigram_nature(upper_gua)
    
    if upper_gua == lower_gua:
        # 八纯卦
        return f"上{upper_gua}下{lower_gua} {upper_gua}为{upper_nature}卦"
    else:
        # 异卦：GUA64_NAMES中存储的是如"风天小畜"、"天山遁"等
        gua64_name = get_gua64_name(upper_gua, lower_gua)
        return f"上{upper_gua}下{lower_gua} {gua64_name}卦"


def flip_yao(yao_list: list, moving_yao_list: List[int]) -> list:
    """
    反转动爻位置的爻值（1↔2）
    
    注意：动爻位置是1-6，需要转换为数组索引0-5
    
    Args:
        yao_list: 原始六爻数组
        moving_yao_list: 动爻位置列表（1-6）
    
    Returns:
        list: 反转后的新六爻数组
    """
    new_yao_list = yao_list.copy()
    
    for pos in moving_yao_list:
        # 索引转换：动爻位置1-6 → 数组索引0-5
        index = pos - 1
        
        # 反转爻值：1→2, 2→1
        if new_yao_list[index] == 1:
            new_yao_list[index] = 2
        else:
            new_yao_list[index] = 1
    
    return new_yao_list


def generate_change_detail(
    yao_list: list, 
    new_yao_list: list, 
    moving_yao_list: List[int],
    old_lower_gua: str,
    old_upper_gua: str,
    new_lower_gua: str,
    new_upper_gua: str
) -> str:
    """
    生成变化详情描述
    
    Args:
        yao_list: 原始六爻数组
        new_yao_list: 变化后的六爻数组
        moving_yao_list: 动爻位置列表
        old_lower_gua: 原下卦名
        old_upper_gua: 原上卦名
        new_lower_gua: 新下卦名
        new_upper_gua: 新上卦名
    
    Returns:
        str: 变化详情描述
    """
    details = []
    
    for pos in moving_yao_list:
        index = pos - 1
        old_value = yao_list[index]
        new_value = new_yao_list[index]
        yao_name = YAO_NAMES[index]
        
        old_type = "阳" if old_value == 1 else "阴"
        new_type = "阳" if new_value == 1 else "阴"
        
        details.append(f"{yao_name}{old_type}变{new_type}")
    
    # 判断上下卦变化
    gua_changes = []
    if old_lower_gua != new_lower_gua:
        gua_changes.append(f"下卦由{old_lower_gua}变为{new_lower_gua}")
    if old_upper_gua != new_upper_gua:
        gua_changes.append(f"上卦由{old_upper_gua}变为{new_upper_gua}")
    
    result = "，".join(details)
    if gua_changes:
        result += "，" + "，".join(gua_changes)
    
    return result


def calculate_ben_gua(yao_list: list) -> dict:
    """
    计算本卦
    
    Args:
        yao_list: 六爻数组
    
    Returns:
        dict: 本卦信息
    """
    parsed = parse_yao_list(yao_list)
    
    upper_gua = parsed['upper_gua_name']
    lower_gua = parsed['lower_gua_name']
    
    return {
        'name': format_gua_full_name(upper_gua, lower_gua),
        'upper_gua': upper_gua,
        'lower_gua': lower_gua,
        'upper_nature': parsed['upper_nature'],
        'lower_nature': parsed['lower_nature'],
        'gua64_name': get_gua64_name(upper_gua, lower_gua),
        'upper_trigram': parsed['upper_trigram'],
        'lower_trigram': parsed['lower_trigram'],
    }


def calculate_bian_gua(
    yao_list: list, 
    moving_yao: Union[int, List[int], None]
) -> Optional[dict]:
    """
    计算变卦
    
    Args:
        yao_list: 六爻数组
        moving_yao: 动爻位置（支持int/list/None）
    
    Returns:
        dict: 变卦信息，无动爻时返回None
    """
    # 标准化动爻参数
    moving_yao_list = normalize_moving_yao(moving_yao)
    
    if not moving_yao_list:
        return None
    
    # 获取本卦信息
    ben_parsed = parse_yao_list(yao_list)
    
    # 反转动爻
    new_yao_list = flip_yao(yao_list, moving_yao_list)
    
    # 计算变卦
    bian_parsed = parse_yao_list(new_yao_list)
    
    new_upper_gua = bian_parsed['upper_gua_name']
    new_lower_gua = bian_parsed['lower_gua_name']
    
    # 生成变化详情
    change_detail = generate_change_detail(
        yao_list, 
        new_yao_list, 
        moving_yao_list,
        ben_parsed['lower_gua_name'],
        ben_parsed['upper_gua_name'],
        new_lower_gua,
        new_upper_gua
    )
    
    return {
        'name': format_gua_full_name(new_upper_gua, new_lower_gua),
        'upper_gua': new_upper_gua,
        'lower_gua': new_lower_gua,
        'upper_nature': bian_parsed['upper_nature'],
        'lower_nature': bian_parsed['lower_nature'],
        'gua64_name': get_gua64_name(new_upper_gua, new_lower_gua),
        'upper_trigram': bian_parsed['upper_trigram'],
        'lower_trigram': bian_parsed['lower_trigram'],
        'changed_yao': moving_yao_list,
        'change_detail': change_detail,
        'new_yao_list': new_yao_list,
    }


def calculate_gua(
    yao_list: list, 
    moving_yao: Union[int, List[int], None] = None
) -> dict:
    """
    主函数：计算本卦和变卦
    
    Args:
        yao_list: 六爻数组 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
        moving_yao: 动爻位置（可选），支持：
            - int: 单个动爻（如 3）
            - list[int]: 多个动爻（如 [3, 5]）
            - None: 无动爻
    
    Returns:
        dict: 包含本卦和变卦信息的字典
    
    Examples:
        >>> result = calculate_gua([1, 1, 1, 2, 1, 1])
        >>> print(result['ben_gua']['name'])
        '上巽下乾 风天小畜卦'
        
        >>> result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
        >>> print(result['bian_gua']['name'])
        '上乾下艮 天山遁卦'
    """
    # 验证输入
    validate_yao_list(yao_list)
    
    # 标准化动爻参数
    moving_yao_list = normalize_moving_yao(moving_yao)
    
    # 计算本卦
    ben_gua = calculate_ben_gua(yao_list)
    
    # 计算变卦
    bian_gua = calculate_bian_gua(yao_list, moving_yao_list)
    
    return {
        'ben_gua': ben_gua,
        'bian_gua': bian_gua,
        'yao_list': yao_list,
        'moving_yao': moving_yao_list if moving_yao_list else None,
    }


# =============================================================================
# 测试代码
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("64卦算法测试")
    print("=" * 60)
    
    # 测试用例1：无动爻
    print("\n【测试1】无动爻")
    result1 = calculate_gua([1, 1, 1, 2, 1, 1])
    print(f"六爻: {result1['yao_list']}")
    print(f"本卦: {result1['ben_gua']['name']}")
    print(f"变卦: {result1['bian_gua']}")
    
    # 测试用例2：有动爻
    print("\n【测试2】有动爻（三爻动）")
    result2 = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    print(f"六爻: {result2['yao_list']}")
    print(f"本卦: {result2['ben_gua']['name']}")
    print(f"变卦: {result2['bian_gua']['name']}")
    print(f"变化: {result2['bian_gua']['change_detail']}")
    
    # 测试用例3：八纯卦
    print("\n【测试3】八纯卦（乾为天）")
    result3 = calculate_gua([1, 1, 1, 1, 1, 1])
    print(f"六爻: {result3['yao_list']}")
    print(f"本卦: {result3['ben_gua']['name']}")
    
    # 测试用例4：多动爻
    print("\n【测试4】多动爻（三爻、五爻动）")
    result4 = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=[3, 5])
    print(f"六爻: {result4['yao_list']}")
    print(f"本卦: {result4['ben_gua']['name']}")
    print(f"变卦: {result4['bian_gua']['name']}")
    print(f"变化: {result4['bian_gua']['change_detail']}")