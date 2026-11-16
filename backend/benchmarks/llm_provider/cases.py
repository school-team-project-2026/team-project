from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    name: str
    category: str
    comment: str


CASES = [
    BenchmarkCase(
        case_id="CASE-01",
        name="ブルーアーカイブ",
        category="ゲーム",
        comment="世界観が好き",
    ),
    BenchmarkCase(
        case_id="CASE-02",
        name="架空SF映画",
        category="映画",
        comment="世界の設定を少しずつ理解して考察していくのが好き",
    ),
    BenchmarkCase(
        case_id="CASE-03",
        name="F1",
        category="モータースポーツ",
        comment="マシン開発とドライバー同士の駆け引きが好き",
    ),
    BenchmarkCase(
        case_id="CASE-04",
        name="ロードスター",
        category="自動車",
        comment="軽くて、自分で車を操っている感覚が強いところが好き",
    ),
    BenchmarkCase(
        case_id="CASE-05",
        name="高速ジャズ",
        category="音楽",
        comment="音が多くて忙しいのに、全体としてまとまっている感じが好き",
    ),
    BenchmarkCase(
        case_id="CASE-06",
        name="架空RPG",
        category="ゲーム",
        comment=(
            "戦闘そのものにはあまり興味がなく、知らない場所を探索して発見するのが好き"
        ),
    ),
    BenchmarkCase(
        case_id="CASE-07",
        name="架空作品A",
        category="アニメ",
        comment="なんとなく雰囲気が好き",
    ),
    BenchmarkCase(
        case_id="CASE-08",
        name="ガーデニング",
        category="園芸",
        comment="少しずつ手をかけた結果が時間をかけて形になるところが好き",
    ),
]
