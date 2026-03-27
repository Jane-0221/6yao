# -*- coding: utf-8 -*-
"""
世应推算核心算法模块

根据六爻正统规则，实现64卦世应位置自动推算。

核心规则（不可修改）：
1. 世应唯一绑定卦象：同一个卦，世爻、应爻位置永远固定不变
2. 应爻计算公式：应爻位置 = 世爻位置 + 3（若结果 > 6，则减 6）
3. 八宫卦序与世位固定对应

使用示例:
    from shi_ying import get_shi_ying
    
    result = get_shi_ying("乾为天")
    print(result)  # {"shi": 6, "ying": 3}
"""

from typing import Dict

# =============================================================================
# 常量定义（正统规则，不可修改）
# =============================================================================

# 64卦世爻位置映射表
# key: 64卦标准名
# value: 世爻位置(1~6)
SHIYING_MAP: Dict[str, int] = {
    # ========== 乾宫八卦（金） ==========
    "乾为天": 6,
    "天风姤": 1,
    "天山遁": 2,
    "天地否": 3,
    "风地观": 4,
    "山地剥": 5,
    "火地晋": 4,   # 游魂
    "火天大有": 3,  # 归魂

    # ========== 兑宫八卦（金） ==========
    "兑为泽": 6,
    "泽水困": 1,
    "泽地萃": 2,
    "泽山咸": 3,
    "水山蹇": 4,
    "地山谦": 5,
    "雷山小过": 4,
    "雷泽归妹": 3,

    # ========== 离宫八卦（火） ==========
    "离为火": 6,
    "火山旅": 1,
    "火风鼎": 2,
    "火水未济": 3,
    "山水蒙": 4,
    "风水涣": 5,
    "天水讼": 4,
    "天火同人": 3,

    # ========== 震宫八卦（木） ==========
    "震为雷": 6,
    "雷地豫": 1,
    "雷水解": 2,
    "雷风恒": 3,
    "地风升": 4,
    "水风井": 5,
    "泽风大过": 4,
    "泽雷随": 3,

    # ========== 巽宫八卦（木） ==========
    "巽为风": 6,
    "风天小畜": 1,
    "风火家人": 2,
    "风雷益": 3,
    "天雷无妄": 4,
    "火雷噬嗑": 5,
    "山雷颐": 4,
    "山风蛊": 3,

    # ========== 坎宫八卦（水） ==========
    "坎为水": 6,
    "水泽节": 1,
    "水雷屯": 2,
    "水火既济": 3,
    "泽火革": 4,
    "雷火丰": 5,
    "地火明夷": 4,
    "地水师": 3,

    # ========== 艮宫八卦（土） ==========
    "艮为山": 6,
    "山火贲": 1,
    "山天大畜": 2,
    "山泽损": 3,
    "火泽睽": 4,
    "天泽履": 5,
    "风泽中孚": 4,
    "风山渐": 3,

    # ========== 坤宫八卦（土） ==========
    "坤为地": 6,
    "地雷复": 1,
    "地泽临": 2,
    "地天泰": 3,
    "雷天大壮": 4,
    "泽天夬": 5,
    "水天需": 4,
    "水地比": 3,
}

# 爻位名称（从初爻到上爻）
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

# 八宫名称
GONG_NAMES = ["乾宫", "兑宫", "离宫", "震宫", "巽宫", "坎宫", "艮宫", "坤宫"]

# 八宫卦序（用于反向查询）
GONG_GUA_MAP = {
    "乾宫": ["乾为天", "天风姤", "天山遁", "天地否", "风地观", "山地剥", "火地晋", "火天大有"],
    "兑宫": ["兑为泽", "泽水困", "泽地萃", "泽山咸", "水山蹇", "地山谦", "雷山小过", "雷泽归妹"],
    "离宫": ["离为火", "火山旅", "火风鼎", "火水未济", "山水蒙", "风水涣", "天水讼", "天火同人"],
    "震宫": ["震为雷", "雷地豫", "雷水解", "雷风恒", "地风升", "水风井", "泽风大过", "泽雷随"],
    "巽宫": ["巽为风", "风天小畜", "风火家人", "风雷益", "天雷无妄", "火雷噬嗑", "山雷颐", "山风蛊"],
    "坎宫": ["坎为水", "水泽节", "水雷屯", "水火既济", "泽火革", "雷火丰", "地火明夷", "地水师"],
    "艮宫": ["艮为山", "山火贲", "山天大畜", "山泽损", "火泽睽", "天泽履", "风泽中孚", "风山渐"],
    "坤宫": ["坤为地", "地雷复", "地泽临", "地天泰", "雷天大壮", "泽天夬", "水天需", "水地比"],
}


# =============================================================================
# 核心函数
# =============================================================================

def normalize_gua_name(gua_name: str) -> str:
    """
    规范化卦名
    
    处理以下情况：
    - 去除所有空格（包括全角和半角）
    - 去除首尾空白字符
    
    Args:
        gua_name: 原始卦名
    
    Returns:
        str: 规范化后的卦名
    
    Examples:
        >>> normalize_gua_name("  乾为天  ")
        '乾为天'
        >>> normalize_gua_name("乾　为天")  # 全角空格
        '乾为天'
        >>> normalize_gua_name("乾 为 天")  # 多个空格
        '乾为天'
    """
    if not gua_name:
        return ""
    
    # 替换全角空格为半角空格
    gua_name = gua_name.replace("　", " ")
    # 去除所有空格
    gua_name = gua_name.replace(" ", "")
    # 去除首尾空白字符
    gua_name = gua_name.strip()
    
    return gua_name


def validate_gua_name(gua_name: str) -> bool:
    """
    验证卦名是否有效
    
    Args:
        gua_name: 卦名
    
    Returns:
        bool: 卦名是否在64卦映射表中
    
    Examples:
        >>> validate_gua_name("乾为天")
        True
        >>> validate_gua_name("不存在的卦")
        False
    """
    normalized = normalize_gua_name(gua_name)
    return normalized in SHIYING_MAP


def calculate_ying(shi: int) -> int:
    """
    根据世爻位置计算应爻位置
    
    计算公式：应爻位置 = 世爻位置 + 3
    若结果 > 6，则循环对应（减 6）
    
    Args:
        shi: 世爻位置（1-6）
    
    Returns:
        int: 应爻位置（1-6）
    
    Raises:
        ValueError: 世爻位置不在1-6范围内
    
    Examples:
        >>> calculate_ying(1)
        4
        >>> calculate_ying(6)
        3
        >>> calculate_ying(3)
        6
    """
    if not 1 <= shi <= 6:
        raise ValueError(f"世爻位置必须在1-6之间，当前值: {shi}")
    
    ying = shi + 3
    if ying > 6:
        ying -= 6
    return ying


def get_yao_name(position: int) -> str:
    """
    根据位置获取爻位名称
    
    Args:
        position: 爻位（1-6）
    
    Returns:
        str: 爻位名称（初爻、二爻、三爻、四爻、五爻、上爻）
    
    Raises:
        ValueError: 位置不在1-6范围内
    
    Examples:
        >>> get_yao_name(1)
        '初爻'
        >>> get_yao_name(6)
        '上爻'
    """
    if not 1 <= position <= 6:
        raise ValueError(f"爻位必须在1-6之间，当前值: {position}")
    return YAO_NAMES[position - 1]


def get_gong_name(gua_name: str) -> str:
    """
    根据卦名获取所属宫位
    
    Args:
        gua_name: 卦名
    
    Returns:
        str: 宫位名称（如"乾宫"、"坤宫"等）
    
    Raises:
        ValueError: 卦名无效时抛出异常
    
    Examples:
        >>> get_gong_name("乾为天")
        '乾宫'
        >>> get_gong_name("坤为地")
        '坤宫'
    """
    normalized = normalize_gua_name(gua_name)
    
    if not validate_gua_name(normalized):
        raise ValueError(f"无效的卦名: {gua_name}")
    
    for gong, gua_list in GONG_GUA_MAP.items():
        if normalized in gua_list:
            return gong
    
    # 理论上不会执行到这里，因为前面已经验证过
    raise ValueError(f"无法找到卦名所属宫位: {gua_name}")


def get_shi_ying(gua_name: str) -> dict:
    """
    根据64卦卦名获取世应位置
    
    这是模块的主函数，根据卦名返回世爻和应爻的位置。
    
    Args:
        gua_name: 标准卦名，如 "乾为天"、"风天小畜"
    
    Returns:
        dict: {"shi": 世位(1-6), "ying": 应位(1-6)}
    
    Raises:
        ValueError: 卦名无效时抛出异常
    
    Examples:
        >>> get_shi_ying("乾为天")
        {'shi': 6, 'ying': 3}
        >>> get_shi_ying("天风姤")
        {'shi': 1, 'ying': 4}
        >>> get_shi_ying("风天小畜")
        {'shi': 1, 'ying': 4}
        >>> get_shi_ying("火天大有")
        {'shi': 3, 'ying': 6}
    """
    # 规范化卦名
    normalized = normalize_gua_name(gua_name)
    
    # 验证卦名
    if not validate_gua_name(normalized):
        valid_guas = list(SHIYING_MAP.keys())
        raise ValueError(
            f"无效的卦名: '{gua_name}'。\n"
            f"请使用标准的64卦卦名，如: {', '.join(valid_guas[:5])}..."
        )
    
    # 查表获取世爻位置
    shi = SHIYING_MAP[normalized]
    
    # 计算应爻位置
    ying = calculate_ying(shi)
    
    return {"shi": shi, "ying": ying}


def get_all_gua_names() -> list:
    """
    获取所有64卦卦名列表
    
    Returns:
        list: 64卦卦名列表
    
    Examples:
        >>> names = get_all_gua_names()
        >>> len(names)
        64
        >>> "乾为天" in names
        True
    """
    return list(SHIYING_MAP.keys())


def get_gua_info(gua_name: str) -> dict:
    """
    获取卦象的完整信息（包含宫位、世应等）
    
    Args:
        gua_name: 卦名
    
    Returns:
        dict: {
            "gua_name": "卦名",
            "gong": "宫位",
            "shi": 世位,
            "ying": 应位,
            "shi_name": "世爻名称",
            "ying_name": "应爻名称"
        }
    
    Raises:
        ValueError: 卦名无效时抛出异常
    
    Examples:
        >>> info = get_gua_info("乾为天")
        >>> info['gong']
        '乾宫'
        >>> info['shi']
        6
    """
    normalized = normalize_gua_name(gua_name)
    
    if not validate_gua_name(normalized):
        raise ValueError(f"无效的卦名: {gua_name}")
    
    shi_ying = get_shi_ying(normalized)
    gong = get_gong_name(normalized)
    
    return {
        "gua_name": normalized,
        "gong": gong,
        "shi": shi_ying["shi"],
        "ying": shi_ying["ying"],
        "shi_name": get_yao_name(shi_ying["shi"]),
        "ying_name": get_yao_name(shi_ying["ying"]),
    }