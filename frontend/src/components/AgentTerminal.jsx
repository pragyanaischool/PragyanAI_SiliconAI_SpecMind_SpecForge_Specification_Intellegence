import React from 'react';
import { Terminal, CheckCircle2 } from 'lucide-react';

export default function AgentTerminal({ logs }) {
  return (
    <div className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-4">
      <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 mb-3 border-b border-obsidian-800 pb-2">
        <Terminal className="h-4 w-4 text-cyanAccent" />
        <span>LangGraph Agent Execution Telemetry</span>
      </div>
      <div className="space-y-2 max-h-80 overflow-y-auto font-mono text-xs">
        {logs.length === 0 ? (
          <span className="text-slate-500">Telemetry idle. Run extraction to view trace.</span>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="flex items-start space-x-2 text-slate-300">
              <CheckCircle2 className="h-3.5 w-3.5 text-cyanAccent mt-0.5 flex-shrink-0" />
              <span>{log}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
