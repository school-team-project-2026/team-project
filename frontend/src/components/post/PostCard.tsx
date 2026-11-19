import Image from "next/image";

type Post = {
    id: number;
    content: string;
    hobby: string;
    likes: number;
    imageUrl?: string;
};

// 親コンポーネントから受け取るデータ型指定
type PostCardProps = {
    post: Post;
};

function PostCard({ post }: PostCardProps) {
    return (
        <article className="w-full rounded-xl border border-gray-200 bg-white p-5 shadow-sm">

            {/* 趣味カテゴリ */}
            <div className="mb-3 flex items-center justify-between">
                <span className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-600">
                    #{post.hobby}
                </span>

                <span className="text-xs text-gray-400">
                    匿名投稿
                </span>
            </div>

            {/* 投稿文章 */}
            <p className="mb-4 text-gray-700">
                {post.content}
            </p>

            {/* 投稿画像 */}
            {post.imageUrl && (
                <div className="relative mb-4 aspect-video w-full overflow-hidden rounded-lg">
                    <Image
                        src={post.imageUrl}
                        alt={`${post.hobby}の画像`}
                        fill
                        sizes="(max-width: 768px) 100vw, 672px"
                        className="object-cover"
                    />
                </div>
            )}

            {/* いいね */}
            <div className="border-t border-gray-100 pt-3">
                <span className="text-sm text-gray-500">
                    ♡ {post.likes}
                </span>
            </div>

        </article>
    );
}

export default PostCard;