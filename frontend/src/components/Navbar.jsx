import React from 'react';
import { Cpu, FileCode2, Terminal, ShieldAlert } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, activeModule }) {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: Cpu },
    { id: 'interfaces', label: 'Ports & Timing', icon: FileCode2 },
    { id: 'sva', label: 'Corner Cases & SVA', icon: ShieldAlert },
    { id: 'copilot', label: 'AI Copilot', icon: Terminal },
  ];

  return (
    <header className="border-b border-obsidian-800 bg-obsidian-900/80 backdrop-blur-md sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="h-8 w-8 rounded-lg bg-cyan-500/10 border border-cyanAccent flex items-center justify-center text-cyanAccent shadow-lg shadow-cyan-500/10">
          <Cpu className="h-5 w-5" />
        </div>
        <div>
          <span className="font-extrabold tracking-wider text-white text-base">PRAGYANAI</span>
          <span className="text-cyanAccent text-base font-extrabold ml-1.5">SPECFORGE</span>
          <span className="ml-3 px-2 py-0.5 rounded text-[10px] bg-obsidian-800 text-slate-400 border border-obsidian-700">v2.0</span>
        </div>
      </div>

      <nav className="flex space-x-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-obsidian-800 text-cyanAccent border-b-2 border-cyanAccent shadow-inner'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-obsidian-850'
              }`}
            >
              <Icon className="h-3.5 w-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="flex items-center space-x-3">
        {activeModule && (
          <div className="px-3 py-1 rounded bg-cyan-950/60 border border-cyanAccent/30 text-cyanAccent text-xs font-medium">
            Active: <span className="font-bold">{activeModule}</span>
          </div>
        )}
      </div>
    </header>
  );
}
