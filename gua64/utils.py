# -*- coding: utf-8 -*-
"""
64卦工具函数模块

提供格式化输出和辅助功能。
"""

from typing import Dict, List, Optional


def format_gua_result(result: Dict, show_detail: bool = True) -> str:
    """
    格式化卦象结果为可读字符串
    
    Args:
        result: calculate_gua() 返回的结果字典
        show_detail: 是否显示详细信息
    
    Returns:
        str: 格式化后的字符串
    """
    lines = []
    
    # 基本信息
    lines.append(f"本卦: {result['ben_gua']['name']}")
    
    # 变卦信息
    if result['bian_gua']:
        lines.append(f"变卦: {result['bian_gua']['name']}")
        if show_detail:
            lines.append(f"变化: {result['bian_gua']['change_detail']}")
    else:
        lines.append("变卦: 无")
    
    # 六爻信息
    lines.append(f"六爻: {result['yao_list']}")
    
    # 动爻信息
    if result['moving_yao']:
        if isinstance(result['moving_yao'], list):
            moving_str = "、".join([f"第{p}爻" for p in result['moving_yao']])
        else:
            moving_str = f"第{result['moving_yao']}爻"
        lines.append(f"动爻: {moving_str}")
    
    return "\n".join(lines)


def format_gua_table(result: Dict) -> str:
    """
    格式化卦象结果为表格形式
    
    Args:
        result: calculate_gua() 返回的结果字典
    
    Returns:
        str: 表格形式的字符串
    """
    lines = []
    lines.append("=" * 50)
    lines.append("              卦象信息")
    lines.append("=" * 50)
    
    # 本卦
    ben = result['ben_gua']
    lines.append(f"【本卦】{ben['name']}")
    lines.append(f"  上卦: {ben['upper_gua']} ({ben['upper_nature']})")
    lines.append(f"  下卦: {ben['lower_gua']} ({ben['lower_nature']})")
    lines.append(f"  卦名: {ben['gua64_name']}")
    
    # 变卦
    if result['bian_gua']:
        bian = result['bian_gua']
        lines.append("-" * 50)
        lines.append(f"【变卦】{bian['name']}")
        lines.append(f"  上卦: {bian['upper_gua']} ({bian['upper_nature']})")
        lines.append(f"  下卦: {bian['lower_gua']} ({bian['lower_nature']})")
        lines.append(f"  卦名: {bian['gua64_name']}")
        lines.append(f"  变化: {bian['change_detail']}")
    
    lines.append("=" * 50)
    
    # 六爻
    lines.append(f"六爻: {result['yao_list']}")
    if result['moving_yao']:
        if isinstance(result['moving_yao'], list):
            moving_str = "、".join([str(p) for p in result['moving_yao']])
        else:
            moving_str = str(result['moving_yao'])
        lines.append(f"动爻: 第{moving_str}爻")
    
    return "\n".join(lines)


def format_yao_visual(yao_list: List[int], moving_yao: Optional[List[int]] = None) -> str:
    """
    格式化六爻为可视化图形
    
    阳爻: ━━━━━
    阴爻: ━━ ━━
    动爻标记: ○ (阳变阴) 或 × (阴变阳)
    
    Args:
        yao_list: 六爻数组
        moving_yao: 动爻位置列表
    
    Returns:
        str: 可视化图形
    """
    if moving_yao is None:
        moving_yao = []
    elif isinstance(moving_yao, int):
        moving_yao = [moving_yao]
    
    lines = []
    yao_names = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
    
    # 从上到下显示（上爻在上，初爻在下）
    for i in range(5, -1, -1):
        yao = yao_list[i]
        yao_name = yao_names[5 - i]
        pos = i + 1  # 爻位（1-6）
        
        # 爻的图形
        if yao == 1:  # 阳爻
            symbol = "━━━━━"
        else:  # 阴爻
            symbol = "━ ━━"
        
        # 动爻标记
        if pos in moving_yao:
            mark = "○" if yao == 1 else "×"
        else:
            mark = " "
        
        lines.append(f"{yao_name}: {symbol} {mark}")
    
    return "\n".join(lines)


def get_gua_symbol(upper_gua: str, lower_gua: str) -> str:
    """
    获取卦象符号（Unicode）
    
    Args:
        upper_gua: 上卦名
        lower_gua: 下卦名
    
    Returns:
        str: 卦象符号
    """
    # 八卦Unicode符号
    trigram_symbols = {
        "乾": "☰",
        "兑": "☱",
        "离": "☲",
        "震": "☳",
        "巽": "☴",
        "坎": "☵",
        "艮": "☶",
        "坤": "☷",
    }
    
    upper_symbol = trigram_symbols.get(upper_gua, "?")
    lower_symbol = trigram_symbols.get(lower_gua, "?")
    
    return f"{upper_symbol}\n{lower_symbol}"


def format_full_output(result: Dict) -> str:
    """
    格式化完整输出（包含图形和详细信息）
    
    Args:
        result: calculate_gua() 返回的结果字典
    
    Returns:
        str: 完整格式化的字符串
    """
    lines = []
    
    # 标题
    lines.append("=" * 60)
    lines.append("                 卦象排盘")
    lines.append("=" * 60)
    
    # 本卦图形
    lines.append("\n【本卦】")
    lines.append(format_yao_visual(
        result['yao_list'], 
        result['moving_yao']
    ))
    lines.append(f"\n卦名: {result['ben_gua']['name']}")
    
    # 变卦图形
    if result['bian_gua']:
        lines.append("\n" + "-" * 60)
        lines.append("\n【变卦】")
        lines.append(format_yao_visual(
            result['bian_gua']['new_yao_list']
        ))
        lines.append(f"\n卦名: {result['bian_gua']['name']}")
        lines.append(f"变化: {result['bian_gua']['change_detail']}")
    
    lines.append("\n" + "=" * 60)
    
    return "\n".join(lines)


# =============================================================================
# 测试代码
# =============================================================================

if __name__ == "__main__":
    from core import calculate_gua
    
    print("=" * 60)
    print("格式化输出测试")
    print("=" * 60)
    
    # 测试用例
    result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
    
    print("\n【简单格式】")
    print(format_gua_result(result))
    
    print("\n【表格格式】")
    print(format_gua_table(result))
    
    print("\n【完整输出】")
    print(format_full_output(result))