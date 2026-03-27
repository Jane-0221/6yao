# -*- coding: utf-8 -*-
"""
繁体字笔画计算模块
使用 unihan-etl Python API 获取笔画数
"""

import csv
from pathlib import Path
from unihan_etl.core import Packager, Options, download, load_data, expand_delimiters
from unihan_etl.constants import UNIHAN_MANIFEST

# Unihan 数据缓存
_stroke_cache = None
_simplified_to_traditional = None
_traditional_to_simplified = None

# 默认工作目录
WORK_DIR = Path.home() / 'AppData' / 'Local' / 'Tony Narlock' / 'unihan_etl' / 'Cache' / 'downloads'


def _parse_unicode_ref(ref: str) -> str:
    """解析 Unicode 引用，如 'U+5287' -> '劇'"""
    if not ref:
        return ''
    
    # 可能有多个引用，用空格分隔，取第一个
    ref = ref.strip().split()[0]
    
    if ref.startswith('U+'):
        try:
            code_point = int(ref[2:], 16)
            return chr(code_point)
        except ValueError:
            pass
    
    return ''


def _ucn_to_char(ucn: str) -> str:
    """将 UCN (如 U+5287) 转换为字符"""
    if ucn.startswith('U+'):
        try:
            return chr(int(ucn[2:], 16))
        except ValueError:
            pass
    return ''


def _ensure_unihan_data():
    """确保 Unihan 数据已下载"""
    if not WORK_DIR.exists():
        print("正在下载 Unihan 数据...")
        options = Options(download=True)
        packager = Packager(options)
        packager.download()
        print("Unihan 数据下载完成。")


def _load_unihan_data():
    """加载 Unihan 数据"""
    global _stroke_cache, _simplified_to_traditional, _traditional_to_simplified
    
    if _stroke_cache is not None:
        return
    
    _stroke_cache = {}
    _simplified_to_traditional = {}
    _traditional_to_simplified = {}
    
    # 确保数据已下载
    _ensure_unihan_data()
    
    # 加载笔画数据 (kTotalStrokes 在 Unihan_IRGSources.txt 中)
    irg_file = WORK_DIR / 'Unihan_IRGSources.txt'
    if irg_file.exists():
        try:
            with open(irg_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 3 and parts[1] == 'kTotalStrokes':
                        ucn = parts[0]
                        char = _ucn_to_char(ucn)
                        if char:
                            try:
                                _stroke_cache[char] = int(parts[2])
                            except ValueError:
                                pass
        except Exception as e:
            print(f"加载笔画数据失败: {e}")
    
    # 加载简繁转换数据 (kTraditionalVariant, kSimplifiedVariant 在 Unihan_Variants.txt 中)
    variants_file = WORK_DIR / 'Unihan_Variants.txt'
    if variants_file.exists():
        try:
            with open(variants_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        ucn = parts[0]
                        char = _ucn_to_char(ucn)
                        if not char:
                            continue
                        
                        field = parts[1]
                        value = parts[2]
                        
                        if field == 'kTraditionalVariant':
                            # 简体 -> 繁体
                            trad_char = _parse_unicode_ref(value)
                            if trad_char:
                                _simplified_to_traditional[char] = trad_char
                                _traditional_to_simplified[trad_char] = char
                        
                        elif field == 'kSimplifiedVariant':
                            # 繁体 -> 简体
                            simp_char = _parse_unicode_ref(value)
                            if simp_char:
                                _traditional_to_simplified[char] = simp_char
                                _simplified_to_traditional[simp_char] = char
                                
        except Exception as e:
            print(f"加载简繁转换数据失败: {e}")
    
    print(f"已加载 {len(_stroke_cache)} 个字符的笔画数据")
    print(f"已加载 {len(_simplified_to_traditional)} 个简繁转换映射")


def get_traditional(text: str) -> str:
    """
    将简体字转换为繁体字
    
    Args:
        text: 简体文本
    
    Returns:
        繁体文本
    """
    _load_unihan_data()
    
    result = []
    for char in text:
        trad = _simplified_to_traditional.get(char, char)
        result.append(trad)
    
    return ''.join(result)


def get_simplified(text: str) -> str:
    """
    将繁体字转换为简体字
    
    Args:
        text: 繁体文本
    
    Returns:
        简体文本
    """
    _load_unihan_data()
    
    result = []
    for char in text:
        simp = _traditional_to_simplified.get(char, char)
        result.append(simp)
    
    return ''.join(result)


def get_char_stroke(char: str) -> int:
    """
    获取单个汉字的笔画数（使用繁体字笔画）
    
    Args:
        char: 单个汉字（简体或繁体）
    
    Returns:
        笔画数，未收录返回 None
    """
    _load_unihan_data()
    
    # 优先查找繁体字的笔画数
    # 如果是简体字，先转换为繁体
    trad = _simplified_to_traditional.get(char)
    if trad:
        # 找到了对应的繁体字
        if trad in _stroke_cache:
            return _stroke_cache[trad]
    
    # 如果字符本身是繁体字（没有对应的简体转换），直接查找
    if char in _stroke_cache:
        return _stroke_cache[char]
    
    # 如果是繁体字，尝试查找其简体对应的繁体
    simp = _traditional_to_simplified.get(char)
    if simp:
        trad_from_simp = _simplified_to_traditional.get(simp)
        if trad_from_simp and trad_from_simp in _stroke_cache:
            return _stroke_cache[trad_from_simp]
    
    return None


def get_text_stroke(text: str) -> int:
    """
    计算文本的总笔画数（使用繁体字笔画）
    
    Args:
        text: 文本（简体或繁体）
    
    Returns:
        总笔画数
    """
    _load_unihan_data()
    
    total_strokes = 0
    missing_chars = []
    
    for char in text:
        # 跳过非汉字字符
        if not '\u4e00' <= char <= '\u9fff':
            continue
        
        stroke = get_char_stroke(char)
        if stroke is not None:
            total_strokes += stroke
        else:
            missing_chars.append(char)
    
    if missing_chars:
        trad_missing = [get_traditional(c) for c in missing_chars]
        print(f"警告：以下字符未找到笔画数据: {missing_chars} (繁体: {trad_missing})")
        # 对于未找到的字符，使用估算值（平均笔画约10画）
        total_strokes += len(missing_chars) * 10
    
    return total_strokes


def test_stroke_counter():
    """测试笔画计算功能"""
    test_cases = [
        ("刘", "劉", 15),  # 简体刘 -> 繁体劉 -> 15画
        ("张", "張", 11),  # 简体张 -> 繁体張 -> 11画
        ("王", "王", 4),   # 王字繁简相同 -> 4画
        ("李", "李", 7),   # 李字繁简相同 -> 7画
        ("股票", "股票", None),  # 词组测试
        ("汉", "漢", 14),  # 简体汉 -> 繁体漢 -> 14画
        ("体", "體", 22),  # 简体体 -> 繁体體 -> 22画 (Unihan数据)
    ]
    
    print("=" * 60)
    print("笔画计算测试（使用 unihan-etl Python API）")
    print("=" * 60)
    
    for simp, expected_trad, expected_stroke in test_cases:
        trad = get_traditional(simp)
        stroke = get_text_stroke(simp)
        
        trad_match = "[OK]" if trad == expected_trad else "[X]"
        stroke_match = "[OK]" if expected_stroke is None or stroke == expected_stroke else "[X]"
        
        print(f"简体: {simp} -> 繁体: {trad} {trad_match} -> 笔画: {stroke} {stroke_match}")
    
    print("=" * 60)


if __name__ == "__main__":
    test_stroke_counter()