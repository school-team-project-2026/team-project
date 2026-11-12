import React from 'react';

export const Header: React.FC = () => {
    return (
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-800 bg-slate-900 px-6 text-white">
            <span className="text-lg font-bold">Header</span>
        </header>
    )
}