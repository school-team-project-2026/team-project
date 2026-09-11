# PRISM LLM Provider Benchmark v0.1

## 1. 目的

PRISM Stage 0で使用するLLM Provider / Modelを、
同一条件で比較し、嗜好特徴抽出に最も適した候補を選定する。

このBenchmarkでは一般的なLLM性能ではなく、
PRISMの用途である

Interest Item
→ 嗜好特徴抽出
→ Structured Output
→ Recommendation

への適性を評価する。

Stage 0では原則として無料で利用可能なProviderを優先する。

有料Providerは、
無料Baselineでは明確に品質不足と判断された場合や、
Human Evaluation等で品質上限を測る必要が生じた場合に
Referenceとして比較する。

---

## 2. 共通Input

各Modelには以下の3項目を渡す。

- name
- category
- comment

例：

name: ブルーアーカイブ
category: ゲーム
comment: 世界観が好き

commentを最も強いEvidenceとして扱う。

name / categoryは文脈補助として利用するが、
Model自身が知っている対象情報を、
ユーザー本人の嗜好として勝手に追加してはならない。

---

## 3. 共通Output Schema

すべてのModelで以下のPreferenceFeaturesを使用する。

```python
class PreferenceFeatures(BaseModel):
    attributes: list[str] = Field(default_factory=list)
    appeal_points: list[str] = Field(default_factory=list)
    desired_experiences: list[str] = Field(default_factory=list)
    values: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
Field Definition

attributes:
対象そのものの、ユーザーの好みに関係している特徴。

appeal_points:
ユーザー本人が明示・強く示唆した魅力。

desired_experiences:
その対象を通して得たいと考えられる体験。

values:
好みの背後にある評価軸・価値基準。

keywords:
ジャンル横断比較や検索に利用しやすい短い概念語。

Evidenceが不足する場合は、
無理に特徴を生成せず空配列を許可する。

4. 共通Prompt

You extract a user's preference features for a cross-domain
recommendation system.

Rules:

Treat the user's comment as the strongest evidence.
Use the item name and category only as context.
Do not invent preferences that the user did not express or strongly imply.
Prefer concepts that can be compared across different domains such as
media, sports, vehicles, music, travel, and other hobbies.
If there is not enough evidence for a field, return an empty list.
Keep each feature concise.
Return features in Japanese.
5. Benchmark Cases
CASE-01: 既知作品・Evidence少

name: ブルーアーカイブ
category: ゲーム
comment: 世界観が好き

目的：
Model自身の作品知識をユーザー嗜好として過剰補完しないか確認する。

CASE-02: 架空作品・考察

name: 架空SF映画
category: 映画
comment: 世界の設定を少しずつ理解して考察していくのが好き

目的：
作品知識に頼らず、
考察・発見・設定理解等を横断的な特徴へ変換できるか確認する。

CASE-03: スポーツ

name: F1
category: モータースポーツ
comment: マシン開発とドライバー同士の駆け引きが好き

目的：
作品以外のジャンルでも同一Schemaが機能するか確認する。

CASE-04: 自動車

name: ロードスター
category: 自動車
comment: 軽くて、自分で車を操っている感覚が強いところが好き

目的：
操作感、一体感、軽快さ等へ適切に抽象化できるか確認する。

CASE-05: 音楽

name: 高速ジャズ
category: 音楽
comment: 音が多くて忙しいのに、全体としてまとまっている感じが好き

目的：
高密度、複雑さ、秩序など、
作品系とは異なる好みを抽象化できるか確認する。

CASE-06: Negative Preference

name: 架空RPG
category: ゲーム
comment: 戦闘そのものにはあまり興味がなく、知らない場所を探索して発見するのが好き

目的：
categoryから「戦闘が好き」等を誤推論せず、
否定された特徴をPreferenceとして抽出しないか確認する。

CASE-07: Evidence不足

name: 架空作品A
category: アニメ
comment: なんとなく雰囲気が好き

目的：
Evidence不足時に特徴を大量に捏造せず、
空配列を利用できるか確認する。

CASE-08: 非作品ジャンル

name: ガーデニング
category: 園芸
comment: 少しずつ手をかけた結果が時間をかけて形になるところが好き

目的：
作品・スポーツ・自動車以外でも、
継続、成長、変化を見守る体験等へ横断抽象化できるか確認する。

6. Quality Score

100点満点。

Evaluation	Score
Input Fidelity	30
Cross-domain Abstraction	20
Recommendation Usefulness	20
Structured Output Stability	15
Field Separation	10
Japanese Quality	5
Input Fidelity

入力から根拠のないPreferenceを追加していないか。

特に重要な評価項目とする。

Cross-domain Abstraction

特定ジャンル専用の特徴だけでなく、
異分野推薦にも利用できる特徴へ抽象化できているか。

Recommendation Usefulness

後段のEmbedding、Similarity、Rankingへ
利用可能な特徴になっているか。

Structured Output Stability

指定Schemaに従い、
欠損・不正形式なく安定して出力できるか。

Field Separation

attributes / appeal_points / desired_experiences / values / keywords
の役割が過度に重複していないか。

Japanese Quality

簡潔で自然かつ意味の明確な日本語になっているか。

7. Operation Score

100点満点。

Evaluation	Score
Free Usage / Rate Limit	25
Privacy / Data Policy	20
API / SDK Usability	15
Structured Output Implementation	15
Latency	10
Team Reproducibility	10
Provider Stability	5

Quality Scoreとは別に記録し、
最終判断時にも両方のRaw Scoreを保存する。

8. Execution Rule

各Modelについて各Caseを3回実行する。

8 Cases × 3 Runs = 24 Requests / Model

すべて同一Prompt、同一PreferenceFeatures Schema、
同一Inputを使用する。

可能な限りModelのRandomness / Reasoning設定も固定する。

Provider固有の制約により完全一致できない場合は、
設定差をBenchmark結果へ記録する。

9. Result Record

各Requestについて以下を保存する。

provider:
model:
case_id:
run_no:

schema_valid:
latency_ms:

input_tokens:
output_tokens:

output:

fidelity_score:
abstraction_score:
usefulness_score:
structured_output_score:
field_separation_score:
japanese_quality_score:

notes:

10. Candidate Providers

候補はBenchmark開始時点の公式情報を再確認して決定する。

現時点の想定候補：

Gemini系 Free Tier
Groq / GPT-OSS系
Groq / Qwen系

必要に応じて：

OpenRouter Free
Ollama Local

を特別枠として追加する。

具体的なModel ID、Free Tier、Rate Limit、
Structured Output対応、Privacy Policyは
API Key取得前に公式情報を再確認する。

11. Selection Policy

Stage 0では無料Providerを優先する。

無料Providerが十分なQuality Scoreを得た場合、
Baseline Providerとして採用する。

無料Providerで明確な品質不足が確認された場合のみ、
有料ProviderをReferenceとして追加比較する。

最終選定では、

Quality
Cost
Privacy
Latency
Reproducibility
Provider Dependency

を総合して判断する。

「最も高性能なModel」ではなく、
「PRISM Stage 0に最も適したModel」を優勝とする。

## Preliminary Result - 2026-09-11

### Stage 0 Primary Candidate

Groq / `openai/gpt-oss-120b`

Stage 0の暫定Primary Provider / Modelとして採用する。

### Groq Preliminary Result

8 Cases × 1 Run:

- Success: 7
- API Failure: 1
- Schema Failure: 0

CASE-04では以下のエラーが発生した。

- BadRequestError
- HTTP 400
- `json_validate_failed`

CASE-04のみ再実行したが、同じエラーが再現した。

現在のGroq Providerでは Structured Outputs の
Best-effort Mode (`strict: false`) を使用している。

そのため、この結果は一時的な通信障害ではなく、
現在のStructured Output設定における再現性のある
Validation Failureとして記録する。

GPT-OSS 120BはStrict Mode (`strict: true`) に対応しているため、
正式なPreferenceExtractorへ統合する際にStrict Modeへの移行を行い、
再度Smoke Testする。

### Quality Tendency

良好だった点:

- Evidenceが少ない場合に空配列を利用できる
- 入力にない嗜好の過剰補完が比較的少ない
- Negative Preferenceを適切に扱えた
- ゲーム、スポーツ、音楽、園芸等でCross-domain abstractionが機能した
- 成功RequestはPreferenceFeaturesへ正常変換できた

注意点:

- `values`では一部、入力より強い推論が見られた
- Best-effort Structured OutputでCASE-04が再現性を持って失敗した

### Gemini Result

Gemini 3.8 FlashはQuality Reference / Fallbackとして保持する。

Quality面では高い抽象化能力を確認したが、
Free TierのRequest QuotaがPRISMの反復開発には厳しく、
Stage 0の日常開発Providerとしては採用しない。

### Decision

Primary:
Groq / `openai/gpt-oss-120b`

Fallback / Quality Reference:
Gemini 3.8 Flash

第3Providerの追加Benchmarkは現時点では行わない。

次の作業ではProvider Benchmarkを終了し、
PreferenceExtractorの正式実装へ戻る。

GroqについてはStrict Structured Output対応を
PreferenceExtractor統合時の必須確認事項とする。