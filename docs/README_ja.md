# 🇩🇪 job-search-de — ドイツAI・テック求人 自動探索＆エビデンス評価パイプライン

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-対応済み-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/ターゲット-ドイツ%20AI%2FTech-emerald.svg?style=flat-square" alt="Target Market" />
  <img src="https://img.shields.io/badge/スコアリング-根拠重視-purple.svg?style=flat-square" alt="Scoring Mode" />
  <img src="https://img.shields.io/badge/ライセンス-MIT-green.svg?style=flat-square" alt="License" />
</p>

ドイツ国内のAI・テクノロジー分野の求人情報を対象に、自動収集・検証・2段階エビデンス評価・レポート生成・ワークベンチ管理を行うAIエージェント向けスキルです。

---

## 📸 デモ＆インターフェース

### 1. Notionスタイルのインタラクティブ求人ワークベンチ（テーブル表示）
> リアルタイムの選考ステータス追跡、多角的な条件絞り込み、求人鮮度判定、精密な適合度スコア。

![ワークベンチ テーブル表示](images/workbench-table.png)

---

### 2. 選考プロセス管理カンバン
> ドラッグ＆ドロップやステータス変更に対応した応募進捗管理（応募予定、応募済み、面接中、内定、アーカイブ）。

![ワークベンチ カンバン表示](images/workbench-kanban.png)

---

### 3. ローカル候補者プロフィール＆設定ドロワー
> 候補者中立・プライバシー重視設計：経歴、必須条件、希望勤務地、レポート設定はローカルの `.job-search/` フォルダ内に安全に保持されます。

![設定ドロワー](images/workbench-config-drawer.png)

---

### 4. ドイツ市場インテリジェンス分析レポート
> フランクフルト、ミュンヘン、ベルリン、ドイツ全国フルリモートなどの地域別求人動向と、JD（募集要項）と候補者経歴のエビデンスマッチング詳細。

![分析レポート](images/report-overview.png)

---

## 🌟 主な特徴

- 🎯 **プライバシーファースト＆候補者中立設計**: スキル本体は候補者データから完全に分離。個人情報や希望条件はプロジェクトローカルの `<workdir>/.job-search/` にのみ保存されます。
- 🔍 **主要ATS直接連携**: Greenhouse、Lever、Ashby、SmartRecruiters、Personio、Workable などの公式採用APIから直接求人を取得し、古い集約サイトのノイズを排除。
- ⚡ **自動検証＆鮮度判定**: URLの疎通確認、HTTPステータス、Schema.org JSON-LD構造化データ（`datePosted`、`validThrough` 等）の自動パース。
- 📊 **2段階エビデンスマッチング**:
  - **Stage 1 (高速トリアージ)**: 必須除外条件や職位レベルによる高速スクリーニング。
  - **Stage 2 (深層マッチング)**: 必須要件と歓迎要件を明確に分類し、プロフィール内の客観的事実のみを根拠に適合度を算出。
- 🗂️ **Notion風Webワークベンチ**: テーブル表示、カンバンボード、条件フィルタ、Notionデータベースとの双方向連携を備えたモダンなUI。
- 📑 **多言語エグゼクティブレポート**: 地域別・スキル別に整理されたMarkdownおよびHTML形式の分析レポートを自動出力。

---

## 🔄 処理フロー

```text
          候補者資料 (履歴書 / LinkedIn / ポートフォリオ)
                            │
                            ▼
              [1. オンボーディング＆プロファイル生成]
                            │ (.job-search/profile.md & preferences.md を作成)
                            ▼
                [2. マルチチャネル求人探索]
              ATS直結取得 ＋ 地域別ギャップ補完検索
                            │
                            ▼
                [3. データ正規化＆有効性検証]
             Schema.org JSON-LD ＋ HTTP日時チェック
                            │
                            ▼
                [4. 2段階エビデンススコアリング]
             足切りフィルタ ➔ JDと経歴事実の照合
                            │
                            ▼
                [5. レポート生成＆同期配信]
        詳細レポート ＋ インタラクティブUI ＋ Notion連携
```

---

## 📁 ディレクトリ構成

```text
job-search-de/
├── SKILL.md                  # Agent Skill エントリポイントと動作規約
├── README.md                 # メインドキュメント (英語)
├── VERSION                   # セマンティックバージョン定義 (例: 1.1.0)
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
│   ├── bump_version.py       # Auto semantic version bumper
│   ├── check_update.py       # アップストリーム更新チェック
│   ├── update_skill.sh       # ワンクリックSkill更新スクリプト
│   ├── download.sh           # ATS API一括ダウンロード
│   ├── parse_ats.py          # ATSデータパーサー＆正規化
│   ├── verify.sh             # 求人URL＆メタデータ検証
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
    └── images/               # デモ画像・アニメーションGIF
```

---

## 🚀 クイックスタート（3ステップで完了）

### 1. スキルのインストール
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. 履歴書の配置
作業フォルダに職務経歴書や履歴書（`resume.pdf`、`CV.md`、LinkedInエクスポート等）を配置します。

### 3. AIエージェントに指示
AIアシスタント（Antigravity、Claude Code、Cursor等）に自然言語で話しかけるだけです：

> **「私の経歴書にマッチするドイツ（フランクフルト、ミュンヘン、またはフルリモート）のAI/ML求人を探して評価レポートとワークベンチを作成して。」**

AIエージェントが自動で全工程を実行します：
1. 📄 **プロファイル抽出**: 経歴を解析し、ローカルの `.job-search/profile.md` を作成。
2. 🔍 **リアルタイム探索**: Greenhouse、Lever、Ashby、Personio などから最新求人を直結取得。
3. ⚡ **有効性検証**: URLの疎通とSchema.org掲載日を自動確認。
4. 📊 **エビデンス評価**: 募集要項と経歴事実を厳密に照合して採点。
5. 🗂️ **レポート＆UI生成**: 分析レポートを作成し、インタラクティブWebワークベンチを更新。

<details>
<summary><b>🛠️ 手動CLIコマンド（上級者向け・任意）</b></summary>

スクリプトを直接実行したい場合：

```bash
# 設定テンプレートの初期化
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# 求人ダウンロードとパース
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# URLの検証
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## ⚡ 利用可能なコマンド（Commands）

AIエージェントとのチャットで直接実行できるコマンド：

| コマンド | 説明 |
|---|---|
| `/refresh` | **最新求人の全探索**：ATSからの最新取得、有効性検証、2段階エビデンス評価、ワークベンチ＆レポート更新を実行。 |
| `/update-skill` | **スキルの自動更新**：GitHubから最新リリースを取得し、`npx skills update job-search-de -g` を実行。 |
| `/match <URL または JD>` | **即時適合度判定**：指定した求人URLや募集要項テキストを経歴事実と即座に照合・採点。 |
| `/tailor <ID または URL>` | **職務経歴・カバーレター最適化**：募集ポジションに特化したアピールポイントとドイツ語のカバーレター（Anschreiben）を生成。 |
| `/sync` | **Notion同期**：ローカルのワークベンチとNotionデータベースの選考ステータスを双方向同期。 |
| `/digest` | **デイリーダイジェスト**：過去24〜48時間に新着した高適合度求人Top 5を簡潔に要約。 |

---

## ⚙️ プライバシー設定管理 (`.job-search/`)

候補者個人の情報や検索条件は、すべてローカルの `.job-search/` にのみ保存されます：

<details>
<summary><b>📂 設定例 <code>.job-search/preferences.md</code> および <code>settings.ini</code></b></summary>

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

## ❓ よくある質問 (FAQ)

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

## 📄 ライセンス

[MIT License](LICENSE) のもとで公開されています。
