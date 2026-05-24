"""Domain profiles for low-AIGC humanized thesis rewriting.

Profiles are intentionally separate from the older strategy classes.  A strategy
decides rewrite mechanics; a domain profile describes what counts as authentic
material in a discipline and what style should be preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DomainProfile:
    name: str
    label: str
    aliases: tuple[str, ...] = ()
    material_anchors: dict[str, tuple[str, ...]] = field(default_factory=dict)
    style_guidance: tuple[str, ...] = ()
    natural_phrases: tuple[str, ...] = ()
    avoid_phrases: tuple[str, ...] = ()
    classifier_keywords: tuple[str, ...] = ()

    @property
    def prompt_summary(self) -> str:
        anchors = "、".join(self.material_anchors.keys())
        guidance = "；".join(self.style_guidance)
        return f"{self.label}: 保留/增强材料锚点({anchors})。{guidance}"


DOMAIN_PROFILES: dict[str, DomainProfile] = {
    "computer_engineering": DomainProfile(
        name="computer_engineering",
        label="计算机/软件工程/信息系统",
        aliases=("computer", "software_engineering", "information_system", "cs", "se"),
        material_anchors={
            "源码": ("源码", "代码", "class", "def ", "函数", "类名"),
            "页面": ("页面", "界面", "表单", "按钮", "用户操作路径"),
            "接口": ("接口", "API", "请求", "返回", "输入输出"),
            "字段": ("字段", "status", "user_id", "id", "状态字段"),
            "数据库表": ("数据库", "数据表", "表结构", "集合", "MySQL", "MongoDB"),
            "配置文件": ("配置文件", "application.yml", "settings.py", "pom.xml"),
            "运行环境": ("运行环境", "部署", "服务器", "本地运行"),
            "测试用例": ("测试用例", "测试步骤", "错误提示", "实际测试"),
            "截图说明": ("截图", "图示", "页面截图"),
        },
        style_guidance=(
            "像学生基于项目实现过程整理出的说明",
            "少写宏大意义，多写实现、流程、字段、测试",
            "可保留适度工程解释感",
        ),
        natural_phrases=("源码中", "实际测试时", "当前版本", "这里"),
        avoid_phrases=("具有重要意义", "提供有力支撑", "形成闭环"),
        classifier_keywords=(
            "Spring Boot", "Vue", "Django", "Flask", "MySQL", "接口", "数据库",
            "系统实现", "系统测试", "字段", "页面", "源码", "小程序", "软件工程",
        ),
    ),
    "management": DomainProfile(
        name="management",
        label="管理/工商管理/人力资源",
        aliases=("business_administration", "human_resource", "hr", "business", "management"),
        material_anchors={
            "公司": ("公司", "企业", "案例企业", "A公司", "某企业"),
            "案例背景": ("案例背景", "企业概况", "行业背景"),
            "部门": ("部门", "门店", "事业部"),
            "岗位": ("岗位", "员工", "负责人", "招聘专员"),
            "制度": ("制度", "绩效", "薪酬", "考核", "培训"),
            "流程": ("流程", "招聘流程", "审批流程", "业务流程"),
            "访谈": ("访谈", "员工反馈", "访谈记录"),
            "问卷": ("问卷", "调查", "量表"),
            "表格数据": ("表", "数据", "统计", "比例"),
            "年份": ("2020", "2021", "2022", "2023", "2024", "2025", "年度"),
            "经营指标": ("营业额", "成本", "利润", "离职率", "满意度", "转化率"),
            "组织结构": ("组织结构", "层级", "汇报关系"),
        },
        style_guidance=(
            "像学生基于企业案例和管理问题做分析",
            "对策要对应企业实际问题",
            "避免加强重视、完善制度、提升水平这类空话单独成句",
        ),
        natural_phrases=("在该企业中", "访谈中", "实际执行时"),
        avoid_phrases=("加强重视", "完善机制", "提升水平", "构建体系"),
        classifier_keywords=(
            "工商管理", "人力资源", "绩效", "薪酬", "招聘", "企业", "岗位",
            "访谈", "问卷", "组织结构", "市场营销", "财务管理",
        ),
    ),
    "education": DomainProfile(
        name="education",
        label="教育/教学",
        aliases=("pedagogy", "teaching"),
        material_anchors={
            "学校": ("学校", "小学", "中学", "高校", "幼儿园"),
            "班级": ("班级", "一班", "二班", "三班", "年级"),
            "学生": ("学生", "儿童", "学习者"),
            "课堂": ("课堂", "课上", "课堂上"),
            "教学活动": ("教学活动", "小组活动", "导入", "展示", "讨论"),
            "问卷": ("问卷", "调查"),
            "访谈": ("访谈", "教师反馈"),
            "课堂观察": ("课堂观察", "观察记录"),
            "作业": ("作业", "练习", "作品"),
            "教学评价": ("评价", "测评", "学习效果"),
        },
        style_guidance=(
            "像学生基于教学场景和学生表现进行分析",
            "少写抽象教育理念，多写课堂现象和教学过程",
        ),
        natural_phrases=("课堂上", "学生在完成任务时", "教师反馈中"),
        classifier_keywords=("教育", "教学", "课堂", "学生", "教师", "班级", "课程", "作业"),
    ),
    "literature": DomainProfile(
        name="literature",
        label="文学/汉语言",
        aliases=("chinese_language", "literature_language", "language"),
        material_anchors={
            "作品": ("《", "作品", "小说", "诗歌", "散文", "文本"),
            "人物": ("人物", "翠翠", "周朴园", "主人公", "形象"),
            "情节": ("情节", "叙事情节", "故事"),
            "叙事": ("叙事", "视角", "叙述"),
            "意象": ("意象", "象征", "隐喻"),
            "语言风格": ("语言风格", "修辞", "句式"),
            "文本片段": ("描写", "台词", "片段"),
            "时代背景": ("时代背景", "创作背景"),
            "作者": ("作者", "创作特征"),
        },
        style_guidance=(
            "像基于具体文本细读写出的分析",
            "避免空泛评价，多写文本证据和细节分析",
        ),
        natural_phrases=("这一处描写", "从情节看", "文本中"),
        avoid_phrases=("展现人性光辉", "具有深刻意义"),
        classifier_keywords=("文学", "小说", "人物", "情节", "叙事", "意象", "语言风格", "汉语言"),
    ),
    "law": DomainProfile(
        name="law",
        label="法学/法律",
        aliases=("legal", "law_governance"),
        material_anchors={
            "法条": ("法条", "民法典", "刑法", "公司法", "司法解释"),
            "案例": ("案例", "该案", "本案", "案情", "裁判文书"),
            "案例事实": ("事实", "合同履行", "侵权行为"),
            "争议焦点": ("争议焦点", "争议集中", "焦点"),
            "裁判结果": ("裁判结果", "判决", "裁定"),
            "权利义务关系": ("权利", "义务", "请求权"),
            "适用条件": ("适用条件", "构成要件", "适用"),
            "责任承担": ("责任承担", "赔偿责任", "法律责任"),
        },
        style_guidance=(
            "像围绕案例和规范适用展开的论证",
            "强调事实—规范—结论的对应关系",
        ),
        natural_phrases=("在该案中", "争议集中在", "从规范适用看"),
        avoid_phrases=("法治意义重大", "具有重要法治价值"),
        classifier_keywords=("法学", "法律", "法条", "案例", "民法典", "刑法", "争议焦点", "司法解释"),
    ),
    "economics": DomainProfile(
        name="economics",
        label="经济/金融",
        aliases=("finance", "economy"),
        material_anchors={
            "指标": ("指标", "资产负债率", "收益率", "增长率", "GDP", "CPI"),
            "年份": ("2019", "2020", "2021", "2022", "2023", "2024", "年份"),
            "样本": ("样本", "样本企业", "观测值"),
            "变量": ("变量", "解释变量", "被解释变量"),
            "模型": ("模型", "回归", "面板", "VAR"),
            "统计结果": ("统计结果", "回归结果", "显著", "系数"),
            "政策背景": ("政策", "政策背景"),
            "行业数据": ("行业数据", "行业", "市场规模"),
            "图表": ("图", "表", "趋势图"),
            "趋势": ("趋势", "上升", "下降", "波动"),
            "影响因素": ("影响因素", "原因", "约束"),
        },
        style_guidance=(
            "像围绕数据和经济现象展开分析",
            "少写泛泛的促进经济发展，多写指标变化和原因解释",
        ),
        natural_phrases=("从数据看", "这一阶段", "指标变化显示"),
        classifier_keywords=("经济", "金融", "指标", "样本", "变量", "回归", "政策", "趋势", "融资"),
    ),
    "medicine": DomainProfile(
        name="medicine",
        label="医学/护理",
        aliases=("nursing", "medical_nursing", "clinical"),
        material_anchors={
            "病例": ("病例", "患者", "病人"),
            "样本": ("样本", "纳入", "排除"),
            "护理流程": ("护理", "护理流程", "护理措施"),
            "观察指标": ("观察指标", "评分", "量表"),
            "干预措施": ("干预", "干预措施"),
            "临床表现": ("临床表现", "症状", "体征"),
            "伦理说明": ("伦理", "知情同意"),
            "量表": ("量表", "评分表"),
            "随访": ("随访", "复查"),
            "并发症": ("并发症", "不良反应"),
            "治疗或护理结果": ("治疗结果", "护理结果", "预后"),
        },
        style_guidance=(
            "保守、准确、规范",
            "不伪造临床数据，不夸大疗效",
            "强调观察记录、护理过程、风险控制",
        ),
        natural_phrases=("护理过程中", "观察记录显示", "风险控制上"),
        classifier_keywords=("医学", "护理", "临床", "患者", "病例", "干预", "观察指标", "量表"),
    ),
    "art_design": DomainProfile(
        name="art_design",
        label="艺术设计",
        aliases=("design", "visual_design"),
        material_anchors={
            "设计主题": ("设计主题", "主题"),
            "用户群体": ("用户群体", "受众", "目标用户"),
            "构图": ("构图", "版式", "布局"),
            "色彩": ("色彩", "配色", "颜色"),
            "材料": ("材料", "材质"),
            "工艺": ("工艺", "制作"),
            "草图": ("草图", "手稿"),
            "方案迭代": ("迭代", "调整", "两轮", "修改"),
            "视觉元素": ("视觉元素", "图形", "字体"),
            "交互体验": ("交互", "体验"),
            "作品展示": ("展示", "作品"),
            "方案": ("方案", "设计方案"),
        },
        style_guidance=(
            "像围绕设计过程和作品表达写出的说明",
            "少写空泛审美价值，多写设计选择的依据和调整过程",
        ),
        natural_phrases=("方案调整时", "视觉上", "设计过程中"),
        classifier_keywords=("设计", "构图", "色彩", "材料", "草图", "视觉", "交互", "作品"),
    ),
    "engineering_general": DomainProfile(
        name="engineering_general",
        label="通用工科/机械/电气/土木",
        aliases=("mechanical", "electrical", "civil", "engineering"),
        material_anchors={
            "参数": ("参数", "尺寸", "荷载", "功率", "电压"),
            "设备": ("设备", "仪器", "装置"),
            "结构": ("结构", "构件", "节点"),
            "工况": ("工况", "载荷", "环境条件"),
            "图纸": ("图纸", "CAD", "示意图"),
            "计算过程": ("计算", "公式", "校核"),
            "实验步骤": ("实验步骤", "试验过程"),
            "测试结果": ("测试结果", "测量结果"),
            "材料": ("材料", "钢材", "混凝土"),
            "误差": ("误差", "偏差"),
            "规范标准": ("规范", "标准", "GB", "JGJ"),
        },
        style_guidance=(
            "像基于设计、实验或工程计算写出的说明",
            "少写宏观意义，多写参数和验证过程",
        ),
        natural_phrases=("计算过程中", "测试时", "从工况看"),
        classifier_keywords=("机械", "电气", "土木", "参数", "设备", "结构", "工况", "图纸", "规范"),
    ),
    "marxism": DomainProfile(
        name="marxism",
        label="马克思主义/思政/公共管理",
        aliases=("ideological_political", "public_administration", "public_management"),
        material_anchors={
            "政策文本": ("政策文本", "政策", "文件", "条例"),
            "地方实践": ("地方实践", "地区", "社区", "基层"),
            "基层案例": ("基层案例", "案例", "治理场景"),
            "历史阶段": ("历史阶段", "阶段"),
            "理论来源": ("理论来源", "马克思主义", "理论"),
            "现实问题": ("现实问题", "问题"),
            "制度安排": ("制度安排", "制度"),
            "治理场景": ("治理场景", "公共服务", "基层治理"),
        },
        style_guidance=(
            "保持必要政治表述规范",
            "避免全篇套话，多结合具体政策、地区、实践对象和现实问题",
        ),
        natural_phrases=("在地方实践中", "从基层治理看", "政策文本中"),
        classifier_keywords=("马克思主义", "思政", "公共管理", "公共服务", "基层", "治理", "政策", "地方实践"),
    ),
    "universal": DomainProfile(
        name="universal",
        label="通用",
        aliases=("auto", "other", "universal_light"),
        material_anchors={
            "研究对象": ("研究对象", "对象", "案例", "材料"),
            "过程": ("过程", "步骤", "环节"),
            "限制": ("限制", "不足", "局限"),
            "原文材料": ("原文", "材料", "依据"),
        },
        style_guidance=(
            "降低模板化和可预测性",
            "保留毕业论文基本规范",
            "材料不足时只提示需要材料，不凭空补细节",
        ),
        classifier_keywords=("研究对象", "案例", "材料", "过程"),
    ),
}


def list_domain_profiles() -> list[DomainProfile]:
    """Return all canonical profiles except aliases."""
    return list(DOMAIN_PROFILES.values())


def get_domain_profile(domain: str | None) -> DomainProfile:
    """Resolve a domain name or alias to a profile."""
    if not domain:
        return DOMAIN_PROFILES["universal"]

    key = domain.strip().lower()
    if key in DOMAIN_PROFILES:
        if key == "auto":
            return DOMAIN_PROFILES["universal"]
        return DOMAIN_PROFILES[key]

    for profile in DOMAIN_PROFILES.values():
        if key in {alias.lower() for alias in profile.aliases}:
            return profile
        if key == profile.label.lower():
            return profile

    return DOMAIN_PROFILES["universal"]


def classify_domain(
    title: str = "",
    abstract: str = "",
    keywords: str = "",
    headings: list[str] | None = None,
    declared_major: str = "",
) -> tuple[DomainProfile, list[str]]:
    """Classify a thesis into a domain profile using simple keyword scoring.

    User-declared major is still treated as evidence, not as an override here;
    callers that need hard user priority should pass the explicit --domain value
    through get_domain_profile before calling this classifier.
    """
    combined = " ".join([
        declared_major or "",
        title or "",
        abstract or "",
        keywords or "",
        " ".join(headings or []),
    ]).lower()

    scores: dict[str, float] = {}
    evidence: dict[str, list[str]] = {}
    for name, profile in DOMAIN_PROFILES.items():
        if name == "universal":
            continue
        score = 0.0
        hits: list[str] = []
        for kw in profile.classifier_keywords:
            if kw.lower() in combined:
                score += max(1.0, len(kw) / 3)
                hits.append(kw)
        for alias in profile.aliases:
            if alias and alias.lower() in combined:
                score += 1.5
                hits.append(alias)
        scores[name] = score
        evidence[name] = hits

    best_name = max(scores, key=scores.get, default="universal")
    best_score = scores.get(best_name, 0.0)
    if best_score <= 0:
        return DOMAIN_PROFILES["universal"], []

    sorted_scores = sorted(scores.values(), reverse=True)
    if len(sorted_scores) > 1 and sorted_scores[0] - sorted_scores[1] < 1.0:
        return DOMAIN_PROFILES["universal"], evidence.get(best_name, [])

    return DOMAIN_PROFILES[best_name], evidence.get(best_name, [])
