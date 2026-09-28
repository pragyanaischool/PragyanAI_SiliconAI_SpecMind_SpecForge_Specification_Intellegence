import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';

export default function HitlModal({ isOpen, onClose, onAddPort }) {
  const [name, setName] = useState('');
  const [direction, setDirection] = useState('input');
  const [width, setWidth] = useState('[31:0]');
  const [clockDomain, setClockDomain] = useState('clk');
  const [description, setDescription] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name) return;
    onAddPort({
      name,
      direction,
      width,
      clock_domain: clockDomain,
      active_level: 'high',
      description
    });
    setName('');
    setDescription('');
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-obsidian-900 border border-obsidian-700 rounded-xl max-w-md w-full p-5 shadow-2xl">
        <div className="flex justify-between items-center mb-4 border-b border-obsidian-800 pb-2">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <Plus className="h-4 w-4 text-cyanAccent" />
            <span>Human-in-the-Loop Port Override</span>
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="text-slate-400 mb-1 block">Port Identifier</label>
            <input
              type="text"
              placeholder="e.g. s_axis_tready"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-white outline-none focus:border-cyanAccent font-mono"
            />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-slate-400 mb-1 block">Direction</label>
              <select
                value={direction}
                onChange={(e) => setDirection(e.target.value)}
                className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-white outline-none focus:border-cyanAccent"
              >
                <option value="input">Input</option>
                <option value="output">Output</option>
                <option value="inout">Inout</option>
              </select>
            </div>
            <div>
              <label className="text-slate-400 mb-1 block">Bit Width</label>
              <input
                type="text"
                placeholder="[31:0]"
                value={width}
                onChange={(e) => setWidth(e.target.value)}
                className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-white outline-none focus:border-cyanAccent font-mono"
              />
            </div>
          </div>
          <div>
            <label className="text-slate-400 mb-1 block">Clock Domain</label>
            <input
              type="text"
              value={clockDomain}
              onChange={(e) => setClockDomain(e.target.value)}
              className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-white outline-none focus:border-cyanAccent font-mono"
            />
          </div>
          <div>
            <label className="text-slate-400 mb-1 block">Functional Description</label>
            <textarea
              rows="2"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-white outline-none focus:border-cyanAccent"
              placeholder="Specifies function..."
            />
          </div>

          <div className="flex justify-end space-x-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 rounded bg-obsidian-800 text-slate-300 hover:bg-obsidian-700"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-3 py-1.5 rounded bg-cyanAccent text-obsidian-950 font-bold hover:bg-cyan-300 transition"
            >
              Inject Port
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
