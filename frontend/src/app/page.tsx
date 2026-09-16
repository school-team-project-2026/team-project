import {LinkButton} from '@/components/Button/ButtonLink';

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight">
          開発環境は正常に動作しています
        </h1>
        <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-400">
          Team Project frontend
        </p>

        <LinkButton href="/search" className="mt-6">
          探すへ
        </LinkButton>

        <p>
          <LinkButton href="/sns" className="mt-6">
            SNSへ
          </LinkButton> 
        </p>
        
        <p>
          <LinkButton href="/abstraction" className="mt-6">
            抽象化へ
          </LinkButton>
        </p>

        <p>
          <LinkButton href="/setting" className="mt-6">
            設定へ
          </LinkButton>
        </p>
        
      </div>
    </main>
  );
}
