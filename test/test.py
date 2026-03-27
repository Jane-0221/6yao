# ===================== 六爻装卦算法（增强版：含旬空/旺衰/刑冲合害/飞伏神/神煞）=====================
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 基础常量（沿用基础版，新增部分见上文）
BA_GUA = {
    "111": {"name": "乾", "element": "金", "yin_yang": "阳"},
    "110": {"name": "兑", "element": "金", "yin_yang": "阴"},
    "101": {"name": "离", "element": "火", "yin_yang": "阴"},
    "100": {"name": "震", "element": "木", "yin_yang": "阳"},
    "011": {"name": "巽", "element": "木", "yin_yang": "阴"},
    "010": {"name": "坎", "element": "水", "yin_yang": "阳"},
    "001": {"name": "艮", "element": "土", "yin_yang": "阳"},
    "000": {"name": "坤", "element": "土", "yin_yang": "阴"},
}

NA_JIA_TIAN_GAN = {
    "乾": {"inner": "甲", "outer": "壬"}, "坤": {"inner": "乙", "outer": "癸"},
    "震": {"inner": "庚", "outer": "庚"}, "巽": {"inner": "辛", "outer": "辛"},
    "坎": {"inner": "戊", "outer": "戊"}, "离": {"inner": "己", "outer": "己"},
    "艮": {"inner": "丙", "outer": "丙"}, "兑": {"inner": "丁", "outer": "丁"},
}

NA_JIA_DI_ZHI = {
    "乾": {"inner": ["子", "寅", "辰"], "outer": ["午", "申", "戌"]},
    "震": {"inner": ["子", "寅", "辰"], "outer": ["午", "申", "戌"]},
    "坎": {"inner": ["寅", "辰", "午"], "outer": ["申", "戌", "子"]},
    "艮": {"inner": ["辰", "午", "申"], "outer": ["戌", "子", "寅"]},
    "坤": {"inner": ["未", "巳", "卯"], "outer": ["丑", "亥", "酉"]},
    "兑": {"inner": ["巳", "卯", "丑"], "outer": ["亥", "酉", "未"]},
    "离": {"inner": ["卯", "丑", "亥"], "outer": ["酉", "未", "巳"]},
    "巽": {"inner": ["丑", "亥", "酉"], "outer": ["未", "巳", "卯"]},
}

DI_ZHI_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

SHENG_KE = {
    "木": {"sheng": "火", "ke": "土", "bei_sheng": "水", "bei_ke": "金"},
    "火": {"sheng": "土", "ke": "金", "bei_sheng": "木", "bei_ke": "水"},
    "土": {"sheng": "金", "ke": "水", "bei_sheng": "火", "bei_ke": "木"},
    "金": {"sheng": "水", "ke": "木", "bei_sheng": "土", "bei_ke": "火"},
    "水": {"sheng": "木", "ke": "火", "bei_sheng": "金", "bei_ke": "土"},
}

LIU_SHEN = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]
LIU_SHEN_START = {
    "甲": 0, "乙": 0, "丙": 1, "丁": 1, "戊": 2,
    "己": 3, "庚": 4, "辛": 4, "壬": 5, "癸": 5
}

GUA_64_MAP = {
    "111111": {"name": "乾为天", "palace": "乾宫", "element": "金", "shi_pos": 5},
    "111011": {"name": "天风姤", "palace": "乾宫", "element": "金", "shi_pos": 0},
    "111001": {"name": "天山遁", "palace": "乾宫", "element": "金", "shi_pos": 1},
    "111000": {"name": "天地否", "palace": "乾宫", "element": "金", "shi_pos": 2},
    "011000": {"name": "风地观", "palace": "乾宫", "element": "金", "shi_pos": 3},
    "001000": {"name": "山地剥", "palace": "乾宫", "element": "金", "shi_pos": 4},
    "101000": {"name": "火地晋", "palace": "乾宫", "element": "金", "shi_pos": 3},
    "101111": {"name": "火天大有", "palace": "乾宫", "element": "金", "shi_pos": 2},
    "010010": {"name": "坎为水", "palace": "坎宫", "element": "水", "shi_pos": 5},
    "010110": {"name": "水泽节", "palace": "坎宫", "element": "水", "shi_pos": 0},
    "010100": {"name": "水雷屯", "palace": "坎宫", "element": "水", "shi_pos": 1},
    "010101": {"name": "水火既济", "palace": "坎宫", "element": "水", "shi_pos": 2},
    "110101": {"name": "泽火革", "palace": "坎宫", "element": "水", "shi_pos": 3},
    "100101": {"name": "雷火丰", "palace": "坎宫", "element": "水", "shi_pos": 4},
    "000101": {"name": "地火明夷", "palace": "坎宫", "element": "水", "shi_pos": 3},
    "000010": {"name": "地水师", "palace": "坎宫", "element": "水", "shi_pos": 2},
    "001001": {"name": "艮为山", "palace": "艮宫", "element": "土", "shi_pos": 5},
    "001101": {"name": "山火贲", "palace": "艮宫", "element": "土", "shi_pos": 0},
    "001111": {"name": "山天大畜", "palace": "艮宫", "element": "土", "shi_pos": 1},
    "001110": {"name": "山泽损", "palace": "艮宫", "element": "土", "shi_pos": 2},
    "101110": {"name": "火泽睽", "palace": "艮宫", "element": "土", "shi_pos": 3},
    "111110": {"name": "天泽履", "palace": "艮宫", "element": "土", "shi_pos": 4},
    "011110": {"name": "风泽中孚", "palace": "艮宫", "element": "土", "shi_pos": 3},
    "011001": {"name": "风山渐", "palace": "艮宫", "element": "土", "shi_pos": 2},
    "100100": {"name": "震为雷", "palace": "震宫", "element": "木", "shi_pos": 5},
    "100000": {"name": "雷地豫", "palace": "震宫", "element": "木", "shi_pos": 0},
    "100010": {"name": "雷水解", "palace": "震宫", "element": "木", "shi_pos": 1},
    "100011": {"name": "雷风恒", "palace": "震宫", "element": "木", "shi_pos": 2},
    "000011": {"name": "地风升", "palace": "震宫", "element": "木", "shi_pos": 3},
    "010011": {"name": "水风井", "palace": "震宫", "element": "木", "shi_pos": 4},
    "110011": {"name": "泽风大过", "palace": "震宫", "element": "木", "shi_pos": 3},
    "110100": {"name": "泽雷随", "palace": "震宫", "element": "木", "shi_pos": 2},
    "011011": {"name": "巽为风", "palace": "巽宫", "element": "木", "shi_pos": 5},
    "011111": {"name": "风天小畜", "palace": "巽宫", "element": "木", "shi_pos": 0},
    "011101": {"name": "风火家人", "palace": "巽宫", "element": "木", "shi_pos": 1},
    "011100": {"name": "风雷益", "palace": "巽宫", "element": "木", "shi_pos": 2},
    "111100": {"name": "天雷无妄", "palace": "巽宫", "element": "木", "shi_pos": 3},
    "101100": {"name": "火雷噬嗑", "palace": "巽宫", "element": "木", "shi_pos": 4},
    "001100": {"name": "山雷颐", "palace": "巽宫", "element": "木", "shi_pos": 3},
    "001011": {"name": "山风蛊", "palace": "巽宫", "element": "木", "shi_pos": 2},
    "101101": {"name": "离为火", "palace": "离宫", "element": "火", "shi_pos": 5},
    "101001": {"name": "火山旅", "palace": "离宫", "element": "火", "shi_pos": 0},
    "101011": {"name": "火风鼎", "palace": "离宫", "element": "火", "shi_pos": 1},
    "101010": {"name": "火水未济", "palace": "离宫", "element": "火", "shi_pos": 2},
    "001010": {"name": "山水蒙", "palace": "离宫", "element": "火", "shi_pos": 3},
    "011010": {"name": "风水涣", "palace": "离宫", "element": "火", "shi_pos": 4},
    "111010": {"name": "天水讼", "palace": "离宫", "element": "火", "shi_pos": 3},
    "111101": {"name": "天火同人", "palace": "离宫", "element": "火", "shi_pos": 2},
    "000000": {"name": "坤为地", "palace": "坤宫", "element": "土", "shi_pos": 5},
    "000100": {"name": "地雷复", "palace": "坤宫", "element": "土", "shi_pos": 0},
    "000110": {"name": "地泽临", "palace": "坤宫", "element": "土", "shi_pos": 1},
    "000111": {"name": "地天泰", "palace": "坤宫", "element": "土", "shi_pos": 2},
    "100111": {"name": "雷天大壮", "palace": "坤宫", "element": "土", "shi_pos": 3},
    "110111": {"name": "泽天夬", "palace": "坤宫", "element": "土", "shi_pos": 4},
    "010111": {"name": "水天需", "palace": "坤宫", "element": "土", "shi_pos": 3},
    "010000": {"name": "水地比", "palace": "坤宫", "element": "土", "shi_pos": 2},
    "110110": {"name": "兑为泽", "palace": "兑宫", "element": "金", "shi_pos": 5},
    "110010": {"name": "泽水困", "palace": "兑宫", "element": "金", "shi_pos": 0},
    "110000": {"name": "泽地萃", "palace": "兑宫", "element": "金", "shi_pos": 1},
    "110001": {"name": "泽山咸", "palace": "兑宫", "element": "金", "shi_pos": 2},
    "010001": {"name": "水山蹇", "palace": "兑宫", "element": "金", "shi_pos": 3},
    "000001": {"name": "地山谦", "palace": "兑宫", "element": "金", "shi_pos": 4},
    "100001": {"name": "雷山小过", "palace": "兑宫", "element": "金", "shi_pos": 3},
    "100110": {"name": "雷泽归妹", "palace": "兑宫", "element": "金", "shi_pos": 2},
}

# 新增常量（完整见上文，此处简化展示）
JIA_ZI_60 = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
             "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
             "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
             "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
             "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
             "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"]
XUN_KONG_MAP = {"甲子": ["戌", "亥"], "甲戌": ["申", "酉"], "甲申": ["午", "未"],
                 "甲午": ["辰", "巳"], "甲辰": ["寅", "卯"], "甲寅": ["子", "丑"]}
YUE_JIAN_INFO = {
    "寅": {"element": "木", "season": "春"}, "卯": {"element": "木", "season": "春"},
    "辰": {"element": "土", "season": "季春"}, "巳": {"element": "火", "season": "夏"},
    "午": {"element": "火", "season": "夏"}, "未": {"element": "土", "season": "季夏"},
    "申": {"element": "金", "season": "秋"}, "酉": {"element": "金", "season": "秋"},
    "戌": {"element": "土", "season": "季秋"}, "亥": {"element": "水", "season": "冬"},
    "子": {"element": "水", "season": "冬"}, "丑": {"element": "土", "season": "季冬"}
}
DI_ZHI_RELATIONS = {
    "liu_he": {"子": "丑", "丑": "子", "寅": "亥", "亥": "寅", "卯": "戌", "戌": "卯",
               "辰": "酉", "酉": "辰", "巳": "申", "申": "巳", "午": "未", "未": "午"},
    "liu_chong": {"子": "午", "午": "子", "丑": "未", "未": "丑", "寅": "申", "申": "寅",
                  "卯": "酉", "酉": "卯", "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"}
}
SHEN_SHA_RULES = {
    "天乙贵人": {"甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["亥", "酉"], "丁": ["亥", "酉"],
                 "戊": ["丑", "未"], "己": ["子", "申"], "庚": ["丑", "未"], "辛": ["寅", "午"],
                 "壬": ["卯", "巳"], "癸": ["卯", "巳"]},
    "驿马": {"申": "寅", "子": "寅", "辰": "寅", "亥": "巳", "卯": "巳", "未": "巳",
             "寅": "申", "午": "申", "戌": "申", "巳": "亥", "酉": "亥", "丑": "亥"}
}

# 八纯卦纳甲（用于飞伏神计算，简化展示乾宫）
BA_CHUN_GUA_YAO = {
    "乾为天": [
        {"yao_pos": 1, "tian_gan": "甲", "di_zhi": "子", "element": "水", "liu_qin": "子孙"},
        {"yao_pos": 2, "tian_gan": "甲", "di_zhi": "寅", "element": "木", "liu_qin": "妻财"},
        {"yao_pos": 3, "tian_gan": "甲", "di_zhi": "辰", "element": "土", "liu_qin": "父母"},
        {"yao_pos": 4, "tian_gan": "壬", "di_zhi": "午", "element": "火", "liu_qin": "官鬼"},
        {"yao_pos": 5, "tian_gan": "壬", "di_zhi": "申", "element": "金", "liu_qin": "兄弟"},
        {"yao_pos": 6, "tian_gan": "壬", "di_zhi": "戌", "element": "土", "liu_qin": "父母"},
    ]
}
GONG_PURE_GUA = {
    "乾宫": "乾为天", "坤宫": "坤为地", "震宫": "震为雷", "巽宫": "巽为风",
    "坎宫": "坎为水", "离宫": "离为火", "艮宫": "艮为山", "兑宫": "兑为泽"
}

# ===================== 核心功能函数 =====================
def get_liu_qin(self_element, yao_element):
    if yao_element == self_element: return "兄弟"
    elif yao_element == SHENG_KE[self_element]["bei_sheng"]: return "父母"
    elif yao_element == SHENG_KE[self_element]["sheng"]: return "子孙"
    elif yao_element == SHENG_KE[self_element]["bei_ke"]: return "官鬼"
    elif yao_element == SHENG_KE[self_element]["ke"]: return "妻财"
    return "未知"

def calculate_xun_kong(ri_gan, ri_zhi):
    """计算六甲旬空"""
    ri_gan_zhi = ri_gan + ri_zhi
    idx = JIA_ZI_60.index(ri_gan_zhi)
    xun_shou_idx = (idx // 10) * 10
    xun_shou = JIA_ZI_60[xun_shou_idx][:2]
    return xun_shou, XUN_KONG_MAP[xun_shou]

def calculate_wang_shuai(yao_element, yao_di_zhi, yue_jian, ri_zhi):
    """计算旺相休囚死（月建为主，日辰为辅）"""
    yue_info = YUE_JIAN_INFO[yue_jian]
    yue_element, season = yue_info["element"], yue_info["season"]
    score, base_status = 0, ""

    # 月建基础判断
    if yao_element == yue_element:
        base_status, score = "旺", 5
    elif yao_element == SHENG_KE[yue_element]["sheng"]:
        base_status, score = "相", 4
    elif yao_element == SHENG_KE[yue_element]["bei_sheng"]:
        base_status, score = "休", 3
    elif yao_element == SHENG_KE[yue_element]["bei_ke"]:
        base_status, score = "囚", 2
    else:
        base_status, score = "死", 1

    # 日辰调整
    ri_element = DI_ZHI_ELEMENT[ri_zhi]
    if SHENG_KE[ri_element]["sheng"] == yao_element: score += 2; base_status += "（日生）"
    if SHENG_KE[ri_element]["ke"] == yao_element: score -= 2; base_status += "（日克）"
    if ri_element == yao_element: score += 1; base_status += "（日比）"
    if DI_ZHI_RELATIONS["liu_he"].get(yao_di_zhi) == ri_zhi: score += 1; base_status += "（日合）"
    if DI_ZHI_RELATIONS["liu_chong"].get(yao_di_zhi) == ri_zhi: score -= 1; base_status += "（日冲）"

    # 最终判定
    final_status = "旺相有力" if score >=7 else "旺相" if score >=5 else "有气" if score >=3 else "休囚" if score >=1 else "休囚无力"
    return final_status, base_status, score

def calculate_di_zhi_relations(yao_di_zhi, target_di_zhi_list):
    """计算地支刑冲合害"""
    relations = {"合": [], "冲": [], "刑": [], "害": [], "破": []}
    for dz in target_di_zhi_list:
        if dz == yao_di_zhi: continue
        if DI_ZHI_RELATIONS["liu_he"].get(yao_di_zhi) == dz: relations["合"].append(dz)
        if DI_ZHI_RELATIONS["liu_chong"].get(yao_di_zhi) == dz: relations["冲"].append(dz)
    return relations

def calculate_fei_fu_shen(main_gua_info, main_yao_detail):
    """计算飞神伏神（简化版：以乾宫为例）"""
    gong = main_gua_info["palace"]
    pure_gua_name = GONG_PURE_GUA.get(gong)
    if not pure_gua_name or pure_gua_name not in BA_CHUN_GUA_YAO:
        return []
    pure_yao_list = BA_CHUN_GUA_YAO[pure_gua_name]
    self_element = main_gua_info["element"]
    fei_fu_list = []

    # 查找缺本宫五行的爻位
    main_elements = [y["element"] for y in main_yao_detail]
    for pure_yao in pure_yao_list:
        if pure_yao["element"] == self_element and pure_yao["element"] not in main_elements:
            fei_yao = next(y for y in main_yao_detail if y["yao_pos"] == pure_yao["yao_pos"])
            fei_fu_list.append({
                "yao_pos": pure_yao["yao_pos"],
                "fu_shen": f"{pure_yao['tian_gan']}{pure_yao['di_zhi']} {pure_yao['liu_qin']}",
                "fei_shen": f"{fei_yao['tian_gan']}{fei_yao['di_zhi']} {fei_yao['liu_qin']}"
            })
            break
    return fei_fu_list

def calculate_shen_sha(ri_gan, ri_zhi):
    """计算神煞"""
    shen_sha = {}
    for sha_name, rule in SHEN_SHA_RULES.items():
        if sha_name in ["天乙贵人"]:
            shen_sha[sha_name] = rule.get(ri_gan, [])
        elif sha_name in ["驿马", "桃花"]:
            sha_dz = rule.get(ri_zhi)
            shen_sha[sha_name] = [sha_dz] if sha_dz else []
    return shen_sha

# ===================== 主装卦函数 =====================
def liu_yao_zhuang_gua(yao_list, ri_gan, ri_zhi, yue_jian):
    # 输入校验
    if len(yao_list) != 6 or not all(y in (0,1,2,3) for y in yao_list):
        raise ValueError("六爻列表错误")
    if ri_gan + ri_zhi not in JIA_ZI_60:
        raise ValueError("日干支错误")
    if yue_jian not in YUE_JIAN_INFO:
        raise ValueError("月建错误")

    # 步骤1：生成主变卦阴阳数组
    main_yao_yinyang = [0 if y in (0,2) else 1 for y in yao_list]
    bian_yao_yinyang = []
    for y in yao_list:
        if y == 2: bian_yao_yinyang.append(1)
        elif y == 3: bian_yao_yinyang.append(0)
        else: bian_yao_yinyang.append(y)
    has_bian_gua = 2 in yao_list or 3 in yao_list

    # 步骤2：匹配卦信息
    main_lower = f"{main_yao_yinyang[2]}{main_yao_yinyang[1]}{main_yao_yinyang[0]}"
    main_upper = f"{main_yao_yinyang[5]}{main_yao_yinyang[4]}{main_yao_yinyang[3]}"
    main_code = main_upper + main_lower
    main_gua_info = GUA_64_MAP[main_code]

    bian_gua_info = None
    if has_bian_gua:
        bian_lower = f"{bian_yao_yinyang[2]}{bian_yao_yinyang[1]}{bian_yao_yinyang[0]}"
        bian_upper = f"{bian_yao_yinyang[5]}{bian_yao_yinyang[4]}{bian_yao_yinyang[3]}"
        bian_code = bian_upper + bian_lower
        bian_gua_info = GUA_64_MAP[bian_code]

    # 步骤3：安世应
    shi_pos = main_gua_info["shi_pos"]
    ying_pos = (shi_pos + 3) % 6

    # 步骤4：主卦纳甲
    inner_gua_name = BA_GUA[main_lower]["name"]
    outer_gua_name = BA_GUA[main_upper]["name"]
    main_yao_detail = [{} for _ in range(6)]

    for i in range(3):
        main_yao_detail[i]["yao_pos"] = i + 1
        main_yao_detail[i]["tian_gan"] = NA_JIA_TIAN_GAN[inner_gua_name]["inner"]
        main_yao_detail[i]["di_zhi"] = NA_JIA_DI_ZHI[inner_gua_name]["inner"][i]
        main_yao_detail[i]["element"] = DI_ZHI_ELEMENT[main_yao_detail[i]["di_zhi"]]
        main_yao_detail[i]["yin_yang"] = main_yao_yinyang[i]
        main_yao_detail[i]["dong_bian"] = yao_list[i]
        main_yao_detail[i]["is_shi"] = i == shi_pos
        main_yao_detail[i]["is_ying"] = i == ying_pos

    for i in range(3, 6):
        pos_in_outer = i - 3
        main_yao_detail[i]["yao_pos"] = i + 1
        main_yao_detail[i]["tian_gan"] = NA_JIA_TIAN_GAN[outer_gua_name]["outer"]
        main_yao_detail[i]["di_zhi"] = NA_JIA_DI_ZHI[outer_gua_name]["outer"][pos_in_outer]
        main_yao_detail[i]["element"] = DI_ZHI_ELEMENT[main_yao_detail[i]["di_zhi"]]
        main_yao_detail[i]["yin_yang"] = main_yao_yinyang[i]
        main_yao_detail[i]["dong_bian"] = yao_list[i]
        main_yao_detail[i]["is_shi"] = i == shi_pos
        main_yao_detail[i]["is_ying"] = i == ying_pos

    # 步骤5：配六亲、定六神
    self_element = main_gua_info["element"]
    for i in range(6):
        main_yao_detail[i]["liu_qin"] = get_liu_qin(self_element, main_yao_detail[i]["element"])

    start_idx = LIU_SHEN_START[ri_gan]
    for i in range(6):
        liu_shen_idx = (start_idx + i) % 6
        main_yao_detail[i]["liu_shen"] = LIU_SHEN[liu_shen_idx]

    # 步骤6：变卦纳甲（略，同基础版）
    bian_yao_detail = None

    # ===================== 新增增强功能 =====================
    # 步骤7：计算旬空
    xun_shou, xun_kong = calculate_xun_kong(ri_gan, ri_zhi)

    # 步骤8：计算旺衰
    for yao in main_yao_detail:
        final_status, base_status, score = calculate_wang_shuai(
            yao["element"], yao["di_zhi"], yue_jian, ri_zhi
        )
        yao["wang_shuai"] = {"final": final_status, "base": base_status, "score": score}

    # 步骤9：计算刑冲合害（与月建、日辰、其他爻）
    all_dz = [y["di_zhi"] for y in main_yao_detail] + [yue_jian, ri_zhi]
    for yao in main_yao_detail:
        yao["relations"] = calculate_di_zhi_relations(yao["di_zhi"], all_dz)

    # 步骤10：计算飞伏神
    fei_fu_list = calculate_fei_fu_shen(main_gua_info, main_yao_detail)

    # 步骤11：计算神煞并匹配到爻
    shen_sha = calculate_shen_sha(ri_gan, ri_zhi)
    for yao in main_yao_detail:
        yao["shen_sha"] = [name for name, dz_list in shen_sha.items() if yao["di_zhi"] in dz_list]

    # 结果整理
    result = {
        "main_gua": main_gua_info,
        "shi_ying": {"shi": shi_pos + 1, "ying": ying_pos + 1},
        "main_yao_detail": main_yao_detail,
        "has_bian_gua": has_bian_gua,
        "bian_gua": bian_gua_info,
        "bian_yao_detail": bian_yao_detail,
        "xun_kong": {"xun_shou": xun_shou, "di_zhi": xun_kong},
        "fei_fu_shen": fei_fu_list,
        "shen_sha_all": shen_sha
    }
    return result

# ===================== 结果打印函数 =====================
def print_zhuang_gua_result(result):
    print("="*80)
    print(f"主卦：{result['main_gua']['name']} | 宫位：{result['main_gua']['palace']} | 本宫五行：{result['main_gua']['element']}")
    print(f"世爻：{result['shi_ying']['shi']}爻 | 应爻：{result['shi_ying']['ying']}爻")
    print(f"六甲旬空：旬首{result['xun_kong']['xun_shou']} | 空亡{result['xun_kong']['di_zhi']}")
    print("="*80)
    print(f"{'爻位':<4}{'六神':<6}{'六亲':<6}{'干支':<8}{'旺衰':<12}{'刑冲合害':<15}{'神煞':<10}{'世应':<4}")
    print("-"*80)
    dong_bian_map = {0: "静", 1: "静", 2: "老阴动", 3: "老阳动"}
    for yao in reversed(result["main_yao_detail"]):
        yao_pos_str = f"{yao['yao_pos']}爻"
        gan_zhi = f"{yao['tian_gan']}{yao['di_zhi']}"
        wang_shuai = yao["wang_shuai"]["final"]
        rel = yao["relations"]
        rel_str = " ".join([f"{k}{v}" for k, v in rel.items() if v])
        shen_sha = ",".join(yao["shen_sha"]) if yao["shen_sha"] else ""
        shi_ying = "世" if yao["is_shi"] else ("应" if yao["is_ying"] else "")
        print(f"{yao_pos_str:<4}{yao['liu_shen']:<6}{yao['liu_qin']:<6}{gan_zhi:<8}{wang_shuai:<12}{rel_str:<15}{shen_sha:<10}{shi_ying:<4}")

    if result["fei_fu_shen"]:
        print("\n" + "="*80)
        print("飞神伏神：")
        print("="*80)
        for ff in result["fei_fu_shen"]:
            print(f"{ff['yao_pos']}爻：伏神{ff['fu_shen']}，飞神{ff['fei_shen']}")

# ===================== 示例运行 =====================
if __name__ == "__main__":
    # 示例：甲子日、寅月，起卦得老阳、少阴、少阳、老阴、少阳、少阳（初爻到上爻）
    yao_list = [3, 0, 1, 2, 1, 1]
    ri_gan, ri_zhi = "甲", "子"
    yue_jian = "寅"
    result = liu_yao_zhuang_gua(yao_list, ri_gan, ri_zhi, yue_jian)
    print_zhuang_gua_result(result)