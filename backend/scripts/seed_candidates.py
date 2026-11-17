from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Candidate

SEED_CANDIDATES = [
    {
        "name": "オクトパストラベラーII",
        "candidate_type": "work",
        "domain": "game",
        "genre": "turn_based_rpg",
        "description": (
            "敵の弱点を突くブレイクシステムやBP管理を特徴とするターン制RPG。"
        ),
        "appeal_tags": [
            "戦略性",
            "弱点分析",
            "リソース管理",
        ],
    },
    {
        "name": "パンデミック",
        "candidate_type": "work",
        "domain": "board_game",
        "genre": "cooperative",
        "description": ("プレイヤー同士で協力し、感染症の拡大を防ぐボードゲーム。"),
        "appeal_tags": [
            "協力",
            "行動計画",
            "リソース管理",
        ],
    },
    {
        "name": "ボルダリング",
        "candidate_type": "activity",
        "domain": "sports",
        "genre": None,
        "description": (
            "手足の運び方を考えながら、設定された課題の完登を目指すスポーツ。"
        ),
        "appeal_tags": [
            "試行錯誤",
            "課題攻略",
            "達成感",
        ],
    },
    {
        "name": "リアル脱出ゲーム",
        "candidate_type": "experience",
        "domain": "puzzle",
        "genre": "escape_room",
        "description": (
            "手がかりを集め、謎を解きながら目標達成を目指す体験型イベント。"
        ),
        "appeal_tags": [
            "謎解き",
            "分析",
            "問題解決",
        ],
    },
    {
        "name": "スパイスカレー作り",
        "candidate_type": "activity",
        "domain": "cooking",
        "genre": None,
        "description": ("スパイスの種類や配合を工夫し、好みの味を追求する料理活動。"),
        "appeal_tags": [
            "組み合わせ",
            "試行錯誤",
            "創造性",
        ],
    },
]

SEED_CANDIDATES.extend(
    [
        # ===== Game =====
        {
            "name": "Portal 2",
            "candidate_type": "work",
            "domain": "game",
            "genre": "puzzle_action",
            "description": (
                "2つのポータルを設置し、空間同士をつなげる仕組みを"
                "利用して、立体的なパズルを解くゲーム。"
                "物体の移動や位置関係の理解が攻略の鍵となる。"
            ),
            "appeal_tags": [
                "空間認識",
                "物理パズル",
                "発想の転換",
                "仕組みの応用",
            ],
        },
        {
            "name": "Stardew Valley",
            "candidate_type": "work",
            "domain": "game",
            "genre": "farming_simulation",
            "description": (
                "農場を経営しながら、作物の栽培、釣り、採掘、"
                "住民との交流などを自分のペースで楽しむゲーム。"
                "季節に応じた農場の計画や発展も特徴。"
            ),
            "appeal_tags": [
                "農場経営",
                "生活の自由度",
                "季節ごとの計画",
                "少しずつ発展させる楽しさ",
            ],
        },
        # ===== Board Game =====
        {
            "name": "カタン",
            "candidate_type": "work",
            "domain": "board_game",
            "genre": "resource_management",
            "description": (
                "島に開拓地や街を建設し、資源の交換や配置を"
                "工夫して勝利点を獲得するボードゲーム。"
                "他プレイヤーとの交渉も重要になる。"
            ),
            "appeal_tags": [
                "資源交換",
                "開拓地の配置",
                "交渉",
                "状況に応じた計画",
            ],
        },
        {
            "name": "コードネーム",
            "candidate_type": "work",
            "domain": "board_game",
            "genre": "word_association",
            "description": (
                "チームの代表者が出すヒントを手がかりに、"
                "関連する単語を推理するボードゲーム。"
                "一つの言葉から複数の意味を連想する面白さがある。"
            ),
            "appeal_tags": [
                "言葉の連想",
                "ヒントの解釈",
                "チーム内の意思疎通",
                "推理",
            ],
        },
        # ===== Sports =====
        {
            "name": "バドミントン",
            "candidate_type": "activity",
            "domain": "sports",
            "genre": "racket_sport",
            "description": (
                "シャトルの速度や落下位置を予測しながら、"
                "ショットの種類やコースを使い分ける競技。"
                "相手の動きを見た駆け引きが特徴。"
            ),
            "appeal_tags": [
                "反応速度",
                "コースの駆け引き",
                "相手の動きの予測",
                "技術の習得",
            ],
        },
        {
            "name": "オリエンテーリング",
            "candidate_type": "activity",
            "domain": "sports",
            "genre": "navigation_sport",
            "description": (
                "地図やコンパスを利用し、野外に設置された"
                "チェックポイントを順番に巡るスポーツ。"
                "地形を読み、効率的な移動経路を判断する。"
            ),
            "appeal_tags": [
                "地図の読解",
                "経路選択",
                "地形の観察",
                "野外探索",
            ],
        },
        # ===== Puzzle =====
        {
            "name": "数独",
            "candidate_type": "activity",
            "domain": "puzzle",
            "genre": "logic_puzzle",
            "description": (
                "縦・横・ブロック内で数字が重複しないように"
                "マスを埋める論理パズル。"
                "確定情報から候補を絞り込む推論が中心となる。"
            ),
            "appeal_tags": [
                "論理的推論",
                "候補の絞り込み",
                "規則の活用",
                "集中力",
            ],
        },
        {
            "name": "ジグソーパズル",
            "candidate_type": "activity",
            "domain": "puzzle",
            "genre": "assembly_puzzle",
            "description": (
                "ピースの形状や色、絵柄のつながりを手がかりに、"
                "一枚の絵を組み立てるパズル。"
                "部分的な特徴から全体の位置を推測する。"
            ),
            "appeal_tags": [
                "形状の観察",
                "色彩の識別",
                "部分と全体の関係",
                "組み立て",
            ],
        },
        # ===== Cooking =====
        {
            "name": "パン作り",
            "candidate_type": "activity",
            "domain": "cooking",
            "genre": "baking",
            "description": (
                "小麦粉や水などから生地を作り、"
                "こね方、発酵時間、焼成条件を調整してパンを焼く活動。"
                "工程による食感や膨らみ方の違いを楽しめる。"
            ),
            "appeal_tags": [
                "発酵の観察",
                "生地の調整",
                "工程管理",
                "食感の追求",
            ],
        },
        {
            "name": "お菓子作り",
            "candidate_type": "activity",
            "domain": "cooking",
            "genre": "confectionery",
            "description": (
                "材料の計量や混ぜ方、温度管理などを工夫して"
                "焼き菓子やデザートを作る活動。"
                "味だけでなく見た目の仕上げも楽しめる。"
            ),
            "appeal_tags": [
                "正確な計量",
                "温度管理",
                "食感の調整",
                "見た目の演出",
            ],
        },
        # ===== Music =====
        {
            "name": "ジャズ鑑賞",
            "candidate_type": "activity",
            "domain": "music",
            "genre": "jazz",
            "description": (
                "演奏者ごとの即興演奏、リズムの取り方、"
                "楽器同士の掛け合いなどに注目してジャズを聴く活動。"
                "同じ曲でも演奏による違いを楽しめる。"
            ),
            "appeal_tags": [
                "即興演奏",
                "リズムの変化",
                "楽器の掛け合い",
                "演奏の個性",
            ],
        },
        {
            "name": "バンドでの合奏",
            "candidate_type": "activity",
            "domain": "music",
            "genre": "ensemble",
            "description": (
                "複数の楽器や歌を合わせて一つの楽曲を演奏する活動。"
                "テンポを共有し、他の演奏者の音を聴きながら"
                "自分の演奏を調整することが重要になる。"
            ),
            "appeal_tags": [
                "音の一体感",
                "演奏者同士の協調",
                "リズムの共有",
                "役割分担",
            ],
        },
        {
            "name": "DTMでの作曲",
            "candidate_type": "activity",
            "domain": "music",
            "genre": "music_production",
            "description": (
                "パソコン上の音楽制作ソフトを使用し、"
                "メロディ、リズム、音色、各トラックの構成を"
                "組み合わせて楽曲を制作する活動。"
            ),
            "appeal_tags": [
                "音色の設計",
                "楽曲構成",
                "トラックの編集",
                "音楽表現の創作",
            ],
        },
        # ===== Book =====
        {
            "name": "シャーロック・ホームズの冒険",
            "candidate_type": "work",
            "domain": "book",
            "genre": "detective_fiction",
            "description": (
                "シャーロック・ホームズが観察と推理によって"
                "事件の真相を解き明かす短編集。"
                "小さな手がかりから意外な結論へ至る過程が特徴。"
            ),
            "appeal_tags": [
                "観察による推理",
                "手がかりの分析",
                "事件の謎",
                "論理的な解明",
            ],
        },
        {
            "name": "三体",
            "candidate_type": "work",
            "domain": "book",
            "genre": "science_fiction",
            "description": (
                "科学研究や地球外文明との接触をめぐる"
                "大規模な物語を描いたSF小説。"
                "科学的な発想と、人類社会への影響を扱う。"
            ),
            "appeal_tags": [
                "科学的な思考実験",
                "地球外文明",
                "大規模な世界観",
                "文明同士の関係",
            ],
        },
        {
            "name": "星の王子さま",
            "candidate_type": "work",
            "domain": "book",
            "genre": "literary_fable",
            "description": (
                "さまざまな星を旅する王子の出会いを通じて、"
                "人間関係や大切なものについて問いかける物語。"
                "象徴的な会話や寓話的な表現が特徴。"
            ),
            "appeal_tags": [
                "寓話的な表現",
                "人間関係への問い",
                "象徴の読み解き",
                "価値観の再考",
            ],
        },
        # ===== Movie =====
        {
            "name": "インターステラー",
            "candidate_type": "work",
            "domain": "movie",
            "genre": "science_fiction",
            "description": (
                "人類の生存をかけた宇宙探査を描くSF映画。"
                "相対性理論に関わる時間の違いや、"
                "家族の関係が物語の重要な要素となる。"
            ),
            "appeal_tags": [
                "宇宙探査",
                "時間の相対性",
                "科学的な設定",
                "家族のドラマ",
            ],
        },
        {
            "name": "ナイブズ・アウト",
            "candidate_type": "work",
            "domain": "movie",
            "genre": "mystery",
            "description": (
                "富豪の死をめぐり、探偵が家族や関係者の"
                "証言を調べて真相に迫るミステリー映画。"
                "証言の食い違いや情報の見せ方が特徴。"
            ),
            "appeal_tags": [
                "証言の矛盾",
                "伏線の読み解き",
                "人物関係の推理",
                "情報の意外なつながり",
            ],
        },
        {
            "name": "ソウルフル・ワールド",
            "candidate_type": "work",
            "domain": "movie",
            "genre": "animation",
            "description": (
                "ジャズ演奏への情熱を持つ主人公を通じて、"
                "人生の目的や日々の喜びを描くアニメーション映画。"
                "音楽と生き方が物語の中心にある。"
            ),
            "appeal_tags": [
                "ジャズ音楽",
                "人生の目的",
                "日常の価値",
                "音楽への情熱",
            ],
        },
    ]
)


def seed_candidates() -> None:
    added = 0
    skipped = 0

    with SessionLocal() as session:
        for data in SEED_CANDIDATES:
            existing_id = session.scalar(
                select(Candidate.id).where(
                    Candidate.name == data["name"],
                    Candidate.domain == data["domain"],
                )
            )

            if existing_id is not None:
                skipped += 1
                continue

            session.add(Candidate(**data))
            added += 1

        session.commit()

    print(f"追加: {added}件 / 登録済み: {skipped}件")


if __name__ == "__main__":
    seed_candidates()
