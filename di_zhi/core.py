# -*- coding: utf-8 -*-
"""
六爻地支核心算法模块

根据上下经卦获取六爻固定地支。

核心规则：
1. 六爻地支终身固定：同一卦的地支永远不变，与动爻、日辰、六神无关
2. 下卦（内卦）决定初爻、二爻、三爻
3. 上卦（外卦）决定四爻、五爻、上爻
"""

from typing import Dict, List


# =============================================================================
# 常量定义
# =============================================================================

# 八卦纳支表（绝对固定，不可修改）
# 格式：经卦名 -> [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
TRIGRAM_NAZHI = {
    "乾": ["子", "寅", "辰", "午", "申", "戌"],
    "震": ["子", "寅", "辰", "午", "申", "戌"],
    "坎": ["寅", "辰", "午", "申", "戌", "子"],
    "艮": ["辰", "午", "申", "戌", "子", "寅"],
    "坤": ["未", "巳", "卯", "丑", "亥", "酉"],
    "巽": ["丑", "亥", "酉", "未", "巳", "卯"],
    "离": ["卯", "丑", "亥", "酉", "未", "巳"],
    "兑": ["巳", "卯", "丑", "亥", "酉", "未"],
}

# 有效的卦名列表
VALID_TRIGRAMS = list(TRIGRAM_NAZHI.keys())

# 爻位名称
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


# =============================================================================
# 核心函数
# =============================================================================

def validate_trigram(trigram: str) -> None:
    """
    校验卦名是否有效
    
    Args:
        trigram: 卦名（乾/兑/离/震/巽/坎/艮/坤）
    
    Raises:
        ValueError: 无效卦名时抛出异常
    
    Examples:
        >>> validate_trigram("乾")  # 不抛出异常
        >>> validate_trigram("无效")  # 抛出 ValueError
    """
    if not isinstance(trigram, str):
        raise ValueError(
            f"无效的卦名类型，请输入字符串类型的卦名。"
            f"有效卦名：乾、兑、离、震、巽、坎、艮、坤"
        )
    
    trigram = trigram.strip()
    
    if trigram not in VALID_TRIGRAMS:
        raise ValueError(
            f"无效的卦名'{trigram}'，请输入八卦之一："
            f"乾、兑、离、震、巽、坎、艮、坤"
        )


def get_six_yao_di_zhi(upper_gua: str, lower_gua: str) -> Dict:
    """
    根据上下经卦获取六爻固定地支
    
    算法逻辑：
    1. 取下卦纳支数组的前3位 -> 初、二、三爻
    2. 取上卦纳支数组的后3位 -> 四、五、上爻
    3. 拼接为完整六爻地支
    
    Args:
        upper_gua: 上卦名（乾/兑/离/震/巽/坎/艮/坤）
        lower_gua: 下卦名（乾/兑/离/震/巽/坎/艮/坤）
    
    Returns:
        dict: {
            "di_zhi": ["子", "寅", "辰", "午", "申", "戌"],
            "upper_gua": upper_gua,
            "lower_gua": lower_gua
        }
    
    Raises:
        ValueError: 无效卦名时抛出异常
    
    Examples:
        >>> get_six_yao_di_zhi("乾", "乾")
        {'di_zhi': ['子', '寅', '辰', '午', '申', '戌'], 'upper_gua': '乾', 'lower_gua': '乾'}
        
        >>> get_six_yao_di_zhi("巽", "乾")
        {'di_zhi': ['子', '寅', '辰', '未', '巳', '卯'], 'upper_gua': '巽', 'lower_gua': '乾'}
        
        >>> get_six_yao_di_zhi("坤", "坤")
        {'di_zhi': ['未', '巳', '卯', '丑', '亥', '酉'], 'upper_gua': '坤', 'lower_gua': '坤'}
    """
    # 校验输入
    validate_trigram(upper_gua)
    validate_trigram(lower_gua)
    
    # 去除首尾空格
    upper_gua = upper_gua.strip()
    lower_gua = lower_gua.strip()
    
    # 获取上下卦的纳支数组
    upper_nazhi = TRIGRAM_NAZHI[upper_gua]
    lower_nazhi = TRIGRAM_NAZHI[lower_gua]
    
    # 拼接六爻地支
    # 下卦前3位 -> 初、二、三爻
    # 上卦后3位 -> 四、五、上爻
    di_zhi = lower_nazhi[:3] + upper_nazhi[3:]
    
    return {
        "di_zhi": di_zhi,
        "upper_gua": upper_gua,
        "lower_gua": lower_gua
    }


def get_yao_di_zhi(upper_gua: str, lower_gua: str, yao_index: int) -> str:
    """
    获取指定爻位的地支
    
    Args:
        upper_gua: 上卦名
        lower_gua: 下卦名
        yao_index: 爻位索引（0-5，0=初爻，5=上爻）
    
    Returns:
        str: 该爻位的地支
    
    Raises:
        ValueError: 无效爻位索引时抛出异常
    
    Examples:
        >>> get_yao_di_zhi("乾", "乾", 0)
        '子'
        >>> get_yao_di_zhi("乾", "乾", 5)
        '戌'
    """
    if not isinstance(yao_index, int) or yao_index < 0 or yao_index > 5:
        raise ValueError(
            f"无效的爻位索引'{yao_index}'，请输入0-5的整数"
        )
    
    result = get_six_yao_di_zhi(upper_gua, lower_gua)
    return result["di_zhi"][yao_index]