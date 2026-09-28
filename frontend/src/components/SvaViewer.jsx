import React from 'react';
import { AlertCircle, Code } from 'lucide-react';

export default function SvaViewer({ cornerCases }) {
  if (!cornerCases || cornerCases.length === 0) {
    return <div className="p-4 text-sm text-slate-500">No corner cases identified.</div>;
  }

  return (
    <div className="space-y-4">
      {cornerCases.map((cc, idx) => (
        <div key={idx} className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-4 transition hover:border-obsidian-700">
          <div className="flex items-center space-x-2 text-cyanAccent text-xs font-bold mb-1.5">
            <AlertCircle className="h-4 w-4 text-amber-400" />
            <span>{cc.scenario_id}: {cc.title}</span>
          </div>
          <p className="text-xs text-slate-300 mb-2">{cc.hazard_description}</p>
          <div className="text-[11px] text-slate-400 mb-2">
            <span className="font-semibold text-slate-300">Required RTL Action:</span> {cc.expected_hardware_behavior}
          </div>
          <div className="bg-obsidian-950 p-3 rounded-lg border border-obsidian-800 font-mono text-[11px] text-emerald-400 overflow-x-auto">
            <div className="flex items-center space-x-1 text-[10px] text-slate-500 mb-1">
              <Code className="h-3 w-3" />
              <span>SystemVerilog Assertion (SVA)</span>
            </div>
            <pre className="whitespace-pre">{cc.sva_property}</pre>
          </div>
        </div>
      ))}
    </div>
  );
}
