# 世应推算模块 (shi_ying)

根据六爻正统规则，实现64卦世应位置自动推算。

## 核心规则

1. **世应唯一绑定卦象**：同一个卦，世爻、应爻位置永远固定不变
2. **应爻计算公式**：应爻位置 = 世爻位置 + 3（若结果 > 6，则减 6）
3. **八宫卦序与世位固定对应**

## 安装

```python
from shi_ying import get_shi_ying, format_shi_ying_result
```

## 快速开始

### 基本用法

```python
from shi_ying import get_shi_ying

# 获取世应位置
result = get_shi_ying("乾为天")
print(result)  # {"shi": 6, "ying": 3}

result = get_shi_ying("风天小畜")
print(result)  # {"shi": 1, "ying": 4}
```

### 格式化输出

```python
from shi_ying import get_shi_ying, format_shi_ying_result

result = get_shi_ying("乾为天")
print(format_shi_ying_result(result, "乾为天"))
# 输出：
# 卦象：乾为天
# 世爻：上爻（6）
# 应爻：三爻（3）
```

### 获取完整信息

```python
from shi_ying import get_gua_info

info = get_gua_info("风天小畜")
print(info)
# {
#     "gua_name": "风天小畜",
#     "gong": "巽宫",
#     "shi": 1,
#     "ying": 4,
#     "shi_name": "初爻",
#     "ying_name": "四爻"
# }
```

### 按宫位查询

```python
from shi_ying import get_guas_by_gong

# 获取乾宫八卦
guas = get_guas_by_gong("乾宫")
print(guas)
# ['乾为天', '天风姤', '天山遁', '天地否', '风地观', '山地剥', '火地晋', '火天大有']
```

### 按世爻位置查询

```python
from shi_ying import find_gua_by_shi

# 查找世爻在上爻（第6爻）的卦
guas = find_gua_by_shi(6)
print(guas)
# ['乾为天', '兑为泽', '离为火', '震为雷', '巽为风', '坎为水', '艮为山', '坤为地']
```

## API 参考

### 核心函数

#### `get_shi_ying(gua_name: str) -> dict`

根据64卦卦名获取世应位置。

**参数：**
- `gua_name`: 标准卦名，如 "乾为天"、"风天小畜"

**返回：**
- `dict`: `{"shi": 世位(1-6), "ying": 应位(1-6)}`

**异常：**
- `ValueError`: 卦名无效时抛出

#### `calculate_ying(shi: int) -> int`

根据世爻位置计算应爻位置。

**参数：**
- `shi`: 世爻位置（1-6）

**返回：**
- `int`: 应爻位置（1-6）

#### `get_gua_info(gua_name: str) -> dict`

获取卦象的完整信息。

**返回：**
```python
{
    "gua_name": "卦名",
    "gong": "宫位",
    "shi": 世位,
    "ying": 应位,
    "shi_name": "世爻名称",
    "ying_name": "应爻名称"
}
```

### 格式化函数

#### `format_shi_ying_result(result: dict, gua_name: str = None) -> str`

格式化输出世应结果。

#### `format_shi_ying_table(gua_name: str) -> str`

格式化为表格形式输出。

#### `format_shi_ying_simple(result: dict) -> str`

简洁格式输出，如 "世6应3"。

### 查询函数

#### `get_guas_by_gong(gong_name: str) -> list`

获取指定宫位的所有卦。

#### `find_gua_by_shi(shi_position: int) -> list`

查找所有世爻在指定位置的卦。

#### `get_all_gua_names() -> list`

获取所有64卦卦名列表。

### 验证函数

#### `validate_gua_name(gua_name: str) -> bool`

验证卦名是否有效。

#### `validate_shi_ying_consistency() -> bool`

验证世应映射的一致性。

## 64卦世应映射表

| 宫位 | 卦名 | 世爻 | 应爻 |
|------|------|------|------|
| 乾宫 | 乾为天 | 6 | 3 |
| 乾宫 | 天风姤 | 1 | 4 |
| 乾宫 | 天山遁 | 2 | 5 |
| 乾宫 | 天地否 | 3 | 6 |
| 乾宫 | 风地观 | 4 | 1 |
| 乾宫 | 山地剥 | 5 | 2 |
| 乾宫 | 火地晋 | 4 | 1 |
| 乾宫 | 火天大有 | 3 | 6 |
| ... | ... | ... | ... |

完整映射表见 [`shi_ying/core.py`](shi_ying/core.py) 中的 `SHIYING_MAP`。

## 与gua64模块集成

```python
from gua64 import calculate_gua
from shi_ying import get_shi_ying

# 从六爻数组计算卦象
gua_result = calculate_gua([1, 1, 1, 1, 1, 1])
gua_name = gua_result['ben_gua']['name']

# 获取世应
shi_ying = get_shi_ying(gua_name)
print(f"本卦：{gua_name}")
print(f"世爻：第{shi_ying['shi']}爻")
print(f"应爻：第{shi_ying['ying']}爻")
```

## 测试

```bash
python -m pytest test_shi_ying.py -v
```

或直接运行：

```bash
python test_shi_ying.py
```

## 版本历史

- v1.0.0: 初始版本，实现完整的64卦世应推算功能