# Team Project

学校のチーム制作プロジェクトです。

正式なプロジェクト名・アプリ名は未定です。

## 必要なツール

- Git
- Node.js 20.9以降
- npm
- uv
- Python 3.13
- Docker Desktop
- VS Code（推奨）

## ディレクトリ構成

- `frontend/`：Next.jsフロントエンド
- `backend/`：FastAPIバックエンド
- `docs/`：仕様・議事録・手順
- `compose.yaml`：共通DB環境

## 環境変数

リポジトリのルートで、PostgreSQL用の環境変数ファイルを作成します。

```powershell
Copy-Item .env.example .env
```

`.env` の `POSTGRES_PASSWORD` は各自のローカル開発用パスワードへ変更してください。
`.env` はGitの管理対象外です。

フロントエンド用の環境変数ファイルも作成します。

```powershell
Copy-Item frontend/.env.local.example frontend/.env.local
```

`NEXT_PUBLIC_API_BASE_URL` はブラウザから接続できるバックエンドのURLです。
`NEXT_PUBLIC_` で始まる値はブラウザへ公開されるため、秘密情報を設定しないでください。

## バックエンド

### セットアップ

```powershell
Set-Location backend
uv python install 3.13
uv sync
```

Python 3.13が既にインストールされている場合、`uv python install 3.13` は省略できます。

### 起動

```powershell
Set-Location backend
uv run uvicorn app.main:app --reload
```

APIは `http://localhost:8000` で起動します。

### ヘルスチェック

バックエンド起動後、ブラウザで `http://localhost:8000/health` を開くか、
PowerShellで次を実行します。

```powershell
Invoke-RestMethod http://localhost:8000/health
```

正常時は `{"status":"ok"}` が返ります。

Swagger UIは `http://localhost:8000/docs` で確認できます。

### テスト

```powershell
Set-Location backend
uv run pytest
```

### Ruff

チェックのみ実行する場合：

```powershell
Set-Location backend
uv run ruff check .
```

フォーマットを変更せずに確認する場合：

```powershell
Set-Location backend
uv run ruff format --check .
```

自動修正とフォーマットを行う場合：

```powershell
Set-Location backend
uv run ruff check . --fix
uv run ruff format .
```

## フロントエンド

### セットアップ

```powershell
Set-Location frontend
npm install
Copy-Item .env.local.example .env.local
```

### 起動

```powershell
Set-Location frontend
npm run dev
```

ブラウザで `http://localhost:3000` を開きます。

### Lint

```powershell
Set-Location frontend
npm run lint
```

### Production build

```powershell
Set-Location frontend
npm run build
```

## PostgreSQL

Docker Desktopを起動し、リポジトリのルートで実行します。

起動：

```powershell
docker compose up -d db
```

状態確認：

```powershell
docker compose ps
```

停止：

```powershell
docker compose down
```

データはDockerの名前付きボリューム `postgres-data` に保存されるため、
通常の `docker compose down` では削除されません。
将来pgvectorを導入する際は、PostgreSQL 16互換のpgvectorイメージへの変更と
拡張機能の有効化を検討します。
