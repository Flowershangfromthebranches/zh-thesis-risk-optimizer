# zh-thesis-risk-optimizer v2.0

中文毕业论文 AIGC 风险降低与论文质量重构工具。

## 项目定位

**输入**：一篇高 AIGC 疑似率的毕业论文（.docx），可选 AIGC 检测报告。

**输出**：一篇低 AIGC 疑似率、高质量、保持原格式的论文。

**核心思路**：不是做同义替换或学术润色，而是通过**重构内容、补充细节、改变论证结构**来降低 AI 写作痕迹，提升论文的真实写作感。

## 不做什么

- ❌ 不承诺绕过任何检测系统
- ❌ 不伪造实验数据、访谈数据、参考文献或引用
- ❌ 不做同义替换式"降重"
- ❌ 不做学术润色（把论文改得更正式、更模板化）
- ❌ 不删除必要引用或把他人观点伪装成原创
- ❌ 不自动猜测专业后直接大规模改写

## 最终主流程（7 步）

```
Step 1: IntakeGate      → 检查必填信息（专业、题目、AIGC率、目标、权限）
Step 2: MajorRoute      → 用户声明专业 → 路由到对应策略（8 条路线）
Step 3: RiskPlan        → 计划 modify/rewrite/rebuild 比例
Step 4: PermissionGate  → 显示方案 → 用户确认（不允许重写？无报告？无材料？）
Step 5: EvidencePlan    → 确定材料优先级（原文 > 用户材料 > 联网 > 模型常识）
Step 6: ExecuteOptimize → 改写引擎 + 策略 + 守卫
Step 7: OutcomeReport   → 诚实评估（成功/失败/部分成功/无法验证）
```

**关键原则**：
- 信息不完整 → 返回缺失项，**不执行优化**
- 用户声明专业最高优先级，系统**不自动猜测后直接改写**
- 所有改写必须先生成方案 → 用户确认 → 再执行
- 严禁伪造数据、文献、实验、问卷或案例

## 快速开始

```bash
# 安装
pip install -e .

# 基本用法
thesis-optimize optimize --input thesis.docx

# 带 AIGC 报告
thesis-optimize optimize \
  --input thesis.docx \
  --aigc-report report.docx \
  --aigc-rate 65.93

# 指定专业（用户声明最高优先级）
thesis-optimize optimize \
  --input thesis.docx \
  --major human_resource

# 只分析,不写入
thesis-optimize optimize --input thesis.docx --dry-run --debug

# 自定义输出
thesis-optimize optimize \
  --input thesis.docx \
  --output thesis_optimized.docx \
  --report thesis_optimization_report.md
```

也可以通过 Python 调用：

```python
python -m thesis_risk_optimizer optimize --input thesis.docx
```

## 专业路线（8 条）

| 路线 | 策略 | 适用专业 | 核心思路 |
|------|------|---------|---------|
| `computer_engineering` | `computer` | 计算机/软件工程/Web/AI | 多写系统实现、模块输入输出、开发环境、测试参数 |
| `human_resource` | `human_resource` | 人力资源管理/招聘/绩效/薪酬 | 不套模板、不编数据、锚定企业/制度/岗位/调查 |
| `business_management` | `management` | 工商管理/财务/市场/物流 | 多写企业场景、具体问题、数据流程、对策落地 |
| `education` | `education` | 教育学/学前/教学设计 | 多写课堂观察、学生表现、教师行为、访谈 |
| `literature_language` | `literature` | 文学/语言/新闻传播 | 多写文本细读、人物分析、保留个人判断 |
| `law_governance` | `law` | 法学/法律事务 | 多写法条适用、案例情境、争议焦点 |
| `medical_nursing` | `medicine` | 护理/临床/药学/公卫 | 多写护理流程、观察指标、操作规范（不伪造数据） |
| `universal_light` | `universal` | 其他专业（默认） | 减少模板句、增加具体细节（不适用于高 AIGC 大规模改写） |

## 材料优先级

改写时使用证据的优先级（从高到低）：

1. **论文原文已有信息**（最高优先级）
2. **用户提供的真实材料**（参考文献、问卷数据、访谈记录等）
3. **论文参考文献中已有的资料**
4. **用户补充的项目/案例/源码/截图**
5. **公开资料联网搜索**（如允许，需记录来源）
6. **模型常识保守表达**（最低优先级，不编造具体数据）

## AIGC 风险等级与处理比例

| AIGC 疑似率 | 修改 | 重写 | 重构 |
|------------|------|------|------|
| < 30% | 80% | 20% | 0% |
| 30%-50% | 50% | 40% | 10% |
| 50%-70% | 25% | 55% | 20% |
| ≥ 70% | 10% | 50% | 40% |

## DOCX 格式保持

- 使用 python-docx + lxml (OOXML) 处理
- 只修改正文文本节点，不重建整个文档
- 保留：标题层级、加粗、字体、字号、表格结构、图片、段落顺序
- 默认不修改：封面、原创性声明、目录、参考文献、公式、图表编号、身份信息

## 输出

每次处理生成两个文件：
1. `原名_optimized.docx` — 优化后的论文
2. `原名_optimization_report.md` — 处理报告

处理报告包含：专业分类、策略模式、处理比例、高风险段落数、重点处理章节、字数变化、反AI文风守卫状态、仍可能高风险的原因、建议补充材料。

## 项目结构

```
src/thesis_risk_optimizer/
├── __init__.py             # 包定义 (v2.0)
├── cli.py                  # CLI 入口
├── intake/                 # Step 1: 必填信息检查
│   ├── intake_gate.py      # IntakeGate
│   ├── required_fields.py  # 必填字段定义
│   └── confirmation.py     # PermissionGate
├── routing/                # Step 2: 专业路由
│   └── major_router.py     # MajorRouter (8 条路线)
├── planning/               # Step 3: 风险规划
│   ├── risk_planner.py     # RiskPlanner
│   └── plan_summary.py     # PlanSummary 生成器
├── evidence/               # Step 5: 材料优先级
│   └── evidence_plan.py    # EvidencePlan + 伪造禁令
├── document_io/            # DOCX 读写 + 文本单元模型
├── report_parser/          # AIGC 报告解析
├── analysis/               # 专业分类、风险估计、段落诊断
├── strategies/             # 8 种专业策略
├── rewrite/                # 修改/重写/重构引擎 + 反AI文风守卫
├── validation/             # 结构/格式/长度校验 + OutcomeReport
└── prompts/                # LLM 提示词模板
```

## 注意事项

1. 本项目不承诺检测平台结果，不保证达到某个具体百分比
2. 高 AIGC 论文优先重写和重构，反复小修通常无效
3. 修改不会删除大段正文，推荐输出字数为原文的 90%-115%
4. 医学/护理策略有极高安全要求——绝对不伪造临床数据和病例
5. 法学策略不伪造法条和案例
6. 如果需要外部资料才能改写的内容，会标注需要用户提供
7. 有 LLM 接入时效果更好，无 LLM 时使用规则引擎做基础修改
8. 用户声明的专业优先级最高，系统不会自动覆盖

## License

MIT
