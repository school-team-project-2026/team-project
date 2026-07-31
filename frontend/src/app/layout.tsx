import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Team Project",
  description: "チーム制作プロジェクト",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
