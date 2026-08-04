# 第1回バックエンド勉強会
## C・C#経験者のためのPython入門と処理分解

> 対象：C・C#の基礎経験があり、Python固有の書き方や処理分解に不安がある人  
> 開催形式：Discord＋画面共有  
> 想定時間：休憩込み約3時間

---

## 0. この回の位置づけ

1. 第1回：C・C#からPythonへ／処理分解とアルゴリズム
2. 第2回：単体プログラムとWebアプリケーションの違い／HTTP・API・FastAPI導入
3. 第3回：Pythonのクラス基礎／Pydantic／FastAPI／pytest
4. 第4回：PostgreSQL／SQLAlchemy／CRUD

この回ではFastAPIやクラスを本格的には扱いません。クラスは第3回で、Pydanticモデルを題材に基礎から扱います。

---

# 1. この回の目標

- C・C#とPythonで共通する考え方を説明できる
- Pythonのインデントがブロックを表すことを理解する
- `range`の開始値・終了値・増分を説明できる
- Pythonの`for`が値を順番に取り出す構文だと理解する
- `list`と`dict`を使った簡単な処理を書ける
- 関数の引数と戻り値を説明できる
- 基本的な型ヒントを読める
- 日本語の要求を「入力・処理・出力」に分解できる
- 小さなPython関数を作れる
- 課題をGitHubへ提出できる

---

# 2. まず確認：何が共通しているのか

新しい言語を学ぶとき、すべてを最初から覚え直す必要はありません。C、C#、Pythonでは、書き方は違っても根底の考え方は共通しています。

| 共通する考え方 | C・C# | Python |
|---|---|---|
| 値を保存する | 変数 | 変数 |
| 条件で分ける | `if` | `if` |
| 繰り返す | `for` / `foreach` | `for` |
| 複数の値を扱う | 配列 / `List<T>` | `list` |
| キーと値を扱う | `Dictionary<TKey, TValue>` | `dict` |
| 処理をまとめる | 関数 / メソッド | 関数 |
| 結果を返す | `return` | `return` |

重要なのは、**考え方はかなり共通しており、主に変わるのは構文と標準機能**だという点です。

---

# 3. C・C#とPythonの主な違い

## 3.1 波括弧ではなくインデント

C#：

```csharp
if (score >= 80)
{
    Console.WriteLine("合格");
}
```

Python：

```python
if score >= 80:
    print("合格")
```

Pythonではインデントがプログラムの構造そのものです。

## 3.2 セミコロンは基本的に不要

```python
score = 80
print(score)
```

## 3.3 変数宣言と型ヒント

```python
score = 80
title = "Sample"

score: int = 80
title: str = "Sample"
```

型ヒントは、読みやすさと開発支援のために使います。

---

# 4. Pythonの `for` と `range`

C#：

```csharp
for (int i = 0; i < 5; i++)
{
    Console.WriteLine(i);
}
```

Python：

```python
for i in range(5):
    print(i)
```

実行結果：`0, 1, 2, 3, 4`

## 4.1 `range` の基本形

```python
range(終了値)
range(開始値, 終了値)
range(開始値, 終了値, 増分)
```

```python
for i in range(1, 6):
    print(i)
```

終了値の6は含みません。

```python
for i in range(1, 10, 2):
    print(i)
```

実行結果：`1, 3, 5, 7, 9`

## 4.2 値を順番に取り出す

```python
scores = [80, 65, 90]

for score in scores:
    print(score)
```

Pythonの`for`は、C#の`foreach`に近い考え方です。

## 4.3 二重ループ

```python
for row in range(1, 4):
    for column in range(1, 4):
        print(row, column)
```

外側のループが1回進む間に、内側のループが最後まで動きます。値を表にして追うと理解しやすくなります。

---

# 5. `list` の基本

```python
scores = [80, 65, 90, 75, 100]
```

C#の配列や`List<T>`に近いデータ構造です。

## 5.1 添字・長さ・追加

```python
print(scores[0])
print(len(scores))
scores.append(85)
```

## 5.2 条件に合う値を集める

```python
high_scores = []

for score in scores:
    if score >= 80:
        high_scores.append(score)
```

## 5.3 よく使う組み込み関数

```python
len(scores)
sum(scores)
max(scores)
min(scores)
```

空の`list`に対する`max`や`min`はエラーになるため注意します。

---

# 6. `dict` の基本

```python
result = {
    "count": 5,
    "average": 82.0,
}
```

C#の`Dictionary<TKey, TValue>`に近い考え方です。

```python
print(result["count"])
result["highest"] = 100
```

複数の計算結果をまとめて返すときにも使えます。第2回以降では、`dict`に近い形のデータがJSONとしてWeb上をやり取りします。

---

# 7. 関数・引数・戻り値

```python
def add(a, b):
    return a + b
```

- `a`と`b`：引数
- `a + b`：処理
- `return`：結果を呼び出し元へ返す

## 7.1 `print`と`return`の違い

```python
def show_total(a, b):
    print(a + b)

def calculate_total(a, b):
    return a + b
```

`print`は画面へ表示し、`return`は結果を次の処理へ渡します。Web APIやテストでは`return`が重要です。

## 7.2 型ヒント

```python
def is_even(number: int) -> bool:
    return number % 2 == 0

def calculate_average(scores: list[int]) -> float:
    return sum(scores) / len(scores)
```

---

# 8. 処理分解とアルゴリズム

例：

> 点数一覧を受け取り、80点以上の点数だけを返す

## 入力

- 点数一覧
- 基準点

## 処理

1. 結果用の空リストを作る
2. 点数を1件ずつ取り出す
3. 基準点以上か判定する
4. 条件を満たした点数を結果へ追加する

## 出力

- 条件を満たした点数一覧

## 疑似コード

```text
結果用の空リストを作る
点数を1件ずつ確認する
    基準点以上なら
        結果へ追加する
結果を返す
```

## Pythonへ変換

```python
def filter_high_scores(scores: list[int], threshold: int) -> list[int]:
    result = []

    for score in scores:
        if score >= threshold:
            result.append(score)

    return result
```

## 動かないときの確認順

1. 入力は想定どおりか
2. 変数には何が入っているか
3. 条件式は正しいか
4. ループは必要な回数動いているか
5. `return`しているか
6. 表示している値と返している値を混同していないか

---

# 9. 講義中の小演習

実際のコードは`exercises.py`にあります。

1. 1から5まで表示する
2. 1から10までの奇数だけ表示する
3. 80点以上の点数だけを新しい`list`へ入れる
4. 件数・合計・最高点を`dict`へまとめる
5. 高得点抽出処理を関数にする

---

# 10. 統合課題

## 作品評価の集計関数を作る

整数の評価点を格納した`list`を受け取り、次の内容を`dict`で返します。

- 評価件数
- 合計点
- 平均点
- 最高点
- 最低点
- 80点以上の件数

```python
def summarize_scores(scores: list[int]) -> dict[str, int | float]:
    ...
```

コードを書く前に、入力・処理・出力・境界値を整理します。

---

# 11. GitHubへの提出

```bash
git switch -c training/backend-lesson-01
git status
git diff
git add docs/training/backend/lesson-01
git commit -m "docs: complete backend training lesson 01"
git push -u origin training/backend-lesson-01
```

PR本文：

```text
## 実施内容
## 確認方法
## 難しかった部分
## 質問したい部分
```

---

# 12. 宿題

所要時間：10〜15分

`homework.py`の`filter_high_scores`を完成させ、確認質問へ回答します。

---

# 13. 自己確認チェックリスト

- [ ] Pythonではインデントがブロックを表すと説明できる
- [ ] `range(1, 6)`で6が含まれないと説明できる
- [ ] Pythonの`for`が値を1件ずつ取り出すと説明できる
- [ ] `list`へ値を追加できる
- [ ] `dict`へ複数の結果をまとめられる
- [ ] `print`と`return`の違いを説明できる
- [ ] 型ヒントを読める
- [ ] 要求を入力・処理・出力へ分けられる
- [ ] 小さな関数を書ける
- [ ] GitHubへ課題を提出できる

---

# 14. 次回予告

第2回では、今回作ったPython関数を題材に、単体プログラムとWebアプリケーションの違い、クライアントとサーバー、HTTP、GETとPOST、API、FastAPIの導入を扱います。

---

# 15. 参考資料

- Python公式チュートリアル
- FastAPI公式 Python Types Intro
- MIXI 新卒技術研修
- サイボウズ新人研修
- Microsoft Web Development for Beginners
- CS50系教材
- GitHub公式ドキュメント

本資料は、公開資料の教育設計や説明順を参考にしつつ、今回の受講者とプロジェクト向けに独自に再構成しています。
