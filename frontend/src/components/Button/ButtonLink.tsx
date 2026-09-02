"use client";

import React from 'react';

type LinkButtonProps = {
    href?: string;
    children: React.ReactNode;
    onClick?: () => void;
    className?: string;
};

export const LinkButton: React.FC<LinkButtonProps> = ({
    href,
    children,
    onClick,
    className = 'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 inline-block text-center',
}) => {
    if (href) {
        return (
            <a href={href} className={className}>
                {children}
            </a>
        );
    }

    return (
        <button onClick={onClick} className={className}>
            {children}
        </button>
    )
};