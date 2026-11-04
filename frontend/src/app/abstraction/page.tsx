import { Sidebar } from '@/components/sidebar/sidebar';

export default function Abstraction_Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight">
            抽象化ホーム
        </h1>

        <Sidebar />

      </div>
    </main>
  );
}
