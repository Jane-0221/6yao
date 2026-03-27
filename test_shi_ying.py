# -*- coding: utf-8 -*-
"""
世应推算模块测试文件

测试用例覆盖：
1. 核心函数测试
2. 边界条件测试
3. 输入容错测试
4. 格式化输出测试
5. 与gua64模块集成测试
"""

import unittest

from shi_ying import (
    # 常量
    SHIYING_MAP,
    YAO_NAMES,
    GONG_NAMES,
    GONG_GUA_MAP,
    # 核心函数
    get_shi_ying,
    calculate_ying,
    normalize_gua_name,
    validate_gua_name,
    get_yao_name,
    get_gong_name,
    get_all_gua_names,
    get_gua_info,
    # 格式化函数
    format_shi_ying_result,
    format_shi_ying_table,
    format_shi_ying_simple,
    # 查询函数
    get_shi_ying_info,
    find_gua_by_shi,
    get_guas_by_gong,
    # 验证函数
    validate_shi_ying_consistency,
)


class TestCoreFunctions(unittest.TestCase):
    """核心函数测试"""

    def test_get_shi_ying_basic(self):
        """测试基本世应计算"""
        # 测试用例：乾为天
        result = get_shi_ying("乾为天")
        self.assertEqual(result, {"shi": 6, "ying": 3})
        
        # 测试用例：天风姤
        result = get_shi_ying("天风姤")
        self.assertEqual(result, {"shi": 1, "ying": 4})
        
        # 测试用例：天山遁
        result = get_shi_ying("天山遁")
        self.assertEqual(result, {"shi": 2, "ying": 5})
        
        # 测试用例：风天小畜
        result = get_shi_ying("风天小畜")
        self.assertEqual(result, {"shi": 1, "ying": 4})
        
        # 测试用例：火天大有
        result = get_shi_ying("火天大有")
        self.assertEqual(result, {"shi": 3, "ying": 6})

    def test_get_shi_ying_all_guas(self):
        """测试所有64卦的世应计算"""
        for gua_name, shi in SHIYING_MAP.items():
            result = get_shi_ying(gua_name)
            self.assertEqual(result["shi"], shi)
            # 验证应爻计算
            expected_ying = shi + 3 if shi <= 3 else shi - 3
            self.assertEqual(result["ying"], expected_ying)

    def test_calculate_ying(self):
        """测试应爻计算函数"""
        # 世1 -> 应4
        self.assertEqual(calculate_ying(1), 4)
        # 世2 -> 应5
        self.assertEqual(calculate_ying(2), 5)
        # 世3 -> 应6
        self.assertEqual(calculate_ying(3), 6)
        # 世4 -> 应1
        self.assertEqual(calculate_ying(4), 1)
        # 世5 -> 应2
        self.assertEqual(calculate_ying(5), 2)
        # 世6 -> 应3
        self.assertEqual(calculate_ying(6), 3)

    def test_calculate_ying_invalid(self):
        """测试应爻计算函数的无效输入"""
        with self.assertRaises(ValueError):
            calculate_ying(0)
        with self.assertRaises(ValueError):
            calculate_ying(7)
        with self.assertRaises(ValueError):
            calculate_ying(-1)

    def test_get_yao_name(self):
        """测试爻位名称获取"""
        self.assertEqual(get_yao_name(1), "初爻")
        self.assertEqual(get_yao_name(2), "二爻")
        self.assertEqual(get_yao_name(3), "三爻")
        self.assertEqual(get_yao_name(4), "四爻")
        self.assertEqual(get_yao_name(5), "五爻")
        self.assertEqual(get_yao_name(6), "上爻")

    def test_get_yao_name_invalid(self):
        """测试爻位名称获取的无效输入"""
        with self.assertRaises(ValueError):
            get_yao_name(0)
        with self.assertRaises(ValueError):
            get_yao_name(7)

    def test_get_gong_name(self):
        """测试宫位获取"""
        self.assertEqual(get_gong_name("乾为天"), "乾宫")
        self.assertEqual(get_gong_name("坤为地"), "坤宫")
        self.assertEqual(get_gong_name("兑为泽"), "兑宫")
        self.assertEqual(get_gong_name("离为火"), "离宫")
        self.assertEqual(get_gong_name("震为雷"), "震宫")
        self.assertEqual(get_gong_name("巽为风"), "巽宫")
        self.assertEqual(get_gong_name("坎为水"), "坎宫")
        self.assertEqual(get_gong_name("艮为山"), "艮宫")

    def test_get_gua_info(self):
        """测试获取完整卦象信息"""
        info = get_gua_info("乾为天")
        self.assertEqual(info["gua_name"], "乾为天")
        self.assertEqual(info["gong"], "乾宫")
        self.assertEqual(info["shi"], 6)
        self.assertEqual(info["ying"], 3)
        self.assertEqual(info["shi_name"], "上爻")
        self.assertEqual(info["ying_name"], "三爻")

    def test_get_all_gua_names(self):
        """测试获取所有卦名"""
        names = get_all_gua_names()
        self.assertEqual(len(names), 64)
        self.assertIn("乾为天", names)
        self.assertIn("坤为地", names)


class TestInputValidation(unittest.TestCase):
    """输入验证测试"""

    def test_normalize_gua_name(self):
        """测试卦名规范化"""
        # 去除首尾空格
        self.assertEqual(normalize_gua_name("  乾为天  "), "乾为天")
        # 全角空格转换为无空格
        self.assertEqual(normalize_gua_name("乾　为天"), "乾为天")
        # 多个空格全部去除
        self.assertEqual(normalize_gua_name("乾  为  天"), "乾为天")
        # 空字符串
        self.assertEqual(normalize_gua_name(""), "")

    def test_validate_gua_name(self):
        """测试卦名验证"""
        self.assertTrue(validate_gua_name("乾为天"))
        self.assertTrue(validate_gua_name("坤为地"))
        self.assertFalse(validate_gua_name("不存在的卦"))
        self.assertFalse(validate_gua_name(""))

    def test_get_shi_ying_invalid_input(self):
        """测试无效卦名输入"""
        with self.assertRaises(ValueError):
            get_shi_ying("不存在的卦")
        with self.assertRaises(ValueError):
            get_shi_ying("")


class TestFormatFunctions(unittest.TestCase):
    """格式化函数测试"""

    def test_format_shi_ying_result(self):
        """测试世应结果格式化"""
        result = {"shi": 6, "ying": 3}
        output = format_shi_ying_result(result, "乾为天")
        self.assertIn("卦象：乾为天", output)
        self.assertIn("世爻：上爻（6）", output)
        self.assertIn("应爻：三爻（3）", output)

    def test_format_shi_ying_result_no_name(self):
        """测试不带卦名的格式化"""
        result = {"shi": 1, "ying": 4}
        output = format_shi_ying_result(result)
        self.assertNotIn("卦象：", output)
        self.assertIn("世爻：初爻（1）", output)
        self.assertIn("应爻：四爻（4）", output)

    def test_format_shi_ying_table(self):
        """测试表格格式化"""
        output = format_shi_ying_table("乾为天")
        self.assertIn("卦象：乾为天", output)
        self.assertIn("宫位：乾宫", output)
        self.assertIn("世爻：上爻", output)
        self.assertIn("应爻：三爻", output)

    def test_format_shi_ying_simple(self):
        """测试简洁格式化"""
        result = {"shi": 6, "ying": 3}
        output = format_shi_ying_simple(result)
        self.assertEqual(output, "世6应3")


class TestQueryFunctions(unittest.TestCase):
    """查询函数测试"""

    def test_find_gua_by_shi(self):
        """测试按世爻位置查找卦"""
        # 世爻在6爻的卦（八纯卦）
        guas = find_gua_by_shi(6)
        self.assertEqual(len(guas), 8)
        self.assertIn("乾为天", guas)
        self.assertIn("坤为地", guas)
        self.assertIn("坎为水", guas)
        self.assertIn("离为火", guas)

        # 世爻在1爻的卦
        guas = find_gua_by_shi(1)
        self.assertEqual(len(guas), 8)
        self.assertIn("天风姤", guas)
        self.assertIn("风天小畜", guas)

    def test_find_gua_by_shi_invalid(self):
        """测试无效世爻位置"""
        with self.assertRaises(ValueError):
            find_gua_by_shi(0)
        with self.assertRaises(ValueError):
            find_gua_by_shi(7)

    def test_get_guas_by_gong(self):
        """测试按宫位获取卦"""
        guas = get_guas_by_gong("乾宫")
        self.assertEqual(len(guas), 8)
        self.assertEqual(guas[0], "乾为天")

        guas = get_guas_by_gong("坤宫")
        self.assertEqual(len(guas), 8)
        self.assertEqual(guas[0], "坤为地")

    def test_get_guas_by_gong_invalid(self):
        """测试无效宫位"""
        with self.assertRaises(ValueError):
            get_guas_by_gong("不存在的宫")

    def test_get_shi_ying_info(self):
        """测试获取完整世应信息"""
        info = get_shi_ying_info("风天小畜")
        self.assertEqual(info["gua_name"], "风天小畜")
        self.assertEqual(info["gong"], "巽宫")
        self.assertEqual(info["shi"], 1)
        self.assertEqual(info["ying"], 4)


class TestConsistency(unittest.TestCase):
    """一致性验证测试"""

    def test_shiying_map_completeness(self):
        """测试64卦映射完整性"""
        self.assertEqual(len(SHIYING_MAP), 64)

    def test_gong_gua_map_completeness(self):
        """测试八宫映射完整性"""
        total = sum(len(guas) for guas in GONG_GUA_MAP.values())
        self.assertEqual(total, 64)
        
        for gong, guas in GONG_GUA_MAP.items():
            self.assertEqual(len(guas), 8, f"{gong}应有8卦")

    def test_validate_shi_ying_consistency(self):
        """测试世应一致性验证函数"""
        self.assertTrue(validate_shi_ying_consistency())

    def test_all_guas_in_map(self):
        """测试所有卦都在映射表中"""
        for gong, guas in GONG_GUA_MAP.items():
            for gua in guas:
                self.assertIn(gua, SHIYING_MAP, f"{gua}不在SHIYING_MAP中")


class TestEightPalaces(unittest.TestCase):
    """八宫卦序测试"""

    def test_qian_gong(self):
        """测试乾宫八卦"""
        guas = get_guas_by_gong("乾宫")
        self.assertEqual(guas[0], "乾为天")  # 本宫卦
        self.assertEqual(get_shi_ying(guas[0])["shi"], 6)  # 上爻世

    def test_kun_gong(self):
        """测试坤宫八卦"""
        guas = get_guas_by_gong("坤宫")
        self.assertEqual(guas[0], "坤为地")  # 本宫卦
        self.assertEqual(get_shi_ying(guas[0])["shi"], 6)  # 上爻世

    def test_all_palaces(self):
        """测试所有宫位"""
        for gong in GONG_NAMES:
            guas = get_guas_by_gong(gong)
            self.assertEqual(len(guas), 8)
            # 本宫卦（第一卦）世爻在上爻
            self.assertEqual(get_shi_ying(guas[0])["shi"], 6)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_with_gua64_module(self):
        """测试与gua64模块的集成"""
        try:
            from gua64 import calculate_gua
            
            # 测试乾为天
            result = calculate_gua([1, 1, 1, 1, 1, 1])
            # gua64_name 是标准的64卦名称（如"乾为天"）
            gua_name = result['ben_gua']['gua64_name']
            self.assertEqual(gua_name, "乾为天")
            
            shi_ying = get_shi_ying(gua_name)
            self.assertEqual(shi_ying["shi"], 6)
            self.assertEqual(shi_ying["ying"], 3)
            
            # 测试坤为地
            result = calculate_gua([2, 2, 2, 2, 2, 2])
            gua_name = result['ben_gua']['gua64_name']
            self.assertEqual(gua_name, "坤为地")
            
            shi_ying = get_shi_ying(gua_name)
            self.assertEqual(shi_ying["shi"], 6)
            self.assertEqual(shi_ying["ying"], 3)
            
        except ImportError:
            self.skipTest("gua64模块未安装")


if __name__ == '__main__':
    unittest.main(verbosity=2)