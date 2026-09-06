# 🇩🇪 job-search-de — 通用型全行业德国求职自动化与证据链评估流水线

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` 是一款专为 AI Agent（Antigravity、Claude Code、Cursor、OpenClaw、Gemini CLI 等）设计的**通用型、候选人中立**全行业德国求职自动化 Skill。全面支持**全栈技术研发、数据与 AI、市场营销 (Marketing)、商务销售 (Sales/BD)、财务审计 (Finance)、人力资源 (HR)、供应链与运营 (Operations)、UI/UX 设计以及商业咨询**等所有职业领域。

---

## 为什么选择 job-search-de

| 核心维度 | 传统招聘网站 / 中介聚合器 (LinkedIn / StepStone) | `job-search-de` 流水线 |
|---|---|---|
| **时效与真实度** | 30%~50% 是过期无效岗位、中介引流帖或幽灵职位 | **100% 真实有效**（直接请求企业官方 ATS API + Schema.org 毫秒级在线校验） |
| **数据隐私安全** | 简历与个人背景被上传至第三方云端数据库 | **100% 本地私密**（数据严格保存在本地 `<workdir>/.job-search/`，绝不上云） |
| **匹配打分可信度** | 粗暴的关键词匹配，虚高误报频繁 | **两阶段严谨证据链打分**（必须引用简历中的真实事实证据，杜绝幻觉打分） |
| **求职进度追踪** | 手动维护零散的 Excel 表格，繁琐易丢 | **开箱即用 4 主题工作台**（Kanban 看板、多维筛选、全键盘流、一键生成开场白） |
| **Agent 原生整合** | 无法融入现代 AI 辅助工作流 | **原生 Agent Skill 协议**（完美支持 Antigravity、Claude Code、Cursor、OpenClaw） |

---

## 界面演示

### 4 套设计主题即时切换（0 Token 纯 CSS 驱动）
> 支持在 **Editorial Craft（纸境文稿）**、**Dark Velocity（暗夜极客）**、**Industrial Precision（精密工业）** 与 **Spatial Quartz（空灵石英）** 之间无缝切换。支持按数字键 <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> 秒切，偏好自动持久化，零 Token 消耗。

![Workbench 4套主题切换演示](images/theme-switcher.gif)

---

### 1. 交互式数据表格视图
> 实时状态追踪、多维度组合筛选、职位新鲜度判定与量化契合度评分。

![工作台表格视图](images/workbench-table.png)

---

### 2. 申请全流程看板视图
> 拖拽与状态流转驱动的求职生命周期管理（待申请、已投递、面试中、已获 Offer、归档）。

![工作台看板视图](images/workbench-kanban.png)

---

### 3. 本地候选人档案与规则抽屉
> 隐私优先的候选人中立设计：个人经历、硬性限制、目标城市及交付配置严格保留在当前工作目录的 `.job-search/` 下，绝不上云。

![配置与档案抽屉](images/workbench-config-drawer.png)

---

### 4. 德国 AI 职位市场全景研报
> 覆盖法兰克福、慕尼黑、柏林、全德远程等多区域分布，包含岗位 JD 与候选人事实的深度证据链剖析。

![全景研报](images/report-overview.png)

---

## 核心特性

- **隐私优先架构**：Skill 核心逻辑与候选人数据严格分离。个人背景事实、求职偏好与搜索设置仅保存在本地工作目录的 `<workdir>/.job-search/` 中，绝不上云。
- **4 套内置设计主题**：支持在 **Editorial Craft（纸境文稿）**、**Dark Velocity（暗夜极客）**、**Industrial Precision（精密工业）** 与 **Spatial Quartz（空灵石英）** 之间即时切换，零 Token 消耗且自动持久化。
- **全键盘高能导航**：提供快捷键帮助中心（<kbd>?</kbd>），支持快速浏览（<kbd>J</kbd>/<kbd>K</kbd>）、展开详情（<kbd>Enter</kbd>）、直达官网（<kbd>O</kbd>）、聚焦搜索（<kbd>/</kbd>）及数字键秒切主题（<kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd>）。
- **一键定制投递 Pitch 话术**：基于匹配的事实证据链，一键生成地道精准的求职信开场白并自动复制到剪贴板。
- **快捷筛选预设胶囊**：提供 `Fit ≥ 85`、`法兰克福/莱美`、`纯远程`、`纯英语`、`待投递岗位` 等高频一键筛选。
- **直连企业官方 ATS 招聘源**：直接从 Greenhouse、Lever、Ashby、SmartRecruiters、Personio、Workable 抓取在招职位，告别过期二手聚合中介信息。
- **自动化多层真实验证**：实时 URL 连通性校验、HTTP 状态检测及 Schema.org JSON-LD 结构化数据解析（`datePosted`、`validThrough`、在招状态）。
- **两阶段严谨证据打分**：
  - **Stage 1 (初筛过滤)**：严格执行硬性约束排除、职级匹配与阈值修剪。
  - **Stage 2 (深度证据匹配)**：区分必要项与加分项，严格要求逐条引用简历证据，杜绝幻觉打分。
- **轻量前端交互工作台**：纯前端 HTML/JS 现代应用，支持看板视图、表格视图、字段筛选及 Notion 数据库双向状态同步。
- **运行时自动版本检测**：后台静默检测 GitHub 上游更新并在工作台展示版本徽章，支持单指令一键更新。

---

## 工作流流水线

```text
         候选人材料 (简历 / LinkedIn / 作品集 / 证书)
                            │
                            ▼
              [1. 导入与候选人画像构建]
                            │ (生成 .job-search/profile.md 与 preferences.md)
                            ▼
                [2. 多渠道岗位搜索发现]
             ATS 直连拉取 + 目标城市补充搜索
                            │
                            ▼
              [3. 职位清洗、归一化与真实验证]
             Schema.org JSON-LD + HTTP 状态检测
                            │
                            ▼
              [4. 两阶段事实证据链量化打分]
           硬性排除初筛 ➔ 候选人事实证据逐条比对
                            │
                            ▼
              [5. 决策研报生成与工作台交付]
     深度市场分析报告 + 交互式 HTML 工作台 + Notion 双向同步
```

---

## 系统架构

> 🌐 **在线交互式架构全景图**：[**`architecture.html`**](architecture.html)（基于 [Archify](https://github.com/tt-a1i/archify) Showcase 标准构建，支持明暗主题秒切、数据链路高亮追踪、导览章节切换、全屏演示与高清矢量导出）。

![job-search-de 系统架构](images/architecture.png)

`job-search-de` 采用**严格解耦、隐私沙箱优先的五层流水线架构**：

1. **本地私有沙箱层 (`.job-search/`)**：候选人中立设计。简历、领英导出的背景材料完全在本地解析为 `.job-search/profile.md`（事实库）、`preferences.md`（求职偏好与排除约束）与 `settings.ini`（阈值配置）。个人敏感信息绝不上云，保障欧洲高规格隐私合规。
2. **多渠道官方 ATS 职位发现引擎**：通过 `download.sh` 与 `parse_ats.py` 直连主流企业部署的公开 ATS 官方 API（Greenhouse, Ashby, Lever, SmartRecruiters, Personio, Workable），彻底过滤过期、死链与中介爬虫噪音。
3. **结构化元数据验证管道**：实时检测 HTTP 连通性，深度解析 Schema.org JSON-LD 结构化招聘元数据（`datePosted`, `validThrough`, 招聘状态），严格划分职位时效梯队（`VERIFIED_FRESH`、`LIKELY_FRESH`、`OLDER_ACTIVE`、`CLOSED`）。
4. **两阶段严格实证评分内核**：隔离不可信外部 JD 内容，建立防提示词注入边界。执行 Stage 1 快速硬约束门槛初筛，并于 Stage 2 进行逐条事实比对——**每一项匹配要求必须援引 `profile.md` 中的客观证据**，坚决杜绝大模型臆测与虚假匹配建议。
5. **全周期交互式交付工作台**：生成分区域多语言决策研报，支持双向同步 Notion 职位数据库，并交付纯前端交互式单页应用（[`job-hunt-workbench.html`](../job-hunt-workbench.html)）——内置 4 套纯 CSS 质感主题、看板/表格双重视图，支持通过浏览器 File System Access API 原生免上传直接编辑保存本地配置。

---

## 项目目录结构

```text
job-search-de/
├── SKILL.md                  # Agent Skill 入口与行为规范
├── README.md                 # 主项目英文文档 (English)
├── VERSION                   # 语义化版本号声明 (例如 1.1.1)
├── assets/
│   └── config-template/      # 候选人私有配置模板
│       ├── profile.md        # 候选人已验证技能与履历事实模板
│       ├── preferences.md    # 目标职能、城市偏好、语言硬性约束
│       └── settings.ini      # 搜索时间窗口、打分阈值与交付语言
├── configs/
│   ├── boards.txt            # 默认直连 ATS 监控企业列表
│   ├── keywords.txt          # 默认搜索关键词矩阵
│   └── profile.md            # 参考画像规范
├── references/
│   ├── configuration.md      # 配置文件规范与约束
│   ├── onboarding.md         # 候选人入驻与档案生成指南
│   ├── resume-parser.md      # 简历事实证据提取标准
│   ├── scoring.md            # 两阶段证据链打分细则
│   └── workbench.md          # 工作台设计系统与多主题规范
├── scripts/
│   ├── bump_version.py       # 语义化版本自动递增脚本（解耦路径）
│   ├── check_update.py       # 在线/离线上游版本检测脚本
│   ├── update_skill.sh       # 一键 Skill 自动更新脚本
│   ├── download.sh           # ATS API 批量下载脚本（含并发限流池）
│   ├── parse_ats.py          # 全行业通用 ATS 数据解析与归一化
│   ├── verify_urls.py        # Schema.org JSON-LD 结构化提取引擎
│   ├── verify.sh             # 职位链接与时效性验证 CLI
│   ├── build_workbench.py    # 工作台 HTML 生成与配置注入工具
│   ├── test_ats_universal.py # 全量回归与正确性验证测试套件
│   ├── init_config.py        # 本地 .job-search/ 模板初始化
│   ├── build_html.sh         # 工作台打包脚本
│   └── fix_html.py           # HTML 研报排版与交互增强脚本
├── templates/
│   ├── agent_prompt_common.md# 规范化 Agent 提示词模块
│   ├── report_skeleton.md    # 决策分析研报骨架模板
│   └── search_queries.md     # 搜索 Query 组合矩阵
└── docs/
    ├── README_zh.md          # 中文使用文档 (当前文件)
    ├── README_de.md          # 德语使用文档 (Deutsch)
    ├── README_ja.md          # 日语使用文档 (日本語)
    ├── README_ko.md          # 韩语使用文档 (한국어)
    ├── architecture.html     # 交互式系统架构全景图 (Archify)
    ├── architecture.json     # 架构规格定义文件
    └── images/               # 演示截图、系统架构图与主题切换动态 GIF
```

---

## 快速上手

### 1. 一键安装 Skill
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 放置简历
在你的工作目录下放入个人简历或背景文件（如 `resume.pdf`、`CV.md` 或 LinkedIn 导出的资料）。

### 3. 对话 AI Agent 自动运行
向你的 AI 助手（Antigravity、Claude Code、Cursor、OpenClaw、Gemini CLI 等）发送指令：

> **“帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型算法岗位，并生成评估报告和求职工作台。”**

```text
> 用户: "帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型岗位。"

Agent 执行流程:
[1/4] 解析简历事实并构建本地 .job-search/profile.md（提炼 6 项核心能力与 4 项项目事实）
[2/4] 直连各大企业 ATS 招聘端点（Greenhouse, Lever, Ashby, Personio...）→ 抓取 42 个在招岗位
[3/4] 执行真实性与时效验证（解析 Schema.org JSON-LD，0 个过期岗位）
[4/4] 严谨匹配事实证据链并量化契合度：
      • 8 个极高契合度岗位（Fit ≥ 85）
      • 14 个中高契合度岗位（70 ≤ Fit < 85）
自动生成深度决策分析研报，并交付交互式 HTML 求职工作台 `job-hunt-workbench.html`！
```

<details>
<summary><b>开发者底层 CLI 脚本调用（可选）</b></summary>

如果你希望脱离 Agent 自行调用底层脚本：

```bash
# 初始化本地配置模版
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# 批量拉取 ATS 在招职位并清洗
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# 校验职位链接与新鲜度
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## 支持的快捷指令

在 AI 对话中可随时输入以下快捷指令：

| 指令 | 作用说明 |
|---|---|
| `/refresh` | **全量更新搜索**：重新拉取最新 ATS 接口、联网真实性验证、两阶段证据打分并更新工作台与研报。 |
| `/update-skill` | **自动更新 Skill**：静默拉取 GitHub 最新发布的版本代码。 |
| `/match <url / jd>` | **单职位即时评估**：输入单条职位链接或 JD 文本，对照档案证据链快速打分。 |
| `/tailor <id / url>` | **定制简历与求职信**：针对指定岗位生成证据对齐的定制简历要点与德式求职信 (Anschreiben)。 |
| `/sync` | **Notion 同步**：双向同步投递进度至本地或云端 Notion 职位看板数据库。 |
| `/digest` | **每日 60 秒精选**：提取近 24~48 小时新增的高契合度 TOP 5 岗位速报。 |

---

## Agent Skill 配置接入

本 Skill 严格遵循标准 Agent Skill 协议（支持 Antigravity, Claude Code, OpenClaw, Gemini CLI, Cursor 等）。

在配置文件中引入：

```json
{
  "skills": [
    "~/.agents/skills/job-search-de"
  ]
}
```

触发指令（如 *“寻找法兰克福匹配我背景的德国 AI 岗位”*）后，Agent 将严格按照 `SKILL.md` 全自动执行。

---

## 配置与隐私管理

所有属于候选人的个人背景与求职偏好，均仅保存在本地工作目录的 `.job-search/` 文件夹中：

<details>
<summary><b>查看配置示例 <code>.job-search/preferences.md</code> 与 <code>settings.ini</code></b></summary>

```markdown
# 求职偏好与限制 (.job-search/preferences.md)

- **目标职位:** Senior AI Engineer, Machine Learning Engineer, Applied AI Lead
- **目标区域:** 法兰克福及莱美大区, 德国全境 (Full Remote)
- **最低契合度分值:** 75
- **语言偏好:** 英语为主 (具备 B1/B2 基础德语)
```

```ini
# 搜索与交付配置 (.job-search/settings.ini)
[scoring]
fit_threshold = 75
require_direct_ats = true

[delivery]
workbench_language = zh
auto_open_browser = true
```
</details>

---

## 常见问题 (FAQ)

<details>
<summary><b>1. 我需要配置 LinkedIn 或各大招聘网站的付费 API 吗？</b></summary>

**完全不需要。** 本流水线直接请求企业公开部署的官方 ATS 招聘端点（Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable），既合法合规，又绕过了各类商业中介爬虫与付费限制。
</details>

<details>
<summary><b>2. 我的简历或个人隐私信息会被上传到外部服务器吗？</b></summary>

**绝对不会。** 简历解析、证据链比对、打分与工作台渲染 100% 在你的本地机器与当前 Agent 交互会话中完成，没有任何外部数据埋点或云端同步。
</details>

<details>
<summary><b>3. 我可以自定义目标城市、搜索关键词或排除条件吗？</b></summary>

**可以。** 只需修改本地 `.job-search/preferences.md` 或 `.job-search/settings.ini` 即可随意调整目标城市（如慕尼黑、柏林）、薪资期望或特定技术栈，无需修改任何代码。
</details>

---

## 开源许可证

本项目基于 [MIT License](LICENSE) 开源发布。
