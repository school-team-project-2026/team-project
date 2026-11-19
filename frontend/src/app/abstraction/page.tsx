import { Sidebar } from '@/components/sidebar/sidebar';
import { Header } from '@/components/header/header'; 

export default function Abstraction_Home() {
  return (
    <div className="flex h-dvh flex-col">
      <Header />

      <div className="flex flex-1 min-h-0">
        <Sidebar />

        <main className="min-w-0 flex-1 overflow-y-auto bg-zinc-50 px-6 py-8 dark:bg-zinc-900">
          <div className="text-center">
            <h1 className="text-3xl font-semibold tracking-tight">
              抽象化ホーム
            </h1>
          </div>
        </main>
      </div>
    </div>
  );
}
