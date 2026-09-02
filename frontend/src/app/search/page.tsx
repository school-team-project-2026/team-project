import {LinkButton} from '@/components/Button/ButtonLink';

export default function Search_Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight">
            探すホーム
        </h1>

        <LinkButton href="/" className="mt-6">
          homeへ
        </LinkButton>

        <p>
          <LinkButton href="/sns" className="mt-6">
            snsへ
          </LinkButton>
        </p>

        <p>
          <LinkButton href="/abstraction" className="mt-6">
            abstractionへ
          </LinkButton>
        </p>
      </div>
    </main>
  );
}
