import React from 'react';

function DashboardLayout({ sidebar, children }) {
    return (
        <div className="flex bg-zinc-50 h-screen w-screen overflow-hidden font-sans text-zinc-900 antialiased">
            {sidebar}
            <main className="flex-1 flex flex-col h-full overflow-hidden">
                <header className="h-16 bg-white border-b border-zinc-200/60 flex items-center px-8 justify-between shrink-0">
                    <div className="flex items-center gap-3">
                        <span className="relative flex h-2.5 w-2.5">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                        <span className="text-sm font-medium text-zinc-600 tracking-wide">Fleet Controller Active</span>
                    </div>
                </header>
                
                {/* Scrollable Container with tight bounds */}
                <div className="flex-1 overflow-auto p-10">
                    {children}
                </div>
            </main>
        </div>
    );
}

export default DashboardLayout;
