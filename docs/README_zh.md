# 🇩🇪 job-search-de — 德国 AI / 科技求职自动化发现与证据链评估 Skill

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/目标市场-德国%20AI%2FTech-emerald.svg?style=flat-square" alt="Target Market" />
  <img src="https://img.shields.io/badge/评分模式-证据链匹配-purple.svg?style=flat-square" alt="Scoring Mode" />
  <img src="https://img.shields.io/badge/开源协议-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` 是一款专为 AI Agent（Antigravity、Claude Code、OpenClaw、Gemini CLI 等）设计的候选人中立型德国科技/AI求职全流程自动化 Skill。涵盖**全网/ATS 职位发现、真实性验证、两阶段证据链评分、多语言分析研报生成与 Notion 风格交互式工作台同步**。

---

## 📸 界面与 Demo 演示

### 1. 交互式 Notion 风格求职工作台（表格视图）
> 实时状态追踪、多维度组合筛选、职位新鲜度判定与量化契合度评分。

![工作台表格视图](images/workbench-table.png)

---

### 2. 申请全流程看板（Kanban 视图）
> 拖拽与状态流转驱动的求职生命周期管理（待申请、已投递、面试中、已获 Offer、归档）。

![工作台看板视图](images/workbench-kanban.png)

---

### 3. 本地候选人档案与规则抽屉
> 隐私优先的候选人中立设计：个人经历、硬性限制、目标城市及交付配置严格保留在当前工作目录的 `.job-search/` 下，绝不污染全局 Skill。

![配置与档案抽屉](images/workbench-config-drawer.png)

---

### 4. 德国 AI 职位市场全景研报
> 覆盖法兰克福、慕尼黑、柏林、全德远程等多区域分布，包含岗位 JD 与候选人事实的深度证据链剖析。

![全景研报](images/report-overview.png)

---

## 🌟 核心特性

- 🎯 **隐私保护与候选人中立架构**：Skill 核心逻辑与候选人数据解耦，个人画像与搜索限制存放于项目本地的 `<workdir>/.job-search/`。
- 🔍 **直连主流 ATS 招聘源**：直接拉取 Greenhouse、Lever、Ashby、SmartRecruiters、Personio、Workable 实时岗位接口，杜绝过时中介网站脏数据。
- ⚡ **自动化校验与新鲜度机制**：支持实时 URL 连通性测试、HTTP 状态码检测及 Schema.org JSON-LD 结构化数据解析（`datePosted`、`validThrough` 等）。
- 📊 **两阶段严谨证据链评分**：
  - **Stage 1 (快速初筛)**：按硬性排除项、资历职级及预设门槛快速过滤。
  - **Stage 2 (JD 深度事实匹配)**：严格区分必要条件与加分项，评分必须引用候选人档案中的真实证据，杜绝幻觉匹配。
- 🗂️ **Notion 风格现代化前端工作台**：纯纯前端现代 HTML/JS 构建，支持表格、看板、快捷筛选预设，并支持与 Notion 职位数据库双向状态同步。
- 📑 **多语言智能研报生成**：自动生成结构化 Markdown 与交互式 HTML 报告，精准覆盖目标城市与技术栈。

---

## 🔄 全流程架构图

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
                [3. 数据标准化与真实性验证]
             Schema.org JSON-LD + HTTP 存活校验
                            │
                            ▼
                [4. 两阶段量化证据链评分]
          初筛过滤 ➔ JD 要求与候选人事实逐项对照
                            │
                            ▼
                [5. 研报生成与工作台同步]
       决策研报 + 交互式 HTML 工作台 + Notion 状态同步
```

---

## 📁 目录结构

```text
job-search-de/
├── SKILL.md                  # Agent Skill 入口与行为规范
├── README.md                 # 主项目英文文档 (English)
├── VERSION                   # 语义化版本号声明 (例如 1.1.0)
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
│   ├── bump_version.py       # Auto semantic version bumper
│   ├── check_update.py       # 在线/离线上游版本检测脚本
│   ├── update_skill.sh       # 一键 Skill 自动更新脚本
│   ├── download.sh           # ATS API 批量下载脚本
│   ├── parse_ats.py          # ATS 数据解析与归一化
│   ├── verify.sh             # 职位链接与时效性验证
│   ├── init_config.py        # 本地 .job-search/ 模板初始化
│   ├── build_html.sh         # 工作台打包脚本
│   └── fix_html.py           # HTML 研报数据注入脚本
├── templates/
│   ├── agent_prompt_common.md# 规范化 Agent 提示词模块
│   ├── report_skeleton.md    # 决策分析研报骨架模板
│   └── search_queries.md     # 搜索 Query 组合矩阵
└── docs/
    ├── README_zh.md          # 中文使用文档 (当前文件)
    ├── README_de.md          # 德语使用文档 (Deutsch)
    ├── README_ja.md          # 日语使用文档 (日本語)
    ├── README_ko.md          # 韩语使用文档 (한국어)
    └── images/               # 演示截图与主题切换动态 GIF
```

---

## 🚀 极简快速上手（3 步零配置）

### 1. 一键安装 Skill
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 放置简历
在你的工作目录下放入个人简历或背景文件（如 `resume.pdf`、`CV.md` 或 LinkedIn 导出的资料）。

### 3. 直接对话 AI Agent
向你的 AI 助手（Antigravity、Claude Code、Cursor、OpenClaw、Gemini CLI 等）发送指令：

> **“帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型算法岗位，并生成评估报告和求职工作台。”**

```text
> 👤 用户: "帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型岗位。"

🤖 Agent 执行全流程:
[1/4] 📄 解析简历事实并构建本地 .job-search/profile.md（提炼 6 项核心能力与 4 项项目事实）
[2/4] 🔍 直连各大企业 ATS 招聘端点（Greenhouse, Lever, Ashby, Personio...）→ 抓取 42 个在招岗位
[3/4] ⚡ 执行真实性与时效验证（解析 Schema.org JSON-LD，0 个过期岗位）
[4/4] 📊 严谨匹配事实证据链并量化契合度：
      • 8 个极高契合度岗位（Fit ≥ 85）
      • 14 个中高契合度岗位（70 ≤ Fit < 85）
✨ 自动生成深度决策分析研报，并交付交互式 HTML 求职工作台 `job-hunt-workbench.html`！
```

<details>
<summary><b>🛠️ 开发者底层 CLI 脚本调用（可选高级用法）</b></summary>

如果你希望脱离 Agent 自行调用底层脚本：

```bash
# 初始化本地配置模版
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# 批量拉取 ATS 在招职位并清洗
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# 校验链接真实性
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## ⚡ 常用快捷指令（Commands）

你可以在与 AI Agent 对话时直接输入以下指令：

| 指令 | 作用说明 |
|---|---|
| `/refresh` | **全流程刷新搜索**：执行最新 ATS 批量拉取、真实性校验、两阶段证据链打分，并同步更新工作台与研报。 |
| `/update-skill` | **一键自动升级 Skill**：从 GitHub 拉取最新版本并自动执行 `npx skills update job-search-de -g`。 |
| `/match <url 或 JD>` | **单职位即时打分**：输入任意职位链接或 JD 文本，快速进行证据链比对与契合度评估。 |
| `/tailor <职位ID 或 url>` | **定制简历与德语求职信**：基于你的真实经历严格生成针对该岗位的 CV 要点与德语 Anschreiben（动机信）。 |
| `/sync` | **Notion 状态双向同步**：将本地工作台与 Notion Job 数据库投递状态进行双向对齐同步。 |
| `/digest` | **每日 60 秒极速简报**：快速提炼过去 24–48 小时新发布的 Top 5 高契合度优质岗位。 |

---

## 🤖 AI Agent Skill 集成

本仓库完全兼容标准 Agent Skill 规范（包括 Antigravity、Claude Code、OpenClaw、Gemini CLI、Cursor 等）。

在你的 Skill 配置文件中加入：

```json
{
  "skills": [
    "~/.agents/skills/job-search-de"
  ]
}
```

配置完成后，Agent 接收到求职相关指令时即可自动加载 `SKILL.md` 并执行完整的发现-验证-打分-交付链路。

---

## 📄 开源许可

本项目采用 [MIT 许可证](LICENSE)。
