# 64卦算法模块

根据六爻数组计算本卦和变卦的完整信息。

## 功能特性

- ✅ 八卦映射：三爻数组 → 卦名 + 自然象
- ✅ 64卦命名：根据上下卦生成完整卦名
- ✅ 本卦计算：从六爻数组得出本卦
- ✅ 变卦计算：支持单动爻和多动爻
- ✅ 格式化输出：多种输出格式

## 快速开始

### 基本用法

```python
from gua64 import calculate_gua, format_gua_result

# 计算卦象（无动爻）
result = calculate_gua([1, 1, 1, 2, 1, 1])
print(f"本卦: {result['ben_gua']['name']}")
# 输出: 本卦: 上巽下乾 风天小畜卦

# 计算卦象（有动爻）
result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
print(f"本卦: {result['ben_gua']['name']}")
print(f"变卦: {result['bian_gua']['name']}")
# 输出:
# 本卦: 上乾下坤 天地否卦
# 变卦: 上乾下艮 天山遁卦

# 格式化输出
print(format_gua_result(result))
```

### 多动爻支持

```python
from gua64 import calculate_gua

# 支持多个动爻
result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=[3, 5])
print(f"动爻: {result['moving_yao']}")
print(f"变卦: {result['bian_gua']['name']}")
```

## API 文档

### 核心函数

#### `calculate_gua(yao_list, moving_yao=None)`

主函数：计算本卦和变卦。

**参数：**
- `yao_list`: 六爻数组 `[初爻, 二爻, 三爻, 四爻, 五爻, 上爻]`
  - `1` = 阳爻，`2` = 阴爻
- `moving_yao`: 动爻位置（可选）
  - `int`: 单个动爻（如 `3`）
  - `list[int]`: 多个动爻（如 `[3, 5]`）
  - `None`: 无动爻

**返回：**
```python
{
    'ben_gua': {
        'name': '上巽下乾 风天小畜卦',
        'upper_gua': '巽',
        'lower_gua': '乾',
        'upper_nature': '风',
        'lower_nature': '天',
        'gua64_name': '风天小畜',
        'upper_trigram': (2, 1, 1),
        'lower_trigram': (1, 1, 1),
    },
    'bian_gua': None,  # 或变卦信息
    'yao_list': [1, 1, 1, 2, 1, 1],
    'moving_yao': None,  # 或 [3] 或 [3, 5]
}
```

#### `calculate_ben_gua(yao_list)`

计算本卦。

#### `calculate_bian_gua(yao_list, moving_yao)`

计算变卦。

### 辅助函数

#### `parse_yao_list(yao_list)`

解析六爻数组，返回上下卦信息。

#### `format_gua_full_name(upper_gua, lower_gua)`

生成完整的卦名。

#### `flip_yao(yao_list, moving_yao_list)`

反转动爻位置的爻值（1↔2）。

### 格式化函数

#### `format_gua_result(result)`

格式化卦象结果为简单字符串。

#### `format_gua_table(result)`

格式化卦象结果为表格形式。

#### `format_yao_visual(yao_list, moving_yao)`

格式化六爻为可视化图形。

#### `format_full_output(result)`

格式化完整输出（包含图形和详细信息）。

### 常量

#### `TRIGRAM_NAMES`

八卦二进制到卦名映射。

#### `TRIGRAM_NATURES`

八卦到自然象映射。

#### `GUA64_NAMES`

64卦名称映射表。

#### `YAO_NAMES`

爻位名称列表。

## 核心规则

### 六爻数组格式

- 格式：`[初爻, 二爻, 三爻, 四爻, 五爻, 上爻]`
- 顺序：严格从下到上
- 爻值：`1` = 阳爻，`2` = 阴爻

### 卦象拆分规则

- 下卦（内卦）= 数组前3位 `[0:3]`
- 上卦（外卦）= 数组后3位 `[3:6]`

### 八卦映射表

| 卦名 | 符号 | 二进制 | 自然象 |
|------|------|--------|--------|
| 乾 | ☰ | [1,1,1] | 天 |
| 兑 | ☱ | [1,1,2] | 泽 |
| 离 | ☲ | [1,2,1] | 火 |
| 震 | ☳ | [1,2,2] | 雷 |
| 巽 | ☴ | [2,1,1] | 风 |
| 坎 | ☵ | [2,1,2] | 水 |
| 艮 | ☶ | [2,2,1] | 山 |
| 坤 | ☷ | [2,2,2] | 地 |

### 64卦命名规则

**异卦（上下卦不同）**：
- 格式：`上{上卦名}下{下卦名} {GUA64_NAMES中的名称}卦`
- 示例：`上乾下艮 天山遁卦`

**八纯卦（上下卦相同）**：
- 格式：`上{上卦名}下{下卦名} {卦名}为{自然象}卦`
- 示例：`上乾下乾 乾为天卦`

## 示例

### 示例1：无动爻

```python
from gua64 import calculate_gua

result = calculate_gua([1, 1, 1, 2, 1, 1])
print(f"本卦: {result['ben_gua']['name']}")
print(f"变卦: 无")
```

输出：
```
本卦: 上巽下乾 风天小畜卦
变卦: 无
```

### 示例2：有动爻

```python
from gua64 import calculate_gua

result = calculate_gua([2, 2, 2, 1, 1, 1], moving_yao=3)
print(f"本卦: {result['ben_gua']['name']}")
print(f"变卦: {result['bian_gua']['name']}")
print(f"变化: {result['bian_gua']['change_detail']}")
```

输出：
```
本卦: 上乾下坤 天地否卦
变卦: 上乾下艮 天山遁卦
变化: 三爻阴变阳，下卦由坤变为艮
```

## 与现有模块集成

```python
from divination import time_divination
from gua64 import calculate_gua

# 使用时间起卦
div_result = time_divination()

# 计算卦象
gua_result = calculate_gua(
    yao_list=div_result['yao_list'],
    moving_yao=div_result['moving_yao']
)

print(f"本卦: {gua_result['ben_gua']['name']}")
if gua_result['bian_gua']:
    print(f"变卦: {gua_result['bian_gua']['name']}")
```

## 版本

- v1.0.0 - 初始版本