import { Sidebar } from '@/components/sidebar/sidebar';
import { Header } from '@/components/header/header';

export default function Home() {
  return (
    <div className="flex h-dvh flex-col overflow-hidden">
      <Header />
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          
          <h1 className="text-3xl font-semibold tracking-tight">
            開発環境は正常に動作しています
        </h1>
        <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-400">
          Team Project frontend
        </p>

          <Sidebar />
          
        </div>
      </main>
    </div>
  );
}
