# 🇩🇪 job-search-de — ドイツ全職種対応 求人自動探索＆エビデンス評価パイプライン

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

`job-search-de` は、AI Agent（Antigravity、Claude Code、Cursor、OpenClaw 等）向けに設計された**完全汎用・候補者中立**のドイツ求人自動化スキルです。エンジニアリングだけでなく、**マーケティング、セールス、財務会計、人事、オペレーション、デザイン、コンサルティング**等、あらゆる職種に対応しています。

---

## なぜ job-search-de なのか

| 比較項目 | 従来の求人サイト (LinkedIn / StepStone / Indeed) | `job-search-de` パイプライン |
|---|---|---|
| **求人の鮮度と信頼性** | 30%〜50%が掲載終了、幽霊求人、または仲介業者の転載 | **100% リアルタイム検証済み** (公式ATS API直取得 + Schema.org 検証) |
| **プライバシーとデータ保護** | 履歴書データが外部クラウドDBに送信・蓄積される | **100% ローカル完結** (データはローカルの `<workdir>/.job-search/` のみに保持) |
| **マッチング精度** | 単純なキーワード検索による誤検出が多発 | **2段階エビデンススコアリング** (職務経歴の具体的事実のみを引用、ハルシネーション排除) |
| **選考・応募管理** | Excelやスプレッドシートの手動更新で煩雑 | **4テーマ対応ワークベンチ** (カンバン、高度フィルター、キーボード操作、Pitch生成) |
| **AIエージェント連携** | 最新のAI自動化ワークフローと連携不可 | **Agent Skill ネイティブ対応** (Antigravity, Claude Code, Cursor, OpenClaw) |

---

## デモとUIインターフェース

### 4つのデザインテーマ切り替え（0トークン・純CSS）
> **Notion Craft（温かみのあるドキュメント風）**、**Linear Obsidian（ダークモード）**、**Bauhaus Grid（バウハウス工業風）**、**Bento Quartz（空間ガラス風）** の4テーマを瞬時に切り替え可能。キーボードの <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> で即時切り替え。

![Workbench テーマ切り替えデモ](images/theme-switcher.gif)

---

### 1. インタラクティブ・テーブルデータベースビュー
> リアルタイムの選考ステータス追跡、多次元フィルター、掲載鮮度インジケーター、高精度スコア表示。

![Workbench テーブルビュー](images/workbench-table.png)

---

### 2. 選考パイプライン・カンバンビュー
> ドラッグ＆ドロップおよびステータス管理（応募待ち、応募済み、面接中、オファー獲得、アーカイブ）。

![Workbench カンバンビュー](images/workbench-kanban.png)

---

### 3. ローカル候補者プロファイル＆ルール設定ドロワー
> プライバシー優先設計：個人情報や希望条件はすべてローカルの `.job-search/` にのみ安全に保存。

![Workbench 設定ドロワー](images/workbench-config-drawer.png)

---

### 4. 総合市場分析レポート
> フランクフルト、ミュンヘン、ベルリン、ドイツ全域リモート等、地域別の深層求人マッチング分析。

![市場分析レポート](images/report-overview.png)

---

## 主な機能と特徴

- **プライバシー優先＆候補者データ分離**：Skillのロジックと候補者データを完全分離。個人情報や条件設定はローカルの `<workdir>/.job-search/` にのみ保存。
- **4つの洗練されたテーマ切り替え**：**Notion Craft**、**Linear Obsidian (ダークモード)**、**Bauhaus Grid**、**Bento Quartz** を0トークンで瞬時に切り替え可能。
- **キーボード・パワーナビゲーション**：<kbd>J</kbd>/<kbd>K</kbd> で移動、<kbd>Enter</kbd> で展開、<kbd>O</kbd> で求人ページ直行、<kbd>/</kbd> で検索、<kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd> でテーマ変更。
- **ワンクリック求人マッチングPitch生成**：検証済みのJDエビデンスに基づき、洗練されたカバーレターの冒頭文を即時クリップボードにコピー。
- **クイックプリセット検索チップ**：`Fit ≥ 85`、`フランクフルト地域`、`フルリモート`、`英語必須`、`応募待ち求人` を1タップで抽出。
- **ATS公式API直接取得**：Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable等の公式エンドポイントから最新求人を直取得。
- **自動リアルタイム検証パイプライン**：URL生存確認、HTTPステータス、Schema.org JSON-LDメタデータを自動解析。
- **2段階のエビデンスベース・スコアリング**：
  - **Stage 1 (高速スクリーニング)**：必須要件不適合やシニアリティの即時除外。
  - **Stage 2 (詳細JDマッチング)**：候補者の実際のスキル根拠を引用し、ハルシネーション（嘘の評価）を完全排除。
- **インタラクティブ・ワークベンチ**：カンバンボード、テーブル表示、Notion双方向同期に対応した軽量HTML/JS UI。
- **実行時バージョンチェック＆自動更新**：GitHub上の最新リリースを自動検出し、ステータスバッジ（`v1.1.1`）を表示。

---

### パイプラインワークフロー

```text
               候補者資料 (履歴書 / LinkedIn / ポートフォリオ)
                                      │
                                      ▼
                      [1. オンボーディング＆設定初期化]
                                      │ (.job-search/profile.md と preferences.md 生成)
                                      ▼
                        [2. マルチチャネルATS探索]
                     公式ATS直接取得 + 対象都市補完検索
                                      │
                                      ▼
                      [3. 構造化クレンジング＆実時間検証]
                    Schema.org JSON-LD + HTTPステータスチェック
                                      │
                                      ▼
                      [4. 2段階エビデンスマッチング評価]
                    必須条件除外 ➔ 履歴書エビデンス事実照合
                                      │
                                      ▼
                      [5. 意思決定レポート＆UIワークベンチ]
              市場分析レポート + インタラクティブHTMLワークベンチ
```

---

## システムアーキテクチャ

> 🌐 **インタラクティブ・アーキテクチャ図**: [**`architecture.html`**](architecture.html)（[Archify](https://github.com/tt-a1i/archify) Showcase仕様準拠。ライト/ダークテーマ切替、接続経路ハイライト追跡、章立てガイド、全画面プレゼン、ベクター書き出しに対応）。

![job-search-de システムアーキテクチャ](images/architecture.png)

`job-search-de` は**完全分離型・プライバシー保護優先の5層パイプライン設計**を採用しています：

1. **ローカル機密サンドボックス (`.job-search/`)**: 候補者中立設計。個人情報はすべてローカルの `.job-search/profile.md`、`preferences.md`、`settings.ini` に保存され、外部クラウドやSkillリポジトリには一切送信されません。
2. **公式ATSマルチチャネル探索エンジン**: Greenhouse、Ashby、Lever、SmartRecruiters、Personio、Workableなどの公式ATSエンドポイントに直接アクセスし、期限切れや人材紹介会社の転載ノイズを完全排除。
3. **構造化検証＆正規化パイプライン**: HTTP疎通確認とSchema.org JSON-LDメタデータ（`datePosted`、`validThrough`、募集ステータス）をリアルタイム解析し、鮮度を厳密に判定。
4. **2段階厳格エビデンススコアリング核**: 未信頼な外部JDからのプロンプトインジェクションを遮断。第1段階の必須条件フィルタと、第2段階の事実照合（`profile.md` の検証済みエビデンス引用必須、AIのハルシネーションを完全排除）を実行。
5. **マルチ視覚ワークベンチ＆レポート交付**: 分割地域別の詳細レポート、Notionデータベース双向同期、および4つの独自CSSテーマ（Notion、Linear、Bauhaus、Bento）を備えた単一HTMLワークベンチ（File System Access APIによる直接保存対応）を提供。

---

## ディレクトリ構成

```text
job-search-de/
├── SKILL.md                  # Agent Skill エントリポイントと動作規約
├── README.md                 # メインドキュメント (英語)
├── VERSION                   # セマンティックバージョン定義 (例: 1.1.1)
├── assets/
│   └── config-template/      # 設定テンプレート
│       ├── profile.md        # 検証済みスキル・経歴テンプレート
│       ├── preferences.md    # 検索条件・ターゲット指定
│       └── settings.ini      # スコア閾値・検索対象期間
├── configs/
│   ├── boards.txt            # 監視対象ATS企業リスト
│   ├── keywords.txt          # 検索キーワードマトリクス
│   └── profile.md            # 参考プロファイル定義
├── references/
│   ├── configuration.md      # 設定仕様書
│   ├── onboarding.md         # オンボーディングガイド
│   ├── resume-parser.md      # 履歴書エビデンス抽出仕様
│   ├── scoring.md            # 2段階エビデンススコアリング基準
│   └── workbench.md          # ワークベンチ仕様・テーマ規約
├── scripts/
│   ├── bump_version.py       # バージョン自動更新スクリプト
│   ├── check_update.py       # アップストリーム更新チェック
│   ├── update_skill.sh       # ワンクリックSkill更新スクリプト
│   ├── download.sh           # ATS API一括ダウンロード
│   ├── parse_ats.py          # ATSデータパーサー＆正規化
│   ├── verify_urls.py        # Schema.org JSON-LD メタデータ抽出
│   ├── verify.sh             # 求人URL＆メタデータ検証
│   ├── build_workbench.py    # ワークベンチHTMLビルダー
│   ├── test_ats_universal.py # ATSパーサー回帰テストスイート
│   ├── init_config.py        # ローカル設定初期化
│   ├── build_html.sh         # ワークベンチビルドスクリプト
│   └── fix_html.py           # HTMLレポートデータ注入
├── templates/
│   ├── agent_prompt_common.md# 標準プロンプトブロック
│   ├── report_skeleton.md    # 経営レポートスケルトン
│   └── search_queries.md     # 検索クエリ合成マトリクス
└── docs/
    ├── README_zh.md          # 中国語ドキュメント (中文)
    ├── README_de.md          # ドイツ語ドキュメント (Deutsch)
    ├── README_ja.md          # 日本語ドキュメント (このファイル)
    ├── README_ko.md          # 韓国語ドキュメント (한국어)
    ├── architecture.html     # インタラクティブシステムアーキテクチャ図 (Archify)
    ├── architecture.json     # アーキテクチャ定義仕様
    └── images/               # デモ画像・アーキテクチャ図・アニメーションGIF
```

---

## クイックスタート

### 1. Skillをインストール
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 履歴書をワークスペースに配置
作業フォルダに履歴書ファイル（`resume.pdf`、`CV.md` 等）を置きます。

### 3. AIエージェントに指示
AIアシスタント（Antigravity、Claude Code、Cursor、OpenClaw）に話しかけるだけです：

> **「私の履歴書に合う、フランクフルト、ミュンヘン、またはドイツ国内フルリモートのAIエンジニア求人を探してください。」**

---

## サポートされているコマンド

| コマンド | 説明 |
|---|---|
| `/refresh` | **全体検索更新**: ATS求人の再取得、リンク検証、スコアリングを実行し、ワークベンチを更新。 |
| `/update-skill` | **Skill自動更新**: GitHub上の最新コードを取得。 |
| `/match <url / jd>` | **単一求人評価**: 指定した求人票とプロファイルを即時照合。 |
| `/tailor <id / url>` | **履歴書・カバーレター生成**: エビデンスに基づきドイツ式応募書類を生成。 |
| `/sync` | **Notion同期**: Notionデータベースと選考進捗を双方向同期。 |
| `/digest` | **デイリーダイジェスト**: 直近24〜48時間以内の高マッチ求人TOP5を抽出。 |

---

## 設定とプライバシー管理

個人データと希望条件は、すべてローカルの `.job-search/` にのみ安全に保存されます：

<details>
<summary><b>設定例 <code>.job-search/preferences.md</code> および <code>settings.ini</code></b></summary>

```markdown
# ターゲット希望条件 (.job-search/preferences.md)

- **ターゲット職種:** Senior AI Engineer, Machine Learning Engineer
- **対象地域:** フランクフルト, ドイツ全域 (フルリモート)
- **最低適合度スコア:** 75
- **語学:** 英語流暢 (ドイツ語基礎)
```

```ini
# 検索・評価設定 (.job-search/settings.ini)
[scoring]
fit_threshold = 75
require_direct_ats = true

[delivery]
workbench_language = ja
auto_open_browser = true
```
</details>

---

## よくある質問 (FAQ)

<details>
<summary><b>1. 有料のLinkedIn APIやスクレイピングキーは必要ですか？</b></summary>

**不要です。** 採用企業が公式に使用している公開ATSエンドポイント（Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable）から直接取得します。
</details>

<details>
<summary><b>2. 履歴書や個人情報が外部サーバーに送信されることはありますか？</b></summary>

**一切ありません。** 解析やスコアリング、ワークベンチの生成はすべてローカル環境のエージェントセッション内で行われます。
</details>

<details>
<summary><b>3. 対象都市や希望キーワードはカスタマイズできますか？</b></summary>

**可能です。** ローカルの `.job-search/preferences.md` や `.job-search/settings.ini` を編集するだけで自由に調整できます。
</details>

---

## ライセンス

[MIT License](LICENSE) のもとで公開されています。
