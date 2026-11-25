const trends = [
    { name: "旅行", count: 120 },
    { name: "写真", count: 98 },
    { name: "プログラミング", count: 76 },
];

const hobbies = ["ゲーム", "音楽", "読書"];

export default function RightSidebar() {
    return (
        <aside className="space-y-4">

            {/* 今日のまとめ */}
            <section className="rounded-xl bg-indigo-600 p-5 text-white">
                <h2 className="text-lg font-bold">
                    今日のまとめ
                </h2>

                <p className="mt-3 text-2xl font-bold">
                    3件
                </p>

                <p className="mt-1 text-sm text-indigo-100">
                    新しい反応があります
                </p>

                <div className="mt-4 border-t border-indigo-400 pt-3">
                    <p className="text-sm">
                        趣味の世界をもっと広げよう！
                    </p>
                </div>
            </section>

            {/* 今日のトレンド */}
            <section className="rounded-xl bg-white p-5 shadow-sm">
                <h2 className="mb-4 font-bold text-gray-900">
                    今日のトレンド
                </h2>

                <div className="space-y-3">
                    {trends.map((trend) => (
                        <div
                            key={trend.name}
                            className="flex items-center justify-between"
                        >
                            <span className="text-sm text-gray-700">
                                #{trend.name}
                            </span>

                            <span className="text-xs text-gray-400">
                                {trend.count}件
                            </span>
                        </div>
                    ))}
                </div>
            </section>

            {/* おすすめの趣味 */}
            <section className="rounded-xl bg-white p-5 shadow-sm">
                <h2 className="mb-3 font-bold text-gray-900">
                    おすすめの趣味
                </h2>

                <p className="mb-3 text-sm text-gray-500">
                    新しい趣味を探してみませんか？
                </p>

                <div className="flex flex-wrap gap-2">
                    {hobbies.map((hobby) => (
                        <span
                            key={hobby}
                            className="rounded-full bg-indigo-50 px-3 py-1 text-sm text-indigo-600"
                        >
                            #{hobby}
                        </span>
                    ))}
                </div>
            </section>

        </aside>
    );
}