# -*- coding: utf-8 -*-
"""
六亲模块测试文件

测试六亲计算的核心功能。
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liu_qin import (
    get_element_by_di_zhi,
    get_element_by_gong,
    get_liu_qin_by_element,
    get_six_yao_liu_qin,
    format_liu_qin_simple,
    format_liu_qin_result,
    validate_wuxing,
    validate_di_zhi,
    validate_gong,
)


class TestLiuQinBasic(unittest.TestCase):
    """六亲基础功能测试"""
    
    def test_get_element_by_di_zhi(self):
        """测试地支五行"""
        # 水地支
        self.assertEqual(get_element_by_di_zhi("子"), "水")
        self.assertEqual(get_element_by_di_zhi("亥"), "水")
        
        # 木地支
        self.assertEqual(get_element_by_di_zhi("寅"), "木")
        self.assertEqual(get_element_by_di_zhi("卯"), "木")
        
        # 火地支
        self.assertEqual(get_element_by_di_zhi("巳"), "火")
        self.assertEqual(get_element_by_di_zhi("午"), "火")
        
        # 金地支
        self.assertEqual(get_element_by_di_zhi("申"), "金")
        self.assertEqual(get_element_by_di_zhi("酉"), "金")
        
        # 土地支
        self.assertEqual(get_element_by_di_zhi("丑"), "土")
        self.assertEqual(get_element_by_di_zhi("辰"), "土")
        self.assertEqual(get_element_by_di_zhi("未"), "土")
        self.assertEqual(get_element_by_di_zhi("戌"), "土")
    
    def test_get_element_by_gong(self):
        """测试宫位五行"""
        # 金宫
        self.assertEqual(get_element_by_gong("乾宫"), "金")
        self.assertEqual(get_element_by_gong("兑宫"), "金")
        
        # 火宫
        self.assertEqual(get_element_by_gong("离宫"), "火")
        
        # 木宫
        self.assertEqual(get_element_by_gong("震宫"), "木")
        self.assertEqual(get_element_by_gong("巽宫"), "木")
        
        # 水宫
        self.assertEqual(get_element_by_gong("坎宫"), "水")
        
        # 土宫
        self.assertEqual(get_element_by_gong("艮宫"), "土")
        self.assertEqual(get_element_by_gong("坤宫"), "土")
    
    def test_get_liu_qin_by_element_gold(self):
        """测试金为本宫的六亲关系"""
        # 同我者 → 兄弟
        self.assertEqual(get_liu_qin_by_element("金", "金"), "兄弟")
        
        # 我生者（金生水）→ 子孙
        self.assertEqual(get_liu_qin_by_element("金", "水"), "子孙")
        
        # 我克者（金克木）→ 妻财
        self.assertEqual(get_liu_qin_by_element("金", "木"), "妻财")
        
        # 生我者（土生金）→ 父母
        self.assertEqual(get_liu_qin_by_element("金", "土"), "父母")
        
        # 克我者（火克金）→ 官鬼
        self.assertEqual(get_liu_qin_by_element("金", "火"), "官鬼")
    
    def test_get_liu_qin_by_element_wood(self):
        """测试木为本宫的六亲关系"""
        # 同我者 → 兄弟
        self.assertEqual(get_liu_qin_by_element("木", "木"), "兄弟")
        
        # 我生者（木生火）→ 子孙
        self.assertEqual(get_liu_qin_by_element("木", "火"), "子孙")
        
        # 我克者（木克土）→ 妻财
        self.assertEqual(get_liu_qin_by_element("木", "土"), "妻财")
        
        # 生我者（水生木）→ 父母
        self.assertEqual(get_liu_qin_by_element("木", "水"), "父母")
        
        # 克我者（金克木）→ 官鬼
        self.assertEqual(get_liu_qin_by_element("木", "金"), "官鬼")
    
    def test_get_liu_qin_by_element_water(self):
        """测试水为本宫的六亲关系"""
        self.assertEqual(get_liu_qin_by_element("水", "水"), "兄弟")
        self.assertEqual(get_liu_qin_by_element("水", "木"), "子孙")
        self.assertEqual(get_liu_qin_by_element("水", "火"), "妻财")
        self.assertEqual(get_liu_qin_by_element("水", "金"), "父母")
        self.assertEqual(get_liu_qin_by_element("水", "土"), "官鬼")
    
    def test_get_liu_qin_by_element_fire(self):
        """测试火为本宫的六亲关系"""
        self.assertEqual(get_liu_qin_by_element("火", "火"), "兄弟")
        self.assertEqual(get_liu_qin_by_element("火", "土"), "子孙")
        self.assertEqual(get_liu_qin_by_element("火", "金"), "妻财")
        self.assertEqual(get_liu_qin_by_element("火", "木"), "父母")
        self.assertEqual(get_liu_qin_by_element("火", "水"), "官鬼")
    
    def test_get_liu_qin_by_element_earth(self):
        """测试土为本宫的六亲关系"""
        self.assertEqual(get_liu_qin_by_element("土", "土"), "兄弟")
        self.assertEqual(get_liu_qin_by_element("土", "金"), "子孙")
        self.assertEqual(get_liu_qin_by_element("土", "水"), "妻财")
        self.assertEqual(get_liu_qin_by_element("土", "火"), "父母")
        self.assertEqual(get_liu_qin_by_element("土", "木"), "官鬼")


class TestSixYaoLiuQin(unittest.TestCase):
    """六爻六亲计算测试"""
    
    def test_qian_wei_tian(self):
        """测试乾为天（乾宫，金）"""
        # 乾为天：子、寅、辰、午、申、戌
        di_zhi = ["子", "寅", "辰", "午", "申", "戌"]
        result = get_six_yao_liu_qin("乾宫", di_zhi)
        
        self.assertEqual(result["gong"], "乾宫")
        self.assertEqual(result["gong_element"], "金")
        self.assertEqual(result["di_zhi"], di_zhi)
        
        # 验证五行
        self.assertEqual(result["yao_elements"], ["水", "木", "土", "火", "金", "土"])
        
        # 验证六亲
        # 子水：金生水 → 子孙
        # 寅木：金克木 → 妻财
        # 辰土：土生金 → 父母
        # 午火：火克金 → 官鬼
        # 申金：同金 → 兄弟
        # 戌土：土生金 → 父母
        self.assertEqual(result["liu_qin"], ["子孙", "妻财", "父母", "官鬼", "兄弟", "父母"])
    
    def test_kun_wei_di(self):
        """测试坤为地（坤宫，土）"""
        # 坤为地：未、巳、卯、丑、亥、酉
        di_zhi = ["未", "巳", "卯", "丑", "亥", "酉"]
        result = get_six_yao_liu_qin("坤宫", di_zhi)
        
        self.assertEqual(result["gong"], "坤宫")
        self.assertEqual(result["gong_element"], "土")
        
        # 验证五行
        self.assertEqual(result["yao_elements"], ["土", "火", "木", "土", "水", "金"])
        
        # 验证六亲
        # 未土：同土 → 兄弟
        # 巳火：火生土 → 父母
        # 卯木：木克土 → 官鬼
        # 丑土：同土 → 兄弟
        # 亥水：土克水 → 妻财
        # 酉金：土生金 → 子孙
        self.assertEqual(result["liu_qin"], ["兄弟", "父母", "官鬼", "兄弟", "妻财", "子孙"])
    
    def test_li_wei_huo(self):
        """测试离为火（离宫，火）"""
        # 离为火：卯、丑、亥、酉、未、巳
        di_zhi = ["卯", "丑", "亥", "酉", "未", "巳"]
        result = get_six_yao_liu_qin("离宫", di_zhi)
        
        self.assertEqual(result["gong"], "离宫")
        self.assertEqual(result["gong_element"], "火")
        
        # 验证五行
        self.assertEqual(result["yao_elements"], ["木", "土", "水", "金", "土", "火"])
        
        # 验证六亲
        # 卯木：木生火 → 父母
        # 丑土：火生土 → 子孙
        # 亥水：水克火 → 官鬼
        # 酉金：火克金 → 妻财
        # 未土：火生土 → 子孙
        # 巳火：同火 → 兄弟
        self.assertEqual(result["liu_qin"], ["父母", "子孙", "官鬼", "妻财", "子孙", "兄弟"])
    
    def test_kan_wei_shui(self):
        """测试坎为水（坎宫，水）"""
        # 坎为水：寅、辰、午、申、戌、子
        di_zhi = ["寅", "辰", "午", "申", "戌", "子"]
        result = get_six_yao_liu_qin("坎宫", di_zhi)
        
        self.assertEqual(result["gong"], "坎宫")
        self.assertEqual(result["gong_element"], "水")
        
        # 验证五行
        self.assertEqual(result["yao_elements"], ["木", "土", "火", "金", "土", "水"])
        
        # 验证六亲
        # 寅木：水生木 → 子孙
        # 辰土：土克水 → 官鬼
        # 午火：水克火 → 妻财
        # 申金：金生水 → 父母
        # 戌土：土克水 → 官鬼
        # 子水：同水 → 兄弟
        self.assertEqual(result["liu_qin"], ["子孙", "官鬼", "妻财", "父母", "官鬼", "兄弟"])


class TestValidation(unittest.TestCase):
    """输入验证测试"""
    
    def test_invalid_di_zhi(self):
        """测试无效地支"""
        with self.assertRaises(ValueError):
            get_element_by_di_zhi("无效")
        
        with self.assertRaises(ValueError):
            get_element_by_di_zhi("abc")
    
    def test_invalid_gong(self):
        """测试无效宫位"""
        with self.assertRaises(ValueError):
            get_element_by_gong("无效宫")
        
        with self.assertRaises(ValueError):
            get_element_by_gong("乾")  # 缺少"宫"字
    
    def test_invalid_wuxing(self):
        """测试无效五行"""
        with self.assertRaises(ValueError):
            get_liu_qin_by_element("无效", "金")
        
        with self.assertRaises(ValueError):
            get_liu_qin_by_element("金", "无效")
    
    def test_invalid_di_zhi_list_length(self):
        """测试地支列表长度错误"""
        with self.assertRaises(ValueError):
            get_six_yao_liu_qin("乾宫", ["子", "寅"])  # 长度不足
        
        with self.assertRaises(ValueError):
            get_six_yao_liu_qin("乾宫", ["子"] * 7)  # 长度超出
    
    def test_invalid_di_zhi_list_type(self):
        """测试地支列表类型错误"""
        with self.assertRaises(ValueError):
            get_six_yao_liu_qin("乾宫", "不是列表")


class TestFormatFunctions(unittest.TestCase):
    """格式化函数测试"""
    
    def test_format_liu_qin_simple(self):
        """测试简洁格式输出"""
        result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        output = format_liu_qin_simple(result)
        
        self.assertIn("六亲:", output)
        self.assertIn("子孙", output)
        self.assertIn("妻财", output)
        self.assertIn("兄弟", output)
    
    def test_format_liu_qin_result(self):
        """测试详细格式输出"""
        result = get_six_yao_liu_qin("乾宫", ["子", "寅", "辰", "午", "申", "戌"])
        output = format_liu_qin_result(result)
        
        self.assertIn("宫位：乾宫", output)
        self.assertIn("金", output)
        self.assertIn("初爻", output)
        self.assertIn("上爻", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)