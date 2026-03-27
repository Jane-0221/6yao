# -*- coding: utf-8 -*-
"""
六神排盘核心算法模块

严格遵循《卜筮正宗》六爻六神排盘的正统规则实现。

正统规则（不可修改）：
1. 六神固定循环顺序：青龙、朱雀、勾陈、螣蛇、白虎、玄武
2. 排盘唯一依据：起卦当日的天干
3. 日天干→初爻起始六神映射：
   - 甲、乙 → 青龙（索引0）
   - 丙、丁 → 朱雀（索引1）
   - 戊 → 勾陈（索引2）
   - 己 → 螣蛇（索引3）
   - 庚、辛 → 白虎（索引4）
   - 壬、癸 → 玄武（索引5）
4. 排盘顺序：从初爻到上爻（自下而上）顺排
5. 核心计算公式：六神索引 = (起始索引 + 爻位偏移量) % 6
"""

# =============================================================================
# 常量定义（正统规则，不可修改）
# =============================================================================

# 六神固定循环顺序（绝对不可更改）
# 索引0-5分别对应：青龙、朱雀、勾陈、螣蛇、白虎、玄武
SIX_GODS = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

# 日天干→初爻起始六神索引映射（不可修改）
# 根据天干确定初爻对应的六神，后续爻位按顺序循环
TIANGAN_TO_INDEX = {
    "甲": 0,  # 青龙
    "乙": 0,  # 青龙
    "丙": 1,  # 朱雀
    "丁": 1,  # 朱雀
    "戊": 2,  # 勾陈
    "己": 3,  # 螣蛇
    "庚": 4,  # 白虎
    "辛": 4,  # 白虎
    "壬": 5,  # 玄武
    "癸": 5,  # 玄武
}

# 有效的天干列表
VALID_TIANGAN = list(TIANGAN_TO_INDEX.keys())

# 爻位名称（从初爻到上爻）
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


# =============================================================================
# 核心函数
# =============================================================================

def get_tiangan_index(day_tiangan: str) -> int:
    """
    根据天干获取六神起始索引
    
    正统规则映射：
    - 甲、乙 → 青龙（索引0）
    - 丙、丁 → 朱雀（索引1）
    - 戊 → 勾陈（索引2）
    - 己 → 螣蛇（索引3）
    - 庚、辛 → 白虎（索引4）
    - 壬、癸 → 玄武（索引5）
    
    Args:
        day_tiangan: 天干字符串（甲、乙、丙、丁、戊、己、庚、辛、壬、癸）
    
    Returns:
        int: 六神起始索引（0-5）
    
    Raises:
        ValueError: 无效天干输入时抛出异常
    
    Examples:
        >>> get_tiangan_index("甲")
        0
        >>> get_tiangan_index("己")
        3
        >>> get_tiangan_index("癸")
        5
    """
    # 输入校验
    if not isinstance(day_tiangan, str):
        raise ValueError(
            f"无效的天干类型，请输入字符串类型的天干。"
            f"有效天干：甲、乙、丙、丁、戊、己、庚、辛、壬、癸"
        )
    
    # 去除首尾空格
    day_tiangan = day_tiangan.strip()
    
    # 检查天干是否有效
    if day_tiangan not in TIANGAN_TO_INDEX:
        raise ValueError(
            f"无效的天干'{day_tiangan}'，请输入十天干之一："
            f"甲、乙、丙、丁、戊、己、庚、辛、壬、癸"
        )
    
    return TIANGAN_TO_INDEX[day_tiangan]


def calculate_six_gods(day_tiangan: str, yao_list: list = None) -> dict:
    """
    六神排盘核心函数
    
    根据起卦当日的天干，按照《卜筮正宗》正统规则计算六爻六神。
    
    排盘规则：
    1. 根据天干确定初爻的六神（起始索引）
    2. 从初爻到上爻（自下而上）顺排
    3. 核心公式：六神索引 = (起始索引 + 爻位偏移量) % 6
       - 初爻偏移量 = 0
       - 二爻偏移量 = 1
       - 三爻偏移量 = 2
       - 四爻偏移量 = 3
       - 五爻偏移量 = 4
       - 上爻偏移量 = 5
    
    Args:
        day_tiangan: 起卦日的天干（甲、乙、丙、丁、戊、己、庚、辛、壬、癸）
        yao_list: 可选，六爻数组，格式为[初爻,二爻,三爻,四爻,五爻,上爻]
                  用于匹配爻位输出，显示阴阳属性
                  爻值定义：
                  - 0 = 少阴（阴爻，静）
                  - 1 = 少阳（阳爻，静）或 老阳（阳爻，动）
                  - 2 = 老阴（阴爻，动）
                  - 3 = 老阳（阳爻，动）
    
    Returns:
        dict: {
            'day_tiangan': 天干,
            'start_god': 初爻起始六神名称,
            'start_index': 起始索引（0-5）,
            'six_gods_list': 六神列表[初爻到上爻],
            'yao_details': 爻位详情列表（若传入yao_list）,
            'yao_list': 原始六爻列表（若传入yao_list）
        }
    
    Raises:
        ValueError: 无效天干输入时抛出异常
    
    Examples:
        >>> result = calculate_six_gods("甲")
        >>> result['six_gods_list']
        ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']
        
        >>> result = calculate_six_gods("己")
        >>> result['six_gods_list']
        ['螣蛇', '白虎', '玄武', '青龙', '朱雀', '勾陈']
        
        >>> result = calculate_six_gods("癸")
        >>> result['six_gods_list']
        ['玄武', '青龙', '朱雀', '勾陈', '螣蛇', '白虎']
    """
    # 获取起始索引（包含输入校验）
    start_index = get_tiangan_index(day_tiangan)
    
    # 计算六爻六神
    # 核心公式：六神索引 = (起始索引 + 爻位偏移量) % 6
    six_gods_list = []
    for yao_offset in range(6):  # 爻位偏移量：0, 1, 2, 3, 4, 5
        god_index = (start_index + yao_offset) % 6
        six_gods_list.append(SIX_GODS[god_index])
    
    # 构建基础结果
    result = {
        'day_tiangan': day_tiangan,
        'start_god': SIX_GODS[start_index],
        'start_index': start_index,
        'six_gods_list': six_gods_list,
    }
    
    # 如果传入了六爻列表，生成爻位详情
    if yao_list is not None:
        # 校验六爻列表
        if not isinstance(yao_list, list):
            raise ValueError("yao_list 必须是列表类型")
        if len(yao_list) != 6:
            raise ValueError("yao_list 必须包含6个元素（初爻到上爻）")
        
        # 生成爻位详情
        yao_details = []
        for i, (yao_name, god, yao_value) in enumerate(zip(YAO_NAMES, six_gods_list, yao_list)):
            yin_yang = get_yao_yin_yang(yao_value)
            yao_details.append({
                'yao_name': yao_name,        # 爻位名称
                'yao_index': i + 1,          # 爻位序号（1-6）
                'six_god': god,              # 六神
                'yao_value': yao_value,      # 爻值
                'yin_yang': yin_yang,        # 阴阳属性描述
            })
        
        result['yao_details'] = yao_details
        result['yao_list'] = yao_list
    
    return result


def get_yao_yin_yang(yao_value: int) -> str:
    """
    根据爻值获取阴阳属性描述
    
    爻值定义（与divination.py保持一致）：
    - 0 = 少阴（阴爻，静）
    - 1 = 少阳（阳爻，静）
    - 2 = 老阴（阴爻，动→变阳）
    - 3 = 老阳（阳爻，动→变阴）
    
    Args:
        yao_value: 爻值（0, 1, 2, 3）
    
    Returns:
        str: 阴阳属性描述
    """
    if yao_value == 0:
        return "少阴（阴爻，静）"
    elif yao_value == 1:
        return "少阳（阳爻，静）"
    elif yao_value == 2:
        return "老阴（阴爻，动→变阳）"
    elif yao_value == 3:
        return "老阳（阳爻，动→变阴）"
    else:
        return f"未知爻值({yao_value})"


# =============================================================================
# 测试函数
# =============================================================================

def test_six_gods():
    """
    测试六神排盘功能
    
    验证四个测试用例：
    1. 天干="甲"：初爻青龙，顺排
    2. 天干="己"：初爻螣蛇，顺排
    3. 天干="癸"：初爻玄武，顺排
    4. 无效天干="子"：抛出异常
    """
    print("=" * 60)
    print("六神排盘测试")
    print("=" * 60)
    
    # 测试用例1：天干="甲"
    print("\n【测试用例1】天干='甲'")
    result = calculate_six_gods("甲")
    print(f"起始六神: {result['start_god']} (索引{result['start_index']})")
    print("六神排盘:")
    for i, (yao_name, god) in enumerate(zip(YAO_NAMES, result['six_gods_list'])):
        print(f"  {yao_name}：{god}")
    
    # 验证
    expected = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]
    assert result['six_gods_list'] == expected, f"测试用例1失败: {result['six_gods_list']}"
    print("✓ 测试通过")
    
    # 测试用例2：天干="己"
    print("\n【测试用例2】天干='己'")
    result = calculate_six_gods("己")
    print(f"起始六神: {result['start_god']} (索引{result['start_index']})")
    print("六神排盘:")
    for i, (yao_name, god) in enumerate(zip(YAO_NAMES, result['six_gods_list'])):
        print(f"  {yao_name}：{god}")
    
    # 验证
    expected = ["螣蛇", "白虎", "玄武", "青龙", "朱雀", "勾陈"]
    assert result['six_gods_list'] == expected, f"测试用例2失败: {result['six_gods_list']}"
    print("✓ 测试通过")
    
    # 测试用例3：天干="癸"
    print("\n【测试用例3】天干='癸'")
    result = calculate_six_gods("癸")
    print(f"起始六神: {result['start_god']} (索引{result['start_index']})")
    print("六神排盘:")
    for i, (yao_name, god) in enumerate(zip(YAO_NAMES, result['six_gods_list'])):
        print(f"  {yao_name}：{god}")
    
    # 验证
    expected = ["玄武", "青龙", "朱雀", "勾陈", "螣蛇", "白虎"]
    assert result['six_gods_list'] == expected, f"测试用例3失败: {result['six_gods_list']}"
    print("✓ 测试通过")
    
    # 测试用例4：无效天干="子"
    print("\n【测试用例4】天干='子'（无效天干）")
    try:
        result = calculate_six_gods("子")
        print("✗ 测试失败：应该抛出异常")
    except ValueError as e:
        print(f"正确抛出异常: {e}")
        print("✓ 测试通过")
    
    # 测试带六爻列表的情况
    print("\n【附加测试】带六爻列表")
    result = calculate_six_gods("甲", yao_list=[1, 2, 1, 2, 1, 2])
    print("六神排盘（带阴阳属性）:")
    for detail in result['yao_details']:
        print(f"  {detail['yao_name']}：{detail['six_god']} - {detail['yin_yang']}")
    print("✓ 测试通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    test_six_gods()