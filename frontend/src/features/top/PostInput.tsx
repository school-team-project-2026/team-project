export default function PostInput() {
    return (
        <div className="flex items-center gap-3 rounded-xl bg-white p-4 shdow-sm">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200">
                👤
            </div>

            <div className="flex-1 rounded-full bg-gray-100 px-4 py-3 text-sm text-gray-500">
                今日は何したいですか？
            </div>

            <span className="text-sm text-indigo-600">
                写真
            </span>
        </div>
    );
}