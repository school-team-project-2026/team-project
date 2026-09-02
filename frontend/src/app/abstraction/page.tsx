import {LinkButton} from '@/components/Button/ButtonLink';

export default function Abstraction_Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight">
            抽象化ホーム
        </h1>
        <LinkButton href="/" className="mt-6">
          homeへ
        </LinkButton>

        <p>
          <LinkButton href="/search" className="mt-6">
            searchへ
          </LinkButton>
        </p>

        <p>
          <LinkButton href="/sns" className="mt-6">
            snsへ
          </LinkButton>
        </p>
      </div>
    </main>
  );
}
