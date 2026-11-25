import Image from "next/image";
import { BiHeart, BiComment, BiShare } from "react-icons/bi";

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
            <p className="mb-4 whitespace-pre-wrap break-words text-gray-700">
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
            <div className="flex items-center gap-5 border-t border-gray-100 pt-3">
                <button
                    type="button"
                    className="flex items-center gap-2 text-gray-500 hover:text-red-500"
                    aria-label="いいね"
                >
                    <BiHeart size={20} />
                    <span className="text-sm">{post.likes}</span>
                </button>

                <button
                    type="button"
                    className="text-gray-500 hover:text-indigo-500"
                    aria-label="コメント"
                >
                    <BiComment size={20} />
                </button>

                <button
                    type="button"
                    className="ml-auto text-gray-500 hover:text-indigo-500"
                    aria-label="シェア"
                >
                    <BiShare size={20} />
                </button>
            </div>

        </article>
    );
}

export default PostCard;