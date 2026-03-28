# -*- coding: utf-8 -*-
"""
硬币起卦模块

六爻金钱卦规则（以少为尊）：
- 3个阳面（正面）= 老阳（阳爻动）→ 爻值=1（阳），is_moving=True
- 2个阳面（正面）= 少阴（阴爻静）→ 爻值=2（阴），is_moving=False
  （2正1反，反为少，故阴）
- 1个阳面（正面）= 少阳（阳爻静）→ 爻值=1（阳），is_moving=False
  （1正2反，正为少，故阳）
- 0个阳面（正面）= 老阴（阴爻动）→ 爻值=2（阴），is_moving=True
"""

import random
from gua64 import calculate_gua


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
            'coin_details': 每次抛硬币的详细信息,
            'gua_info': 卦象信息
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
    # 动爻位置不需要转换，因为位置定义是固定的（1=初爻，6=上爻）
    # calculate_gua 内部使用 index = pos - 1 访问数组，所以动爻位置直接传入
    gua_info = calculate_gua(yao_list_reversed, moving_yao_list)
    
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