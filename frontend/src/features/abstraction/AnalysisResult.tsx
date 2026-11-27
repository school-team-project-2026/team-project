type AnalysisResultProps = {
    hobby:string;
    reason: string;
};

export default function AnalysisResult({
    hobby,
    reason,
}: AnalysisResultProps) {
    return(
        <section className="rounded-xl bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-xl font-bold text-gray-900">
                分析結果
            </h2>

            <p className="mb-2 text-sm text-gray-600">
                趣味：{hobby}
            </p>

            <p className="mb-4 text-sm text-gray-600">
                好きな理由：{reason}
            </p>

            <div className="rounded-lg bg-green-50 p-4">
                <p className="text-sm text-green-800">
                    入力された趣味と理由をもとに、興味や価値観の特徴を分析します。
                </p>
            </div>
        </section>
    );
}
