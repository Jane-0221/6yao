# 六亲模块 (liu_qin)

## 模块概述

六亲模块用于计算六爻六亲。根据本宫五行和各爻地支五行，按照传统六爻规则推算六亲。

## 核心规则

### 六亲定义

六亲是根据五行生克关系确定的：

| 关系 | 六亲 | 说明 |
|------|------|------|
| 生我者 | 父母 | 生助本宫五行的五行 |
| 我生者 | 子孙 | 本宫五行所生的五行 |
| 克我者 | 官鬼 | 克制本宫五行的五行 |
| 我克者 | 妻财 | 本宫五行所克的五行 |
| 同我者 | 兄弟 | 与本宫五行相同的五行 |

### 五行生克

```
五行相生：木生火、火生土、土生金、金生水、水生木
五行相克：木克土、土克水、水克火、火克金、金克木
```

### 八宫五行

| 宫位 | 五行 |
|------|------|
| 乾宫 | 金 |
| 兑宫 | 金 |
| 离宫 | 火 |
| 震宫 | 木 |
| 巽宫 | 木 |
| 坎宫 | 水 |
| 艮宫 | 土 |
| 坤宫 | 土 |

## 使用方法

### 基本用法

```python
from liu_qin import get_six_yao_liu_qin, format_liu_qin_simple

# 计算六亲
result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])

# 简洁格式输出
print(format_liu_qin_simple(result))
# 输出: 六亲: 子孙 妻财 兄弟 官鬼 父母 兄弟
```

### 与其他模块集成

```python
from shi_ying import get_gong_name
from di_zhi import get_six_yao_di_zhi
from liu_qin import get_six_yao_liu_qin, format_liu_qin_simple

# 1. 获取卦名
gua_name = "乾为天"

# 2. 获取宫位
gong = get_gong_name(gua_name)  # "乾宫"

# 3. 获取地支
di_zhi_result = get_six_yao_di_zhi("乾", "乾")
# di_zhi_result["di_zhi"] = ["子", "寅", "辰", "午", "申", "戌"]

# 4. 计算六亲
liu_qin_result = get_six_yao_liu_qin(gong, di_zhi_result["di_zhi"])

# 5. 输出结果
print(format_liu_qin_simple(liu_qin_result))
```

### 详细格式输出

```python
from liu_qin import get_six_yao_liu_qin, format_liu_qin_result

result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
print(format_liu_qin_result(result))
```

输出：
```
宫位：乾宫（金）
─────────────────────────
初爻：子（水）→ 子孙
二爻：寅（木）→ 妻财
三爻：辰（土）→ 兄弟
四爻：午（火）→ 官鬼
五爻：申（金）→ 父母
上爻：戌（土）→ 兄弟
```

### 表格格式输出

```python
from liu_qin import get_six_yao_liu_qin, format_liu_qin_table

result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
print(format_liu_qin_table(result))
```

输出：
```
┌──────┬──────┬──────┬────────┐
│ 爻位 │ 地支 │ 五行 │  六亲  │
├──────┼──────┼──────┼────────┤
│ 初爻 │  子  │  水  │  子孙  │
│ 二爻 │  寅  │  木  │  妻财  │
│ 三爻 │  辰  │  土  │  兄弟  │
│ 四爻 │  午  │  火  │  官鬼  │
│ 五爻 │  申  │  金  │  父母  │
│ 上爻 │  戌  │  土  │  兄弟  │
└──────┴──────┴──────┴────────┘
```

## API 参考

### 核心函数

#### `get_six_yao_liu_qin(gong, di_zhi_list)`

计算六爻六亲。

**参数：**
- `gong` (str): 宫位名（如"乾宫"）
- `di_zhi_list` (List[str]): 六爻地支列表，从初爻到上爻

**返回：**
```python
{
    "liu_qin": ["子孙", "妻财", "兄弟", "官鬼", "父母", "兄弟"],
    "gong": "乾宫",
    "gong_element": "金",
    "yao_elements": ["水", "木", "土", "火", "金", "土"],
    "di_zhi": ["子", "寅", "辰", "午", "申", "戌"]
}
```

#### `get_liu_qin_by_element(self_element, yao_element)`

根据本宫五行和爻五行计算六亲。

**参数：**
- `self_element` (str): 本宫五行
- `yao_element` (str): 爻五行

**返回：**
- str: 六亲（父母/兄弟/子孙/妻财/官鬼）

#### `get_element_by_di_zhi(di_zhi)`

根据地支获取五行。

#### `get_element_by_gong(gong)`

根据宫位获取五行。

### 格式化函数

#### `format_liu_qin_simple(result)`

简洁格式输出，适合在终端显示。

#### `format_liu_qin_result(result)`

详细格式输出。

#### `format_liu_qin_table(result)`

表格格式输出。

#### `format_liu_qin_with_gua_name(result, gua_name)`

带卦名的格式化输出。

## 示例

### 乾为天（乾宫，金）

```python
result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
# liu_qin: ['子孙', '妻财', '兄弟', '官鬼', '父母', '兄弟']
```

解释：
- 初爻子水：金生水，我生者 → 子孙
- 二爻寅木：金克木，我克者 → 妻财
- 三爻辰土：土生金，生我者 → 父母（注：辰为土）
- 四爻午火：火克金，克我者 → 官鬼
- 五爻申金：金同金，同我者 → 兄弟
- 上爻戌土：土生金，生我者 → 父母（注：戌为土）

### 坤为地（坤宫，土）

```python
result = get_six_yao_liu_qin("坤宫", ["未", "巳", "卯", "丑", "亥", "酉"])
# liu_qin: ['兄弟', '父母', '官鬼', '兄弟', '妻财', '子孙']
```

## 依赖

- Python 3.6+
- 无第三方依赖

## 版本

- v1.0.0 - 初始版本