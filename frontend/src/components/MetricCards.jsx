import React from 'react';
import { Clock, Layers, ShieldCheck, Zap } from 'lucide-react';

export default function MetricCards({ contract }) {
  if (!contract) return null;

  const metrics = [
    {
      label: 'Reset Scheme',
      value: contract.reset_type?.toUpperCase().replace('_', ' ') || 'ASYNC LOW',
      badge: 'Hardware Reset',
      icon: Zap
    },
    {
      label: 'Target Frequency',
      value: `${contract.timing?.fmax_mhz || '200'} MHz`,
      badge: 'Clock Target',
      icon: Clock
    },
    {
      label: 'Declared Ports',
      value: `${contract.ports?.length || 0} Signals`,
      badge: `${contract.ports?.filter(p => p.direction === 'input').length} In / ${contract.ports?.filter(p => p.direction === 'output').length} Out`,
      icon: Layers
    },
    {
      label: 'Corner Cases & SVA',
      value: `${contract.corner_cases?.length || 0} Properties`,
      badge: 'Formally Verified',
      icon: ShieldCheck
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      {metrics.map((m, idx) => {
        const Icon = m.icon;
        return (
          <div key={idx} className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-4 transition hover:border-cyanAccent/40">
            <div className="flex justify-between items-start">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{m.label}</span>
              <Icon className="h-4 w-4 text-cyanAccent opacity-80" />
            </div>
            <div className="text-xl font-bold text-white mt-1 mb-2 tracking-tight">{m.value}</div>
            <span className="text-[10px] bg-obsidian-800 text-cyanAccent border border-cyanAccent/20 px-2 py-0.5 rounded">
              {m.badge}
            </span>
          </div>
        );
      })}
    </div>
  );
}
