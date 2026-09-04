"use client";

import { FormEvent, useState } from "react";

type HealthResponse = {
  status: string;
};

type InterestItem = {
  id: number;
  name: string;
  category: string;
  comment: string;
  created_at: string;
};

export default function BackendCheckPage() {
  const [status, setStatus] = useState("未接続");
  const [error, setError] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [comment, setComment] = useState("");

  const [items, setItems] = useState<InterestItem[]>([]);

  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  async function checkBackend() {
    if (!apiBaseUrl) {
      setError("NEXT_PUBLIC_API_BASE_URL が設定されていません");
      return;
    }

    try {
      setError(null);
      setStatus("接続中...");

      const response = await fetch(`${apiBaseUrl}/health`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: HealthResponse = await response.json();
      setStatus(data.status);
    } catch (err) {
      setStatus("接続失敗");
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }

  async function loadInterestItems() {
    if (!apiBaseUrl) {
      setError("NEXT_PUBLIC_API_BASE_URL が設定されていません");
      return;
    }

    try {
      setError(null);

      const response = await fetch(`${apiBaseUrl}/interest-items`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: InterestItem[] = await response.json();
      setItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }

  async function createInterestItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!apiBaseUrl) {
      setError("NEXT_PUBLIC_API_BASE_URL が設定されていません");
      return;
    }

    try {
      setError(null);

      const response = await fetch(`${apiBaseUrl}/interest-items`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          category,
          comment,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      setName("");
      setCategory("");
      setComment("");

      await loadInterestItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }

  return (
    <main className="mx-auto min-h-screen max-w-2xl px-6 py-12">
      <h1 className="text-3xl font-semibold">
        Backend Connection Check
      </h1>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">Health Check</h2>

        <p className="mt-2">Backend Status: {status}</p>

        <button
          type="button"
          onClick={checkBackend}
          className="mt-4 rounded bg-black px-4 py-2 text-white"
        >
          Backendに接続
        </button>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">Interest Item POST</h2>

        <form
          onSubmit={createInterestItem}
          className="mt-4 flex flex-col gap-3"
        >
          <input
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="name"
            className="rounded border px-3 py-2"
          />

          <input
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            placeholder="category"
            className="rounded border px-3 py-2"
          />

          <textarea
            value={comment}
            onChange={(event) => setComment(event.target.value)}
            placeholder="comment"
            className="rounded border px-3 py-2"
          />

          <button
            type="submit"
            className="rounded bg-black px-4 py-2 text-white"
          >
            Interest Itemを登録
          </button>
        </form>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold">Interest Item GET</h2>

        <button
          type="button"
          onClick={loadInterestItems}
          className="mt-4 rounded bg-black px-4 py-2 text-white"
        >
          一覧を取得
        </button>

        <ul className="mt-4 space-y-4">
          {items.map((item) => (
            <li key={item.id} className="rounded border p-4">
              <p>
                #{item.id} {item.name}
              </p>
              <p>category: {item.category}</p>
              <p>comment: {item.comment}</p>
              <p className="text-sm">
                created_at: {item.created_at}
              </p>
            </li>
          ))}
        </ul>
      </section>

      {error && (
        <p className="mt-8 text-red-500">
          Error: {error}
        </p>
      )}
    </main>
  );
}