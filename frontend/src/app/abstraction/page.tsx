import { Sidebar } from '@/components/sidebar/sidebar';
import { Header } from '@/components/header/header'; 

export default function Abstraction_Home() {
  return (
    <div className="flex h-dvh flex-col overflow-hidden">
      <Header />
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <h1 className="text-3xl font-semibold tracking-tight">
            抽象化ホーム
          </h1>
          <Sidebar />
        </div>
      </main>
    </div>
  );
}
