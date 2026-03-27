# -*- coding: utf-8 -*-
"""
六亲核心算法模块

根据本宫五行和爻地支五行计算六亲。

核心规则：
1. 生我者为父母
2. 我生者为子孙
3. 克我者为官鬼
4. 我克者为妻财
5. 同我者为兄弟
"""

from typing import Dict, List


# =============================================================================
# 常量定义
# =============================================================================

# 五行列表
WUXING_LIST = ["金", "木", "水", "火", "土"]

# 六亲列表
LIU_QIN_LIST = ["父母", "兄弟", "子孙", "妻财", "官鬼"]

# 五行生克关系表
# sheng: 我生者, ke: 我克者, bei_sheng: 生我者, bei_ke: 克我者
SHENG_KE = {
    "木": {"sheng": "火", "ke": "土", "bei_sheng": "水", "bei_ke": "金"},
    "火": {"sheng": "土", "ke": "金", "bei_sheng": "木", "bei_ke": "水"},
    "土": {"sheng": "金", "ke": "水", "bei_sheng": "火", "bei_ke": "木"},
    "金": {"sheng": "水", "ke": "木", "bei_sheng": "土", "bei_ke": "火"},
    "水": {"sheng": "木", "ke": "火", "bei_sheng": "金", "bei_ke": "土"},
}

# 地支五行表
DI_ZHI_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 八宫五行表
GONG_ELEMENT = {
    "乾宫": "金",
    "兑宫": "金",
    "离宫": "火",
    "震宫": "木",
    "巽宫": "木",
    "坎宫": "水",
    "艮宫": "土",
    "坤宫": "土",
}

# 爻位名称
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


# =============================================================================
# 核心函数
# =============================================================================

def validate_wuxing(element: str) -> None:
    """
    校验五行是否有效
    
    Args:
        element: 五行（金/木/水/火/土）
    
    Raises:
        ValueError: 无效五行时抛出异常
    """
    if element not in WUXING_LIST:
        raise ValueError(
            f"无效的五行'{element}'，请输入五行之一：金、木、水、火、土"
        )


def validate_di_zhi(di_zhi: str) -> None:
    """
    校验地支是否有效
    
    Args:
        di_zhi: 地支
    
    Raises:
        ValueError: 无效地支时抛出异常
    """
    if di_zhi not in DI_ZHI_ELEMENT:
        raise ValueError(
            f"无效的地支'{di_zhi}'，请输入十二地支之一："
            f"子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥"
        )


def validate_gong(gong: str) -> None:
    """
    校验宫位是否有效
    
    Args:
        gong: 宫位名
    
    Raises:
        ValueError: 无效宫位时抛出异常
    """
    if gong not in GONG_ELEMENT:
        raise ValueError(
            f"无效的宫位'{gong}'，请输入八宫之一："
            f"乾宫、兑宫、离宫、震宫、巽宫、坎宫、艮宫、坤宫"
        )


def get_element_by_di_zhi(di_zhi: str) -> str:
    """
    根据地支获取五行
    
    Args:
        di_zhi: 地支（子/丑/寅/卯/辰/巳/午/未/申/酉/戌/亥）
    
    Returns:
        str: 五行（金/木/水/火/土）
    
    Raises:
        ValueError: 无效地支时抛出异常
    
    Examples:
        >>> get_element_by_di_zhi("子")
        '水'
        >>> get_element_by_di_zhi("寅")
        '木'
        >>> get_element_by_di_zhi("午")
        '火'
    """
    validate_di_zhi(di_zhi)
    return DI_ZHI_ELEMENT[di_zhi]


def get_element_by_gong(gong: str) -> str:
    """
    根据宫位获取五行
    
    Args:
        gong: 宫位名（乾宫/兑宫/离宫/震宫/巽宫/坎宫/艮宫/坤宫）
    
    Returns:
        str: 五行（金/木/水/火/土）
    
    Raises:
        ValueError: 无效宫位时抛出异常
    
    Examples:
        >>> get_element_by_gong("乾宫")
        '金'
        >>> get_element_by_gong("离宫")
        '火'
        >>> get_element_by_gong("震宫")
        '木'
    """
    validate_gong(gong)
    return GONG_ELEMENT[gong]


def get_liu_qin_by_element(self_element: str, yao_element: str) -> str:
    """
    根据本宫五行和爻五行计算六亲
    
    六亲规则：
    - 同我者 → 兄弟
    - 我生者 → 子孙
    - 我克者 → 妻财
    - 生我者 → 父母
    - 克我者 → 官鬼
    
    Args:
        self_element: 本宫五行
        yao_element: 爻五行
    
    Returns:
        str: 六亲（父母/兄弟/子孙/妻财/官鬼）
    
    Raises:
        ValueError: 无效五行时抛出异常
    
    Examples:
        >>> get_liu_qin_by_element("金", "金")  # 同我者
        '兄弟'
        >>> get_liu_qin_by_element("金", "水")  # 我生者（金生水）
        '子孙'
        >>> get_liu_qin_by_element("金", "木")  # 我克者（金克木）
        '妻财'
        >>> get_liu_qin_by_element("金", "土")  # 生我者（土生金）
        '父母'
        >>> get_liu_qin_by_element("金", "火")  # 克我者（火克金）
        '官鬼'
    """
    validate_wuxing(self_element)
    validate_wuxing(yao_element)
    
    relation = SHENG_KE[self_element]
    
    if yao_element == self_element:
        # 同我者 → 兄弟
        return "兄弟"
    elif yao_element == relation["sheng"]:
        # 我生者 → 子孙
        return "子孙"
    elif yao_element == relation["ke"]:
        # 我克者 → 妻财
        return "妻财"
    elif yao_element == relation["bei_sheng"]:
        # 生我者 → 父母
        return "父母"
    elif yao_element == relation["bei_ke"]:
        # 克我者 → 官鬼
        return "官鬼"
    else:
        # 理论上不会执行到这里
        raise ValueError(
            f"无法确定六亲关系：本宫五行'{self_element}'，爻五行'{yao_element}'"
        )


def get_six_yao_liu_qin(gong: str, di_zhi_list: List[str]) -> Dict:
    """
    计算六爻六亲
    
    根据宫位五行和六爻地支五行，计算每爻的六亲。
    
    Args:
        gong: 宫位名（如"乾宫"）
        di_zhi_list: 六爻地支列表，从初爻到上爻
    
    Returns:
        dict: {
            "liu_qin": ["兄弟", "父母", "妻财", "官鬼", "父母", "子孙"],
            "gong": "乾宫",
            "gong_element": "金",
            "yao_elements": ["金", "水", "木", "火", "土", "水"],
            "di_zhi": ["子", "寅", "辰", "午", "申", "戌"]
        }
    
    Raises:
        ValueError: 无效参数时抛出异常
    
    Examples:
        >>> result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        >>> result["liu_qin"]
        ['子孙', '妻财', '兄弟', '官鬼', '父母', '兄弟']
        >>> result["gong_element"]
        '金'
        
        >>> result = get_six_yao_liu_qin("离宫", ["卯", "丑", "亥", "酉", "未", "巳"])
        >>> result["liu_qin"]
        ['子孙', '妻财', '官鬼', '兄弟', '父母', '妻财']
    """
    # 校验地支列表长度
    if not isinstance(di_zhi_list, list):
        raise ValueError(
            f"地支列表必须是列表类型，当前类型: {type(di_zhi_list)}"
        )
    
    if len(di_zhi_list) != 6:
        raise ValueError(
            f"地支列表长度必须为6，当前长度: {len(di_zhi_list)}"
        )
    
    # 校验宫位
    validate_gong(gong)
    
    # 获取本宫五行
    gong_element = get_element_by_gong(gong)
    
    # 计算每爻的五行和六亲
    liu_qin_list = []
    yao_elements = []
    
    for i, di_zhi in enumerate(di_zhi_list):
        # 校验地支
        validate_di_zhi(di_zhi)
        
        # 获取地支五行
        yao_element = get_element_by_di_zhi(di_zhi)
        yao_elements.append(yao_element)
        
        # 计算六亲
        liu_qin = get_liu_qin_by_element(gong_element, yao_element)
        liu_qin_list.append(liu_qin)
    
    return {
        "liu_qin": liu_qin_list,
        "gong": gong,
        "gong_element": gong_element,
        "yao_elements": yao_elements,
        "di_zhi": di_zhi_list
    }


def get_yao_liu_qin(gong: str, di_zhi_list: List[str], yao_index: int) -> str:
    """
    获取指定爻位的六亲
    
    Args:
        gong: 宫位名
        di_zhi_list: 六爻地支列表
        yao_index: 爻位索引（0-5，0=初爻，5=上爻）
    
    Returns:
        str: 该爻位的六亲
    
    Raises:
        ValueError: 无效爻位索引时抛出异常
    """
    if not isinstance(yao_index, int) or yao_index < 0 or yao_index > 5:
        raise ValueError(
            f"无效的爻位索引'{yao_index}'，请输入0-5的整数"
        )
    
    result = get_six_yao_liu_qin(gong, di_zhi_list)
    return result["liu_qin"][yao_index]