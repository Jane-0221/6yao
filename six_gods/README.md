# 六神排盘模块

根据《卜筮正宗》六爻六神排盘的正统规则实现的六神自动排盘功能。

## 一、正统规则

### 1.1 六神固定循环顺序（永远不变）

**重要概念**：六神的固定循环顺序永远是：
```
青龙 → 朱雀 → 勾陈 → 螣蛇 → 白虎 → 玄武 →（周而复始，回到青龙）
```

这个顺序是**绝对固定的**，不会因为日期而改变。不同的日天干只是从这个固定循环的**不同位置开始**截取。

### 1.2 日天干→初爻起始六神映射

| 天干 | 起始六神 | 索引 | 说明 |
|------|----------|------|------|
| 甲、乙 | 青龙 | 0 | 从青龙开始 |
| 丙、丁 | 朱雀 | 1 | 从朱雀开始 |
| 戊 | 勾陈 | 2 | 从勾陈开始 |
| 己 | 螣蛇 | 3 | 从螣蛇开始 |
| 庚、辛 | 白虎 | 4 | 从白虎开始 |
| 壬、癸 | 玄武 | 5 | 从玄武开始 |

### 1.3 排盘规则

- **排盘顺序**：从初爻到上爻（自下而上）顺排
- **核心公式**：`六神索引 = (起始索引 + 爻位偏移量) % 6`
  - 初爻偏移量 = 0
  - 二爻偏移量 = 1
  - 三爻偏移量 = 2
  - 四爻偏移量 = 3
  - 五爻偏移量 = 4
  - 上爻偏移量 = 5

### 1.4 排盘示例（庚日）

以庚日为例，初爻起白虎：

| 爻位 | 六神 | 计算过程 | 说明 |
|------|------|----------|------|
| 初爻 | 白虎 | (4+0)%6=4 | 起始位置 |
| 二爻 | 玄武 | (4+1)%6=5 | 白虎后一位 |
| 三爻 | 青龙 | (4+2)%6=0 | 玄武后一位，循环回到青龙 |
| 四爻 | 朱雀 | (4+3)%6=1 | 青龙后一位 |
| 五爻 | 勾陈 | (4+4)%6=2 | 朱雀后一位 |
| 上爻 | 螣蛇 | (4+5)%6=3 | 勾陈后一位 |

**注意**：庚日的排盘结果"白虎→玄武→青龙→朱雀→勾陈→螣蛇"只是从白虎开始截取了固定循环的一部分，**并非**六神顺序改变。六神的固定顺序永远是"青龙→朱雀→勾陈→螣蛇→白虎→玄武"。

## 二、模块结构

```
six_gods/
├── __init__.py    # 模块初始化，导出公共接口
├── core.py        # 核心算法实现
├── utils.py       # 辅助函数
└── README.md      # 本文档
```

## 三、使用方法

### 3.1 基本用法

```python
from six_gods import calculate_six_gods, format_six_gods_result

# 计算六神排盘
result = calculate_six_gods("甲")

# 格式化输出
print(format_six_gods_result(result))
```

输出：
```
日天干：甲
初爻起始六神：青龙
────────────────────
初爻：青龙
二爻：朱雀
三爻：勾陈
四爻：螣蛇
五爻：白虎
上爻：玄武
```

### 3.2 带六爻信息

```python
from six_gods import calculate_six_gods, format_six_gods_result

# 传入六爻列表
yao_list = [1, 2, 1, 2, 1, 2]  # 阳阴阳阴阳阴
result = calculate_six_gods("甲", yao_list=yao_list)

# 格式化输出
print(format_six_gods_result(result))
```

输出：
```
日天干：甲
初爻起始六神：青龙
────────────────────
初爻：青龙 - 少阳（阳爻，静）
二爻：朱雀 - 老阴（阴爻，动→变阳）
三爻：勾陈 - 少阳（阳爻，静）
四爻：螣蛇 - 老阴（阴爻，动→变阳）
五爻：白虎 - 少阳（阳爻，静）
上爻：玄武 - 老阴（阴爻，动→变阳）
```

### 3.3 与起卦功能集成

```python
from divination import get_day_tiangan, coin_divination
from six_gods import calculate_six_gods

# 获取当前日期的天干
day_tiangan = get_day_tiangan()

# 硬币起卦
result = coin_divination([...])

# 计算六神排盘（带六爻信息）
six_gods_result = calculate_six_gods(day_tiangan, yao_list=result['yao_list'])
```

## 四、API 参考

### 4.1 核心函数

#### `calculate_six_gods(day_tiangan: str, yao_list: list = None) -> dict`

六神排盘核心函数。

**参数：**
- `day_tiangan` (str): 起卦日的天干（甲、乙、丙、丁、戊、己、庚、辛、壬、癸）
- `yao_list` (list, 可选): 六爻数组，格式为[初爻,二爻,三爻,四爻,五爻,上爻]

**返回：**
```python
{
    'day_tiangan': str,        # 天干
    'start_god': str,          # 初爻起始六神名称
    'start_index': int,        # 起始索引（0-5）
    'six_gods_list': list,     # 六神列表[初爻到上爻]
    'yao_details': list,       # 爻位详情列表（若传入yao_list）
    'yao_list': list           # 原始六爻列表（若传入yao_list）
}
```

**异常：**
- `ValueError`: 无效天干输入时抛出

#### `get_tiangan_index(day_tiangan: str) -> int`

根据天干获取六神起始索引。

**参数：**
- `day_tiangan` (str): 天干字符串

**返回：**
- `int`: 六神起始索引（0-5）

### 4.2 辅助函数

#### `format_six_gods_result(result: dict) -> str`

格式化输出六神排盘结果。

#### `print_six_gods_result(result: dict)`

打印六神排盘结果。

#### `get_six_god_for_yao(day_tiangan: str, yao_position: int) -> str`

获取指定爻位的六神。

**参数：**
- `day_tiangan` (str): 天干
- `yao_position` (int): 爻位（1-6，1=初爻，6=上爻）

**返回：**
- `str`: 六神名称

#### `validate_tiangan(day_tiangan: str) -> bool`

验证天干是否有效。

### 4.3 常量

```python
# 六神列表
SIX_GODS = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

# 天干到索引的映射
TIANGAN_TO_INDEX = {
    "甲": 0, "乙": 0, "丙": 1, "丁": 1, "戊": 2,
    "己": 3, "庚": 4, "辛": 4, "壬": 5, "癸": 5
}

# 爻位名称
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

# 有效的天干列表
VALID_TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
```

## 五、测试用例

运行测试：
```bash
python test_six_gods.py
```

测试覆盖：
1. 天干="甲"：初爻青龙，顺排
2. 天干="己"：初爻螣蛇，顺排
3. 天干="癸"：初爻玄武，顺排
4. 无效天干="子"：抛出异常

## 六、兼容性

- 与现有的硬币起卦、数字起卦功能完全兼容
- 支持传入 `yao_list` 参数，与起卦结果无缝对接
- 输出格式与现有起卦结果统一

## 七、依赖

- Python 3.x
- 仅使用内置库，无第三方依赖