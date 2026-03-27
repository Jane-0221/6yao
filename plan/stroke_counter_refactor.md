# 笔画解析模块重构计划

## 目标
将 `stroke_counter.py` 从读取 CSV 文件方式改为直接使用 unihan-etl Python API。

## 当前实现分析

### 现有代码结构
- 使用 CSV 文件路径：`%LOCALAPPDATA%/Tony Narlock/unihan_etl/unihan.csv`
- 手动解析 CSV 获取 `kTotalStrokes`、`kTraditionalVariant`、`kSimplifiedVariant`
- 维护三个全局缓存字典：`_stroke_cache`、`_simplified_to_traditional`、`_traditional_to_simplified`

### 现有问题
1. 依赖外部 CSV 文件路径
2. 需要用户手动运行 `unihan-etl download && unihan-etl export` 命令
3. 路径硬编码，跨平台兼容性差

## unihan-etl Python API 使用方式

### 安装
```bash
pip install unihan-etl
```

### 核心 API
unihan-etl 提供以下主要组件：

```python
from unihan_etl import Unihan

# 创建 Unihan 实例
unihan = Unihan()

# 获取字符数据
# 返回包含所有 Unihan 字段的数据
data = unihan.data
```

### 关键字段
- `kTotalStrokes`: 总笔画数
- `kTraditionalVariant`: 繁体变体
- `kSimplifiedVariant`: 简体变体

## 新实现方案

### 方案一：使用 unihan-etl 的数据导出功能
```python
from unihan_etl import Unihan

def _load_unihan_data():
    global _stroke_cache, _simplified_to_traditional, _traditional_to_simplified
    
    if _stroke_cache is not None:
        return
    
    _stroke_cache = {}
    _simplified_to_traditional = {}
    _traditional_to_simplified = {}
    
    # 指定需要的字段
    unihan = Unihan(fields=['kTotalStrokes', 'kTraditionalVariant', 'kSimplifiedVariant'])
    
    for item in unihan.data:
        char = item.get('char', '')
        if not char:
            continue
        
        # 笔画数
        if 'kTotalStrokes' in item:
            _stroke_cache[char] = int(item['kTotalStrokes'])
        
        # 简繁转换映射
        if 'kTraditionalVariant' in item:
            trad = item['kTraditionalVariant']
            _simplified_to_traditional[char] = trad
            _traditional_to_simplified[trad] = char
        
        if 'kSimplifiedVariant' in item:
            simp = item['kSimplifiedVariant']
            _traditional_to_simplified[char] = simp
            _simplified_to_traditional[simp] = char
```

### 方案二：使用 unihan-etl 的表格式数据
```python
from unihan_etl import Unihan
import pandas as pd

def _load_unihan_data():
    global _stroke_cache, _simplified_to_traditional, _traditional_to_simplified
    
    if _stroke_cache is not None:
        return
    
    unihan = Unihan(fields=['kTotalStrokes', 'kTraditionalVariant', 'kSimplifiedVariant'])
    
    # 转换为 DataFrame 便于查询
    df = pd.DataFrame(unihan.data)
    
    # 构建缓存...
```

## 推荐方案

推荐使用**方案一**，原因：
1. 不依赖 pandas，减少依赖
2. 代码结构清晰
3. 与现有逻辑兼容

## 重构步骤

1. **移除 CSV 相关代码**
   - 删除 `UNIHAN_CSV_PATH` 常量
   - 删除 `_parse_unicode_ref` 函数（API 直接返回字符）

2. **修改 `_load_unihan_data` 函数**
   - 导入 `unihan_etl.Unihan`
   - 使用 API 获取数据
   - 保持缓存逻辑不变

3. **保持公共 API 不变**
   - `get_traditional(text: str) -> str`
   - `get_simplified(text: str) -> str`
   - `get_char_stroke(char: str) -> int`
   - `get_text_stroke(text: str) -> int`

4. **更新测试函数**
   - 验证新实现正确性

## 代码变更预览

```python
# -*- coding: utf-8 -*-
"""
繁体字笔画计算模块
使用 unihan-etl Python API 获取笔画数
"""

from unihan_etl import Unihan

# Unihan 数据缓存
_stroke_cache = None
_simplified_to_traditional = None
_traditional_to_simplified = None


def _load_unihan_data():
    """加载 Unihan 数据"""
    global _stroke_cache, _simplified_to_traditional, _traditional_to_simplified
    
    if _stroke_cache is not None:
        return
    
    _stroke_cache = {}
    _simplified_to_traditional = {}
    _traditional_to_simplified = {}
    
    try:
        # 使用 unihan-etl API
        unihan = Unihan(fields=['kTotalStrokes', 'kTraditionalVariant', 'kSimplifiedVariant'])
        
        for item in unihan.data:
            char = item.get('char', '')
            if not char:
                continue
            
            # 笔画数
            if 'kTotalStrokes' in item:
                try:
                    _stroke_cache[char] = int(item['kTotalStrokes'])
                except (ValueError, TypeError):
                    pass
            
            # 简体转繁体映射
            if 'kTraditionalVariant' in item:
                trad = item['kTraditionalVariant']
                if trad:
                    _simplified_to_traditional[char] = trad
                    _traditional_to_simplified[trad] = char
            
            # 繁体转简体映射
            if 'kSimplifiedVariant' in item:
                simp = item['kSimplifiedVariant']
                if simp:
                    _traditional_to_simplified[char] = simp
                    _simplified_to_traditional[simp] = char
                    
    except Exception as e:
        print(f"加载 Unihan 数据失败: {e}")


# 其余函数保持不变...
```

## 注意事项

1. **首次运行**：unihan-etl 首次使用时会自动下载数据，可能需要网络连接
2. **数据缓存**：unihan-etl 会将数据缓存在本地，后续使用无需重新下载
3. **兼容性**：公共 API 保持不变，不影响现有调用代码

## 测试计划

1. 运行 `test_stroke_counter()` 验证基本功能
2. 测试简繁转换正确性
3. 测试笔画计算准确性
4. 验证与 `divination.py` 的集成