"use client";
import AnalysisResult from "./AnalysisResult";

import {useState} from "react";

export default function HobbyInput(){
    const [hobby, setHobby] = useState("");
    const [reason, setReason ] = useState("");
    const [result, setResult] = useState<{
        hobby: string;
        reason: string;
    }| null>(null);

    const handleAnalyze = () =>{
        setResult({
            hobby: hobby.trim(),
            reason: reason.trim(),
        });
    };

    return (
        <section className="ronded-xl bg-white p-6 shadow-sm">
            <h2 className="mb-2 text-xl font-bold text-gray-900">
                あなたの「好き」を深掘りしよう
            </h2>

            <p className="mb-6 text-sm text-gray-500">
                趣味とその理由を入力してください。
            </p>

            <div className="space-y-5">
                <div>
                    <label
                        htmlFor="hobby"
                        className="mb-2 block text-sm font-medium"
                    >
                        趣味の名前
                    </label>

                    <input
                        id="hobby"
                        type="text"
                        value={hobby}
                        onChange={(e) => setHobby(e.target.value)}
                        placeholder="例：プログラミング"
                        className="w-full rounded-lg border border-gray-300 p-3"
                    />
                </div>

                <div>
                    <label
                        htmlFor="reason"
                        className="mb-2 block text-sm font-medium"
                    >
                        その趣味が好きな理由
                    </label>

                    <textarea
                        id="reason"
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="例：自分で問題を解決するのが楽しいから"
                        rows={4}
                        className="w-full rounded-lg border border-gray-300 p-3"
                    />
                </div>

                <button
                    type="button"
                    disabled={!hobby.trim() || !reason.trim()}
                    className="rounded-lg bg-green-700 px-6 py-3 font-medium text-white hover:bg-green-800 disabled:cursor-not-allowed disabled:opacity-50"
                    onClick={handleAnalyze}
                >
                    趣味を分析する
                </button>
            </div>

            {result &&(
                <div className="mt-6">
                    <AnalysisResult
                        hobby={result.hobby}
                        reason={result.reason}
                    />
                </div>
            )}
        </section>
    )
}