# 六爻地支模块 (di_zhi)

根据上下经卦计算六爻固定地支。

## 核心规则

1. **六爻地支终身固定**：同一卦的地支永远不变，与动爻、日辰、六神无关
2. **下卦（内卦）** → 决定 初爻、二爻、三爻
3. **上卦（外卦）** → 决定 四爻、五爻、上爻

## 八卦纳支表

| 经卦 | 初爻 | 二爻 | 三爻 | 四爻 | 五爻 | 上爻 |
|------|------|------|------|------|------|------|
| 乾   | 子   | 寅   | 辰   | 午   | 申   | 戌   |
| 震   | 子   | 寅   | 辰   | 午   | 申   | 戌   |
| 坎   | 寅   | 辰   | 午   | 申   | 戌   | 子   |
| 艮   | 辰   | 午   | 申   | 戌   | 子   | 寅   |
| 坤   | 未   | 巳   | 卯   | 丑   | 亥   | 酉   |
| 巽   | 丑   | 亥   | 酉   | 未   | 巳   | 卯   |
| 离   | 卯   | 丑   | 亥   | 酉   | 未   | 巳   |
| 兑   | 巳   | 卯   | 丑   | 亥   | 酉   | 未   |

## 安装使用

```python
from di_zhi import get_six_yao_di_zhi, format_di_zhi_simple
```

## API 文档

### 核心函数

#### `get_six_yao_di_zhi(upper_gua: str, lower_gua: str) -> Dict`

根据上下经卦获取六爻固定地支。

**参数：**
- `upper_gua`: 上卦名（乾/兑/离/震/巽/坎/艮/坤）
- `lower_gua`: 下卦名（乾/兑/离/震/巽/坎/艮/坤）

**返回：**
```python
{
    "di_zhi": ["子", "寅", "辰", "午", "申", "戌"],
    "upper_gua": "乾",
    "lower_gua": "乾"
}
```

**示例：**
```python
>>> from di_zhi import get_six_yao_di_zhi
>>> result = get_six_yao_di_zhi("乾", "乾")
>>> print(result["di_zhi"])
['子', '寅', '辰', '午', '申', '戌']
```

#### `get_yao_di_zhi(upper_gua: str, lower_gua: str, yao_index: int) -> str`

获取指定爻位的地支。

**参数：**
- `upper_gua`: 上卦名
- `lower_gua`: 下卦名
- `yao_index`: 爻位索引（0-5，0=初爻，5=上爻）

**返回：** 该爻位的地支字符串

**示例：**
```python
>>> from di_zhi import get_yao_di_zhi
>>> get_yao_di_zhi("乾", "乾", 0)
'子'
```

#### `validate_trigram(trigram: str) -> None`

校验卦名是否有效，无效时抛出 `ValueError`。

### 格式化函数

#### `format_di_zhi_simple(result: Dict) -> str`

简洁格式输出（用于 main.py 集成）。

```python
>>> from di_zhi import get_six_yao_di_zhi, format_di_zhi_simple
>>> result = get_six_yao_di_zhi("乾", "乾")
>>> print(format_di_zhi_simple(result))
地支: 初爻子 二爻寅 三爻辰 四爻午 五爻申 上爻戌
```

#### `format_di_zhi_inline(result: Dict) -> str`

单行格式输出。

```python
>>> print(format_di_zhi_inline(result))
地支: 子 寅 辰 午 申 戌
```

#### `format_di_zhi_result(result: Dict) -> str`

详细格式输出。

```python
>>> print(format_di_zhi_result(result))
上卦：乾 | 下卦：乾
────────────────
初爻：子
二爻：寅
三爻：辰
四爻：午
五爻：申
上爻：戌
```

#### `format_di_zhi_table(result: Dict) -> str`

表格格式输出。

```python
>>> print(format_di_zhi_table(result))
┌────────┬────────┐
│  爻位  │  地支  │
├────────┼────────┤
│ 初爻   │  子    │
│ 二爻   │  寅    │
│ 三爻   │  辰    │
│ 四爻   │  午    │
│ 五爻   │  申    │
│ 上爻   │  戌    │
└────────┴────────┘
```

## 与 gua64 模块集成

```python
from gua64 import calculate_gua
from di_zhi import get_six_yao_di_zhi, format_di_zhi_simple

# 1. 先算卦象
gua = calculate_gua([1, 1, 1, 1, 1, 1])
upper = gua["ben_gua"]["upper_gua"]
lower = gua["ben_gua"]["lower_gua"]

# 2. 计算地支
result = get_six_yao_di_zhi(upper, lower)

# 3. 格式化输出
print(f"卦象：{gua['ben_gua']['name']}")
print(format_di_zhi_simple(result))
```

## 测试用例

| 卦象 | 上卦 | 下卦 | 预期输出 |
|------|------|------|----------|
| 乾为天 | 乾 | 乾 | ["子","寅","辰","午","申","戌"] |
| 风天小畜 | 巽 | 乾 | ["子","寅","辰","未","巳","卯"] |
| 坤为地 | 坤 | 坤 | ["未","巳","卯","丑","亥","酉"] |

## 版本历史

- v1.0.0 - 初始版本，实现基本地支计算功能