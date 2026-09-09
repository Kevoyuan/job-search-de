# 🇩🇪 job-search-de: 通用型全行业德国求职自动化与证据链评估 Skill

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-1e5e3a.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/免配置%20API%20Key-Agent%20原生-emerald.svg?style=flat-square" alt="Zero API Key" />
  <img src="https://img.shields.io/badge/广泛兼容-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20OpenClaw-black.svg?style=flat-square" alt="Compatible Agents" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` 是一款专为各类现有 Coding Agent（如 Google Antigravity、Claude Code、Cursor、Codex、OpenClaw、Gemini CLI、Windsurf 等）设计的**通用型、候选人中立**全行业德国求职自动化 Skill。

> **核心定位：Agent 原生技能（Skill），非 API Key 脚本应用**  
> 区别于要求用户在 `.env` 中输入 `OPENAI_API_KEY` 或按 Token 付费的传统脚本应用，`job-search-de` 是一套标准的 **Agent-Native Skill**：
> - **零第三方 API Key 配置**：直接借用宿主 Coding Agent 现成的大模型推理、上下文理解与终端执行能力，用户无需申请任何外部 API Key。
> - **100% 本地隐私沙盒**：候选人个人简历、求职偏好与匹配打分结果完整驻留在本地 `<workdir>/.job-search/`，绝无外部云端数据上传。
> - **通用支持全行业领域**：涵盖软件工程、数据与 AI/ML、云计算/DevOps、产品管理、市场营销 (Marketing)、商务销售 (Sales/BD)、财务审计 (Finance)、人力资源 (HR)、运营供应链 (Operations)、UI/UX 设计及商业咨询。

---

## 为什么选择 job-search-de

| 核心维度 | 传统招聘网站 (LinkedIn / StepStone) | 传统需配 API Key 的 Python 爬虫脚本 | `job-search-de` Agent Skill |
|---|---|---|---|
| **配置与凭证** | 手动注册、频繁人机验证、推送广告 | 要求用户提供付费 `OPENAI_API_KEY` | **零 API Key 配置**：作为原生 Skill 直接挂载于现有 Coding Agent |
| **职位新鲜度** | 30%~50% 是过期无效岗位、中介帖或幽灵职位 | 依赖 HTML 解析，网页微调即崩溃 | **100% 真实有效**：直连官方 ATS 接口 + Schema.org 时间戳多层验证 |
| **数据隐私安全** | 简历上传至第三方商业云端数据库 | 个人材料常被转发至第三方模型接口 | **100% 本地私密沙盒**（严格保留在 `<workdir>/.job-search/`） |
| **匹配打分可信度** | 粗暴关键词匹配，虚高误报频繁 | 单提示词粗糙提炼，极易模型幻觉 | **两阶段严谨证据打分**：强制要求逐条引用简历客观事实 |
| **交付形态** | 充斥广告的商业网页 | 终端纯文本字符流或静态 CSV 表格 | **交互式 4 主题工作台**（Kanban、表格筛选、0 Token 纯 CSS 驱动） |
| **Agent 协作** | 无法融入现代开发者智能体工作流 | 孤立的命令行工具，与 Agent 上下文断连 | **原生智能体协议**（`SKILL.md`、`references/` 渐进式知识库） |

---

## Agent 执行流程与交互体验

当你将本技能引入 Coding Agent 后，只需以自然语言发起对话，Agent 即可自主激活并分步执行流水线：

```text
用户: "帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的机器学习工程师岗位。"
                                    │
                                    ▼
Agent (已自动激活 job-search-de skill):
 ├── [1/5] 解析简历事实库 ──────────► 提炼客观技能与经历至 .job-search/profile.md
 ├── [2/5] 官方 ATS 接口直连发现 ───► 并发请求 Greenhouse, Lever, Ashby, Personio
 ├── [3/5] 职位时效与真实度校验 ────► 解析 Schema.org JSON-LD 毫秒级时间戳（剔除幽灵岗位）
 ├── [4/5] 两阶段严谨证据链打分 ────► 每一项岗位要求均比对档案事实证据（杜绝幻觉虚高分）
 └── [5/5] 交付免 Token 交互工作台 ──► 自动化编译 4 套设计主题的 job-hunt-workbench.html
```

---

## 界面演示：交互式求职工作台（Agent 交付产物）

Agent 执行完成后，将生成并更新一份轻量、纯客户端离线运行的求职驾驶舱（`job-hunt-workbench.html`）：

### 4 套设计主题即时切换（0 Token 纯 CSS 驱动）
> 支持在 **Editorial Craft（纸境文稿）**、**Dark Velocity（暗夜极客）**、**Industrial Precision（精密工业）** 与 **Spatial Quartz（空灵石英）** 之间无缝切换。支持数字快捷键 <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> 秒切，系统配色实时同步，且全量支持减弱动效（`prefers-reduced-motion`）与减弱透明度（`prefers-reduced-transparency`）等无障碍规范。

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

### 4. 德国职位市场全景研报
> 覆盖法兰克福、慕尼黑、柏林、全德远程等多区域分布，包含岗位 JD 与候选人事实的深度证据链剖析。

![全景研报](images/report-overview.png)

---

## 核心特性

- **Agent 原生架构**：无缝挂载于现有 Coding Agent（Antigravity、Claude Code、Cursor、Codex、OpenClaw 等），无需配置任何第三方大模型 API Key。
- **隐私优先沙盒**：候选人背景材料、求职限制与个人设置完全保存在本地工作目录 `<workdir>/.job-search/` 中。
- **4 套防 AI 模版化主题**：全量通过 WCAG AA 级高对比度审查（Editorial Craft、Dark Velocity、Industrial Precision、Spatial Quartz），零 Token 开销且偏好自动持久化。
- **全面无障碍支持**：内置 `@media (prefers-reduced-motion: reduce)` 控制以抑制长周期动效，提供 `@media (prefers-reduced-transparency: reduce)` 高对比度不透明回退机制。
- **全键盘高能导航**：提供快捷键帮助面板（<kbd>?</kbd>），支持快速浏览（<kbd>J</kbd>/<kbd>K</kbd>）、展开详情（<kbd>Enter</kbd>）、直达官网（<kbd>O</kbd>）、聚焦搜索（<kbd>/</kbd>）及数字键秒切主题（<kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd>）。
- **一键定制投递 Pitch 话术**：基于匹配的事实证据链，一键生成地道精准的求职信开场白并自动复制到剪贴板。
- **直连企业官方 ATS 招聘源**：直接从企业部署的 Greenhouse、Lever、Ashby、SmartRecruiters、Personio、Workable 抓取有效在招职位，拒绝二手过期中介信息。
- **自动化多层真实验证**：实时 URL 连通性检测、HTTP 状态检测及 Schema.org JSON-LD 结构化数据解析（`datePosted`、`validThrough`、在招状态）。
- **两阶段严谨证据打分**：
  - **Stage 1 (初筛过滤)**：严格执行硬性约束排除、职级匹配与阈值修剪。
  - **Stage 2 (深度证据匹配)**：区分必要项与加分项，严格要求逐条引用简历证据，杜绝幻觉打分。
- **运行时自动版本检测**：后台静默检测 GitHub 上游更新并在工作台展示版本徽章，支持单指令一键升级。

---

## 系统架构

> 🌐 **在线交互式架构全景图**：[**`architecture.html`**](architecture.html)（基于 [Archify](https://github.com/tt-a1i/archify) Showcase 标准构建，支持明暗主题秒切、数据链路高亮追踪、导览章节切换、全屏演示与高清矢量导出）。

![job-search-de 系统架构](images/architecture.png)

---

## 快速上手

### 1. 将 Skill 挂载至你的 Agent
通过标准 skills 命令安装：
```bash
npx skills add Kevoyuan/job-search-de -g
```
或直接克隆至对应 Agent 的 skills 发现目录：
```bash
git clone https://github.com/Kevoyuan/job-search-de.git ~/.agents/skills/job-search-de
```

### 2. 放置简历背景文件
在当前工作目录放入你的个人简历或材料（如 `resume.pdf`、`CV.md` 或 LinkedIn 导出文件）。

### 3. 在 Coding Agent 中自然对话
直接向你的 AI 助手（Antigravity、Claude Code、Cursor、Codex、OpenClaw 等）发起提问：

> **“帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型算法岗位，并生成评估报告和求职工作台。”**

```text
> 用户: "帮我在德国（法兰克福、慕尼黑或全德远程）寻找匹配我简历的 AI / 大模型岗位。"

Agent:
[1/4] 解析简历事实并构建本地 .job-search/profile.md（提炼 6 项核心能力与 4 项项目事实）
[2/4] 直连各大企业 ATS 招聘端点（Greenhouse, Lever, Ashby, Personio...）-> 抓取 42 个在招岗位
[3/4] 执行真实性与时效验证（解析 Schema.org JSON-LD，0 个过期岗位）
[4/4] 严谨匹配事实证据链并量化契合度：
      • 8 个高契合度岗位（Fit >= 85）
      • 14 个中高契合度岗位（70 <= Fit < 85）
已生成深度决策分析研报，并同步交付交互式 HTML 求职工作台 job-hunt-workbench.html！
```

---

## 适配的 Coding Agent 环境

本技能遵循开放智能体标准协议，已测试兼容：

- **Google Antigravity**：放入 `~/.agents/skills/` 或 `~/.gemini/antigravity/skills/` 即可全局调用。
- **Anthropic Claude Code**：支持通过 `npx skills add Kevoyuan/job-search-de -g` 安装，或在 `CLAUDE.md` 中引用。
- **Cursor**：在项目的 `.cursorrules` 或 Agent 会话上下文中配置技能路径。
- **Codex / Gemini CLI**：支持标准 skill 目录挂载。
- **OpenClaw / Windsurf**：支持全局技能发现体系。

---

## 支持的快捷指令

在与 Agent 对话时可随时输入以下快捷指令：

| 指令 | 作用说明 |
|---|---|
| `/refresh` | **全量更新搜索**：重新拉取最新 ATS 接口、联网真实性验证、两阶段证据打分并更新工作台与研报。 |
| `/update-skill` | **自动更新 Skill**：检测并拉取 GitHub 最新版本代码。 |
| `/match <url / jd>` | **单职位即时评估**：输入单条职位链接或 JD 文本，对照档案证据链快速打分。 |
| `/tailor <id / url>` | **定制简历与求职信**：针对指定岗位生成证据对齐的定制简历要点与德式求职信 (Anschreiben)。 |
| `/sync` | **Notion 同步**：双向同步投递进度至本地或云端 Notion 职位看板数据库。 |
| `/digest` | **每日 60 秒精选**：提取近 24-48 小时新增的高契合度 TOP 5 岗位速报。 |

---

## 配置与本地隐私

所有属于候选人的个人背景与求职偏好，均仅保存在当前工作目录的 `.job-search/` 文件夹中：

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
<summary><b>1. 我需要准备 OpenAI、Claude 或其他大模型的 API Key 吗？</b></summary>

**完全不需要。** 这是一款标准的 Agent Skill，而非 API 调用脚本。你当前使用的 Coding Agent（如 Antigravity、Claude Code、Cursor 等）自身已具备完整的推理与理解能力，本项目只是作为技能扩展包为其提供德国求职的领域知识、ATS 脚本与交付模板，你无需申请任何额外的 API Key。
</details>

<details>
<summary><b>2. 我需要配置 LinkedIn 或各大招聘网站的付费 API 吗？</b></summary>

**不需要。** 本技能直接请求企业公开部署的官方 ATS 招聘端点（Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable），既合法合规，又绕过了商业中介爬虫与付费限制。
</details>

<details>
<summary><b>3. 我的简历或个人隐私信息会被上传到外部服务器吗？</b></summary>

**绝对不会。** 简历解析、证据链比对、打分与工作台渲染 100% 在你的本地机器与当前 Agent 交互会话中完成，没有任何外部数据埋点或云端同步。
</details>

<details>
<summary><b>4. 我可以自定义目标城市、搜索关键词或排除条件吗？</b></summary>

**可以。** 只需修改本地 `.job-search/preferences.md` 或 `.job-search/settings.ini` 即可随意调整目标城市（如慕尼黑、柏林）、薪资期望或特定技术栈，无需修改任何代码。
</details>

---

## 开源许可证

本项目基于 [MIT License](LICENSE) 开源发布。
