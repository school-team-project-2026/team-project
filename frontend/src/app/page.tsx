import { Sidebar } from '@/components/sidebar/sidebar';
import { Header } from '@/components/header/header';
import PostCard from "@/components/post/PostCard";
import WelcomeCard from "@/features/top/WelcomeCard";
import PostInput from "@/features/top/PostInput";
import RightSidebar from '@/features/top/RightSidebar';

//仮データ
const posts = [
  {
    id: 1,
    content: 'これはサンプルの投稿です。',
    hobby: 'プログラミング',
    likes: 10,
    imageUrl: '/images/posts/sample.jpg',
  },
  {
    id: 2,
    content: 'これは別のサンプルの投稿です。',
    hobby: '読書',
    likes: 5,
  },
  {
    id: 3,
    content: 'これはさらに別のサンプルの投稿です。',
    hobby: '旅行',
    likes: 8,
  },
];

export default function Home() {
  return (
    <div className="flex h-dvh flex-col">

      <Header />

      <div className="flex flex-1 min-h-0">

        <Sidebar />

        <main className="min-w-0 flex-1 overflow-y-auto bg-zinc-50 px-6 py-8 dark:bg-zinc-900">
          
          <div className="mx-auto max-w-7xl">

            <h1 className="mb-6 text-2xl font-bold">
              新しい「好き」を見つけよう！
            </h1>

            <div className="grid gri-cols-1 gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(240px,1fr)]">

              {/*中央エリア*/}
              <div className="min-w-0 space-y-6">

                <WelcomeCard />

                <PostInput />

                <section>
                  <h2 className="mb-4 text-xl font-semibold">
                    新着投稿
                  </h2>

                  <div className="space-y-4">
                   {posts.map((post) => (
                     <PostCard key={post.id} post={post} />
                    ))}
                  </div>
                </section>

              </div>

              {/*右サイドバー*/}
              <RightSidebar />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
