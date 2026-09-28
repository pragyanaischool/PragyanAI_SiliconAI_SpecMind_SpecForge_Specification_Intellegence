import React from 'react';

export default function PortTable({ ports }) {
  if (!ports || ports.length === 0) {
    return <div className="p-4 text-sm text-slate-500">No ports defined in contract.</div>;
  }

  return (
    <div className="overflow-x-auto border border-obsidian-800 rounded-xl bg-obsidian-900">
      <table className="w-full text-left text-xs">
        <thead className="bg-obsidian-850 text-slate-400 uppercase text-[10px] tracking-wider border-b border-obsidian-800">
          <tr>
            <th className="py-3 px-4">Port Identifier</th>
            <th className="py-3 px-4">Direction</th>
            <th className="py-3 px-4">Bit Width</th>
            <th className="py-3 px-4">Domain</th>
            <th className="py-3 px-4">Active</th>
            <th className="py-3 px-4">Functional Purpose</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-obsidian-800/60 font-mono text-slate-300">
          {ports.map((port, idx) => (
            <tr key={idx} className="hover:bg-obsidian-800/40 transition">
              <td className="py-2.5 px-4 font-bold text-white flex items-center space-x-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-cyanAccent"></span>
                <span>{port.name}</span>
              </td>
              <td className="py-2.5 px-4">
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  port.direction === 'input'
                    ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                }`}>
                  {port.direction.toUpperCase()}
                </span>
              </td>
              <td className="py-2.5 px-4 text-cyanAccent">{port.width}</td>
              <td className="py-2.5 px-4 text-slate-400">{port.clock_domain}</td>
              <td className="py-2.5 px-4 text-slate-400">{port.active_level}</td>
              <td className="py-2.5 px-4 text-slate-400 truncate max-w-xs">{port.description || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
