"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import { BiGlobe } from 'react-icons/bi';
import { BiHome } from "react-icons/bi";
import { BiSearchAlt2 } from "react-icons/bi";
import { BiSolidCog } from "react-icons/bi";
import { BiWorld } from "react-icons/bi";

//型定義
export interface SidebarItem {
    id: string;
    label: string;
    icon: React.ReactNode;
    href: string;
    badge?: string | number;
}

//サイドバー固定化のため定数で定義
const SIDEBAR_ITEMS: SidebarItem[] = [
    {
        id: 'home',
        label: 'ホーム',
        href: '/',
        icon: <BiHome />
    },
    {
        id: 'abstraction',
        label: '抽象化',
        icon: <BiGlobe />,
        href: '/abstraction',
    },
    {
        id: 'search',
        label: '検索',
        icon: <BiSearchAlt2 />,
        href: '/search',
    },
    {
        id: 'sns',
        label: 'SNS',
        icon: <BiWorld />,
        href: '/sns',
    },
    {
        id: 'setting',
        label: '設定',
        icon: <BiSolidCog />,
        href: '/setting',
    },
];

//サイドバーコンポーネント
export const Sidebar: React.FC = () => {
    // クライアントコンポーネントでは初期値として現在のパスを設定
    const currentPath = usePathname() || '/';

    return (
        <aside className="fixed top-0 left-0 bottom-0 z-30 w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 border-r border-slate-800 transition-all duration-300"
         aria-label="メインナビゲーション">
            {/*ロゴ・ヘッダー領域*/}
            <div className="flex items-center justify-center sm:justify-start gap-3 h-16 px-4 border-b border-slate-800">
                <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center tect-white font-bold shrink-0">
                    A
                </div>
                <span className="hidden sm::inline text-lg font-bold text-ehite tracking-eide truncate">
                    Admin Console
                </span>
            </div>

            {/*ナビゲーションリンク*/}
            <nav className="flex-1 py-4 overflow-y-auto">
                <ul className="space-y-1 px-2">
                    {SIDEBAR_ITEMS.map((item) => {
                        const isActive = currentPath === item.href;
                        return (
                            <li key={item.id}>
                                <a href={item.href}
                                    className={`relative flex items-center justify-center sm:justify-start gap-3 px-3 py-3 rounded-lg text-sm font-medium transition-all ${
                                        isActive
                                            ? 'bg-blue-600/10 text-blue-400 font-semibold'
                                            : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                                    }`}
                                >
                                    {isActive && (
                                        <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-500 rounded-r-full" />
                                    )}

                                    {/*アイコン*/}
                                    <span className={isActive ? 'text-blue-400' : 'text-slate-400'}>
                                        {item.icon}
                                    </span>

                                    {/*ラベル*/}
                                    <span className="hidden sm:inline truncate">{item.label}</span>

                                    {/*バッジ*/}
                                    {item.badge !== undefined &&(
                                        <span className={`hidden sm:inline-block ml-auto px-2 py-0.5 text-xs rounded-full ${
                                            isActive
                                                ? 'bg-blue-500/20 text-blue-300'
                                                : 'bg-slate-800 text-slate-400'
                                        }`}
                                        >
                                            {item.badge}
                                        </span>
                                    )}
                                </a>
                            </li>
                        )
                    })}
                </ul>
            </nav>
        </aside>
    )
}