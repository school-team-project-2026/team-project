import { Sidebar } from '@/components/sidebar/sidebar';

export default function Search_Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight">
            探すホーム
        </h1>

        <Sidebar />

      </div>
    </main>
  );
}
