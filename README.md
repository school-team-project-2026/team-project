# TEAM PROJECT

学校のチーム制作プロジェクトです。

本アプリは、ユーザーが好きな趣味や作品について、
「なぜ好きなのか」という特徴をAIで分析し、
共通する魅力を持つ新しい趣味や作品を推薦するWebアプリケーションです。

単純なジャンルの一致だけでなく、魅力・価値観・体験などの
共通点を利用した異分野推薦を目指しています。

現在は開発中です。

## 技術スタック

| 分野 | 使用技術 |
| --- | --- |
| Frontend | Next.js / React / TypeScript / Tailwind CSS |
| Backend | Python 3.13 / FastAPI |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Database | PostgreSQL |
| LLM | Groq / openai/gpt-oss-120b |
| AI Structured Output | JSON Schema / Pydantic |
| Embedding | Sentence Transformers / multilingual-e5-small |
| Test | pytest |
| Lint / Format | Ruff |
| Infrastructure | Docker Compose |
| Package Management | uv / npm |

## 必要なツール

- Git
- Node.js 20.9以降
- npm
- uv
- Python 3.13
- Docker Desktop
- VS Code（推奨）

好きな理由をAIで解析する推薦機能を使用する場合は、
GroqのAPIキーが必要です。

通常の自動テストにはAPIキーは必要ありません。

## ディレクトリ構成

- `frontend/`：Next.jsフロントエンド
- `backend/`：FastAPIバックエンド
  - `app/`：アプリケーション本体
  - `alembic/`：DBマイグレーション
  - `tests/`：自動テスト
  - `scripts/`：データ登録・評価・検証
  - `benchmarks/`：AIモデルの比較評価
- `docs/`：仕様・議事録・手順
- `compose.yaml`：共通DB環境

## 環境変数

リポジトリのルートで、PostgreSQL用の環境変数ファイルを作成します。

```powershell
Copy-Item .env.example .env
```

`.env` の `POSTGRES_PASSWORD` は各自のローカル開発用
パスワードへ変更してください。

フロントエンド用の環境変数ファイルも作成します。

```powershell
Copy-Item frontend/.env.local.example frontend/.env.local
```

`NEXT_PUBLIC_API_BASE_URL` はブラウザから接続できる
バックエンドのURLです。

`NEXT_PUBLIC_` で始まる値はブラウザへ公開されるため、
秘密情報を設定しないでください。


### AI関連の環境変数

バックエンドはリポジトリのルートにある
`.env` ファイルから環境変数を読み込みます。

好きな理由をAIで分析する推薦機能を利用する場合は、
以下の設定をルートの `.env` に追加してください。

```dotenv
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=intfloat/multilingual-e5-small
```

`GROQ_MODEL` と `EMBEDDING_MODEL` は省略可能です。
省略時は上記のデフォルト値が使用されます。

GroqのAPIキーが必要なのは、好きな理由を指定した
推薦処理や、実Groq APIを使用するBenchmarkです。

好きな理由を指定しない推薦処理や、
通常の自動テストではGroqのAPIキーは不要です。

ただし、実際の推薦処理にはEmbeddingモデルと
PostgreSQLが必要です。

初回の推薦処理では、Embeddingモデルの取得・
読み込みに時間がかかる場合があります。

GeminiはAIモデルの比較評価用として設定できます。
通常の推薦APIでは使用しません。

APIキーやパスワードをGitへコミットしないでください。

## PostgreSQL

Docker Desktopを起動し、
リポジトリのルートで実行します。

### 起動

```powershell
docker compose up -d db
```

### 状態確認

```powershell
docker compose ps
```

### 停止

```powershell
docker compose down
```

データはDockerの名前付きボリューム `postgres-data`
に保存されます。

通常の `docker compose down` では削除されません。

`docker compose down -v` はDBデータを削除するため、
意図しない実行に注意してください。

## バックエンド

### セットアップ

リポジトリのルートから実行します。

```powershell
Set-Location backend
uv python install 3.13
uv sync
```

Python 3.13が既にインストールされている場合、
`uv python install 3.13` は省略できます。

### データベースの初期化

PostgreSQLを起動した状態で、
backendディレクトリから実行します。

```powershell
uv run alembic upgrade head
uv run python -m scripts.seed_candidates
```

Alembicで最新のテーブル構造を適用した後、
推薦用のCandidateデータを登録します。

### 既存環境のデータベース更新

mainブランチの更新などにより、
DB構造やCandidateデータが変更された場合は、
PostgreSQLを起動した状態で以下を実行してください。

```powershell
uv sync
uv run alembic upgrade head
uv run python -m scripts.seed_candidates
```

Negative Preference機能では、
Candidateの `interaction_modes` を使用します。

マイグレーションのみでは、
既存Candidateの活動種別が未設定のままとなる場合があります。

必ずマイグレーション後にSeedを実行してください。

Seedは定義済み候補を追加し、
既存候補については活動種別を補完・更新します。

通常の逐次実行では、同じSeedを再実行しても
同一候補が追加されない設計です。

### 起動

backendディレクトリから実行します。

```powershell
uv run uvicorn app.main:app --reload
```

APIは `http://localhost:8000` で起動します。

### ヘルスチェック

```powershell
Invoke-RestMethod http://localhost:8000/health
```

正常時は `{"status":"ok"}` が返ります。

Swagger UI：
`http://localhost:8000/docs`

OpenAPI：
`http://localhost:8000/openapi.json`

## 推薦API

### POST /recommendations

入力された趣味と好きな理由から、
関連する候補を検索・推薦します。

#### リクエスト例

```json
{
  "interest_text": "ジャズ",
  "liked_aspects": "楽器の掛け合いを聴くのが好きです。自分で演奏することには興味がありません。"
}
```

| フィールド | 必須 | 内容 |
| --- | --- | --- |
| interest_text | 必須 | 好きな趣味・作品など |
| liked_aspects | 任意 | 好きな理由・避けたい条件など |

`liked_aspects` が指定された場合は、
LLMによる特徴抽出を実行します。

省略した場合は、趣味名に基づく類似度検索を行います。

EmbeddingにはE5モデルを使用します。

初回の推薦処理では、
モデルの取得や読み込みに時間がかかる場合があります。

#### レスポンス

| Status | 内容 |
| --- | --- |
| 200 | 推薦処理成功 |
| 422 | 入力内容が不正 |
| 503 | 好きな理由の解析サービスが利用できない、または解析に失敗 |

推薦結果は最大5件です。

制約条件やCandidateデータの状態によっては、
推薦結果が0件となる場合があります。

#### Negative Preference

ユーザーが明示した非希望を考慮して、
推薦候補の表示可否や優先順位を決定します。

- `low_interest`：該当候補の優先順位を下げる
- `avoid`：該当候補を除外する
- 強い拒否について判断できない候補は保留する

保留・除外された候補は推薦結果に表示しません。

現在の制約対象の解決は、
限定的な対応表を使用した開発段階の実装です。

## 自動テスト

backendディレクトリで実行します。

```powershell
uv run python -m pytest -q
```

通常の自動テストでは、Fake・Mock・SQLiteなどを利用して、
実Groq API・E5モデル・PostgreSQLへの依存を分離しています。

依存パッケージのセットアップ後であれば、
外部AIサービスへ接続せずに実行できます。

## Ruff

backendディレクトリで実行します。

### 静的解析

```powershell
uv run ruff check .
```

### フォーマット確認

```powershell
uv run ruff format --check .
```

### 自動修正・フォーマット

```powershell
uv run ruff check . --fix
uv run ruff format .
```

## AI Benchmark

AIモデルの比較や抽出処理の評価には、
通常テストとは別にBenchmarkを使用します。

backendディレクトリで実行します。

### Fake Provider

外部APIを使用せずに、
Benchmarkの実行基盤を確認できます。

```powershell
uv run python -m benchmarks.llm_provider.run_fake
```

### Groq

実際のGroq APIを使用する比較評価です。

```powershell
uv run python -m benchmarks.llm_provider.run_groq
```

実APIを使用するBenchmarkにはAPIキーが必要です。
APIの利用制限や費用に注意してください。

## フロントエンド

### セットアップ

リポジトリのルートから実行します。

```powershell
Set-Location frontend
npm install
```

環境変数ファイルが未作成の場合は作成してください。

```powershell
Copy-Item .env.local.example .env.local
```

### 起動

frontendディレクトリで実行します。

```powershell
npm run dev
```

ブラウザで `http://localhost:3000` を開きます。

### Lint

```powershell
npm run lint
```

### Production build

```powershell
npm run build
```
