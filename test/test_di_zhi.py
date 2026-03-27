# -*- coding: utf-8 -*-
"""
六爻地支模块测试文件

测试用例覆盖：
1. 核心函数测试
2. 边界条件测试
3. 输入容错测试
4. 格式化输出测试
5. 与gua64模块集成测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from di_zhi import (
    # 常量
    TRIGRAM_NAZHI,
    VALID_TRIGRAMS,
    YAO_NAMES,
    # 核心函数
    validate_trigram,
    get_six_yao_di_zhi,
    get_yao_di_zhi,
    # 格式化函数
    format_di_zhi_result,
    format_di_zhi_table,
    format_di_zhi_simple,
    format_di_zhi_inline,
    format_di_zhi_with_gua_name,
)


class TestCoreFunctions(unittest.TestCase):
    """核心函数测试"""

    def test_get_six_yao_di_zhi_qian_wei_tian(self):
        """测试乾为天（上乾下乾）"""
        result = get_six_yao_di_zhi("乾", "乾")
        self.assertEqual(result["di_zhi"], ["子", "寅", "辰", "午", "申", "戌"])
        self.assertEqual(result["upper_gua"], "乾")
        self.assertEqual(result["lower_gua"], "乾")

    def test_get_six_yao_di_zhi_feng_tian_xiao_chu(self):
        """测试风天小畜（上巽下乾）"""
        result = get_six_yao_di_zhi("巽", "乾")
        # 下卦乾前3位: 子、寅、辰
        # 上卦巽后3位: 未、巳、卯
        self.assertEqual(result["di_zhi"], ["子", "寅", "辰", "未", "巳", "卯"])
        self.assertEqual(result["upper_gua"], "巽")
        self.assertEqual(result["lower_gua"], "乾")

    def test_get_six_yao_di_zhi_kun_wei_di(self):
        """测试坤为地（上坤下坤）"""
        result = get_six_yao_di_zhi("坤", "坤")
        self.assertEqual(result["di_zhi"], ["未", "巳", "卯", "丑", "亥", "酉"])
        self.assertEqual(result["upper_gua"], "坤")
        self.assertEqual(result["lower_gua"], "坤")

    def test_get_six_yao_di_zhi_all_trigrams(self):
        """测试所有八卦组合的地支计算"""
        # 测试所有八卦作为下卦
        for trigram in VALID_TRIGRAMS:
            result = get_six_yao_di_zhi("乾", trigram)
            # 验证下卦前3位
            expected_lower = TRIGRAM_NAZHI[trigram][:3]
            self.assertEqual(result["di_zhi"][:3], expected_lower)
        
        # 测试所有八卦作为上卦
        for trigram in VALID_TRIGRAMS:
            result = get_six_yao_di_zhi(trigram, "乾")
            # 验证上卦后3位
            expected_upper = TRIGRAM_NAZHI[trigram][3:]
            self.assertEqual(result["di_zhi"][3:], expected_upper)

    def test_get_yao_di_zhi(self):
        """测试获取指定爻位地支"""
        # 乾为天
        self.assertEqual(get_yao_di_zhi("乾", "乾", 0), "子")  # 初爻
        self.assertEqual(get_yao_di_zhi("乾", "乾", 1), "寅")  # 二爻
        self.assertEqual(get_yao_di_zhi("乾", "乾", 2), "辰")  # 三爻
        self.assertEqual(get_yao_di_zhi("乾", "乾", 3), "午")  # 四爻
        self.assertEqual(get_yao_di_zhi("乾", "乾", 4), "申")  # 五爻
        self.assertEqual(get_yao_di_zhi("乾", "乾", 5), "戌")  # 上爻

    def test_validate_trigram_valid(self):
        """测试有效卦名校验"""
        for trigram in VALID_TRIGRAMS:
            # 不应抛出异常
            validate_trigram(trigram)

    def test_validate_trigram_invalid(self):
        """测试无效卦名校验"""
        # 无效卦名
        with self.assertRaises(ValueError):
            validate_trigram("无效")
        
        with self.assertRaises(ValueError):
            validate_trigram("123")
        
        # 类型错误
        with self.assertRaises(ValueError):
            validate_trigram(123)
        
        with self.assertRaises(ValueError):
            validate_trigram(None)


class TestInputValidation(unittest.TestCase):
    """输入容错测试"""

    def test_invalid_upper_gua(self):
        """测试无效上卦"""
        with self.assertRaises(ValueError):
            get_six_yao_di_zhi("无效", "乾")

    def test_invalid_lower_gua(self):
        """测试无效下卦"""
        with self.assertRaises(ValueError):
            get_six_yao_di_zhi("乾", "无效")

    def test_invalid_yao_index(self):
        """测试无效爻位索引"""
        with self.assertRaises(ValueError):
            get_yao_di_zhi("乾", "乾", -1)
        
        with self.assertRaises(ValueError):
            get_yao_di_zhi("乾", "乾", 6)
        
        with self.assertRaises(ValueError):
            get_yao_di_zhi("乾", "乾", "0")

    def test_trigram_with_spaces(self):
        """测试带空格的卦名"""
        # validate_trigram 会自动 strip
        result = get_six_yao_di_zhi(" 乾 ", " 乾 ")
        self.assertEqual(result["di_zhi"], ["子", "寅", "辰", "午", "申", "戌"])


class TestFormatFunctions(unittest.TestCase):
    """格式化输出测试"""

    def test_format_di_zhi_simple(self):
        """测试简洁格式输出"""
        result = get_six_yao_di_zhi("乾", "乾")
        output = format_di_zhi_simple(result)
        self.assertEqual(output, "地支: 初爻子 二爻寅 三爻辰 四爻午 五爻申 上爻戌")

    def test_format_di_zhi_inline(self):
        """测试单行格式输出"""
        result = get_six_yao_di_zhi("乾", "乾")
        output = format_di_zhi_inline(result)
        self.assertEqual(output, "地支: 子 寅 辰 午 申 戌")

    def test_format_di_zhi_result(self):
        """测试详细格式输出"""
        result = get_six_yao_di_zhi("乾", "乾")
        output = format_di_zhi_result(result)
        self.assertIn("上卦：乾", output)
        self.assertIn("下卦：乾", output)
        self.assertIn("初爻：子", output)
        self.assertIn("上爻：戌", output)

    def test_format_di_zhi_table(self):
        """测试表格格式输出"""
        result = get_six_yao_di_zhi("乾", "乾")
        output = format_di_zhi_table(result)
        self.assertIn("爻位", output)
        self.assertIn("地支", output)
        self.assertIn("初爻", output)
        self.assertIn("子", output)

    def test_format_di_zhi_with_gua_name(self):
        """测试带卦名的格式化输出"""
        result = get_six_yao_di_zhi("乾", "乾")
        output = format_di_zhi_with_gua_name(result, "乾为天")
        self.assertIn("卦象：乾为天", output)
        self.assertIn("上卦：乾", output)
        self.assertIn("下卦：乾", output)


class TestSpecificCases(unittest.TestCase):
    """特定测试用例"""

    def test_qian_zhen_same_nazhi(self):
        """测试乾卦和震卦纳支相同"""
        qian_result = get_six_yao_di_zhi("乾", "乾")
        zhen_result = get_six_yao_di_zhi("震", "震")
        self.assertEqual(qian_result["di_zhi"], zhen_result["di_zhi"])

    def test_li_gua_nazhi(self):
        """测试离卦地支"""
        # 离为火（上离下离）
        result = get_six_yao_di_zhi("离", "离")
        # 离卦纳支: 卯、丑、亥、酉、未、巳
        # 下卦前3位: 卯、丑、亥
        # 上卦后3位: 未、巳、卯
        # 注意：这里需要验证
        expected = TRIGRAM_NAZHI["离"][:3] + TRIGRAM_NAZHI["离"][3:]
        self.assertEqual(result["di_zhi"], expected)

    def test_dui_gua_nazhi(self):
        """测试兑卦地支"""
        # 兑为泽（上兑下兑）
        result = get_six_yao_di_zhi("兑", "兑")
        expected = TRIGRAM_NAZHI["兑"][:3] + TRIGRAM_NAZHI["兑"][3:]
        self.assertEqual(result["di_zhi"], expected)

    def test_kan_gua_nazhi(self):
        """测试坎卦地支"""
        # 坎为水（上坎下坎）
        result = get_six_yao_di_zhi("坎", "坎")
        expected = TRIGRAM_NAZHI["坎"][:3] + TRIGRAM_NAZHI["坎"][3:]
        self.assertEqual(result["di_zhi"], expected)

    def test_gen_gua_nazhi(self):
        """测试艮卦地支"""
        # 艮为山（上艮下艮）
        result = get_six_yao_di_zhi("艮", "艮")
        expected = TRIGRAM_NAZHI["艮"][:3] + TRIGRAM_NAZHI["艮"][3:]
        self.assertEqual(result["di_zhi"], expected)

    def test_xun_gua_nazhi(self):
        """测试巽卦地支"""
        # 巽为风（上巽下巽）
        result = get_six_yao_di_zhi("巽", "巽")
        expected = TRIGRAM_NAZHI["巽"][:3] + TRIGRAM_NAZHI["巽"][3:]
        self.assertEqual(result["di_zhi"], expected)


class TestIntegration(unittest.TestCase):
    """与gua64模块集成测试"""

    def test_integration_with_gua64(self):
        """测试与gua64模块集成"""
        try:
            from gua64 import calculate_gua
            
            # 测试乾为天
            # yao_list格式: [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
            # 下卦 = [0:3], 上卦 = [3:6]
            gua = calculate_gua([1, 1, 1, 1, 1, 1])  # 上乾下乾
            upper = gua["ben_gua"]["upper_gua"]
            lower = gua["ben_gua"]["lower_gua"]
            
            result = get_six_yao_di_zhi(upper, lower)
            self.assertEqual(result["di_zhi"], ["子", "寅", "辰", "午", "申", "戌"])
            
            # 测试风天小畜（上巽下乾）
            # 下卦 = [1, 1, 1] = 乾, 上卦 = [2, 1, 1] = 巽
            gua = calculate_gua([1, 1, 1, 2, 1, 1])  # 上巽下乾
            upper = gua["ben_gua"]["upper_gua"]
            lower = gua["ben_gua"]["lower_gua"]
            
            result = get_six_yao_di_zhi(upper, lower)
            # 下卦乾前3位: 子、寅、辰
            # 上卦巽后3位: 未、巳、卯
            self.assertEqual(result["di_zhi"], ["子", "寅", "辰", "未", "巳", "卯"])
            
        except ImportError:
            self.skipTest("gua64模块未安装")


if __name__ == "__main__":
    unittest.main()