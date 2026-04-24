import React from 'react';
import { Bell, Search } from 'lucide-react';

export default function Header() {
  return (
    <header className="h-16 border-b border-border bg-surface flex items-center justify-between px-6 shrink-0 transition-all z-10">
      <div className="flex items-center flex-1">
        <div className="relative w-64 max-w-md hidden md:block">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search resources..."
            className="w-full h-9 bg-background border border-border rounded-md pl-9 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-success/10 text-success px-3 py-1.5 rounded-full border border-success/20">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
          <span className="text-xs font-semibold uppercase tracking-wider">System Operational</span>
        </div>
        
        <button className="relative p-2 text-text-muted hover:text-text hover:bg-background rounded-full transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-danger rounded-full border-2 border-surface"></span>
        </button>
      </div>
    </header>
  );
}
