# -*- coding: utf-8 -*-
"""
起卦方式公共辅助函数模块

包含：
- 八卦对应表（常量）
- 八卦二进制表示（常量）
- 卦象转换函数
"""

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