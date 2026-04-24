import React from 'react';
import { Route, BarChart3, Settings } from 'lucide-react';
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

function SidebarIcon({ icon: Icon, active, onClick, tooltip }) {
    return (
        <button 
            onClick={onClick}
            title={tooltip}
            className={cn(
                "p-3 rounded-xl cursor-pointer transition-all duration-300 group flex justify-center outline-none", 
                active ? "bg-blue-100 text-blue-600 shadow-sm scale-105" : "text-zinc-400 hover:bg-zinc-100 hover:text-zinc-900 hover:scale-105 active:scale-95"
            )}
        >
            <Icon size={20} className={cn("transition-transform pointer-events-none", !active && "group-hover:scale-110")} />
        </button>
    )
}

export default function Sidebar({ activeTab, setActiveTab }) {
    return (
        <aside className="w-20 bg-white border-r border-zinc-200/60 flex flex-col items-center py-6 gap-8 z-50 shrink-0">
            <div className="w-10 h-10 bg-zinc-900 text-white rounded-xl flex items-center justify-center font-bold text-lg shadow-sm">
                O
            </div>
            <nav className="flex flex-col gap-3">
                <SidebarIcon 
                    icon={Route} 
                    active={activeTab === 'OPERATIONS'} 
                    onClick={() => setActiveTab('OPERATIONS')} 
                    tooltip="Live Operations"
                />
                <SidebarIcon 
                    icon={BarChart3} 
                    active={activeTab === 'ANALYTICS'} 
                    onClick={() => setActiveTab('ANALYTICS')} 
                    tooltip="Research Analytics"
                />
            </nav>
            <div className="mt-auto">
                <SidebarIcon 
                    icon={Settings} 
                    active={activeTab === 'SETTINGS'} 
                    onClick={() => setActiveTab('SETTINGS')} 
                    tooltip="System Settings"
                />
            </div>
        </aside>
    );
}
