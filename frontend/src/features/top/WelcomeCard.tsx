export default function WelcomeCard() {
    return (
        <section className="rounded-xl bg-white p-5 shadow-sm">

            <h2 className="text-lg font-bold text-gray-900">
                ようこそ！
            </h2>

            <p className="mt-2 text-sm text-gray-500">
                あと1ステップで、あなた向けのホームが完成します。
            </p>

            {/* 初期設定の進捗 */}
            <div className="mt-5">
                <div className="mb-2 flex justify-between text-sm">
                    <span className="text-gray-700">
                        初期設定の進捗
                    </span>
                    <span className="text-indigo-600">
                        50%
                    </span>
                </div>

                <div className="h-2 w-full rounded-full bg-gray-200">
                    <div className="h-2 w-1/2 rounded-full bg-indigo-500" />
                </div>
            </div>

            {/* ステップ一覧 */}
            <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">

                <div className="rounded-lg bg-indigo-50 p-4">
                    <p className="font-medium text-indigo-700">
                        ✓ プロフィール完成
                    </p>
                    <p className="mt-1 text-xs text-gray-500">
                        完了
                    </p>
                </div>

                <div className="rounded-lg bg-gray-100 p-4">
                    <p className="font-medium text-gray-700">
                        仲間とつながる
                    </p>
                    <p className="mt-1 text-xs text-gray-500">
                        未完了
                    </p>
                </div>

            </div>
        </section>
    );
}