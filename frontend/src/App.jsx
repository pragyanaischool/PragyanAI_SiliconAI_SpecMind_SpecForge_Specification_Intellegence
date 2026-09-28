import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import MetricCards from './components/MetricCards';
import PortTable from './components/PortTable';
import SvaViewer from './components/SvaViewer';
import AgentTerminal from './components/AgentTerminal';
import HitlModal from './components/HitlModal';
import { api } from './services/api';
import { UploadCloud, Play, Download, Send, Plus, RefreshCw } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [contract, setContract] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [query, setQuery] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [agentLogs, setAgentLogs] = useState([]);
  const [isHitlOpen, setIsHitlOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getActiveContract()
      .then(data => setContract(data))
      .catch(() => {});
  }, []);

  const handleFileUpload = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setLoading(true);
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    if (apiKey) formData.append('groq_api_key', apiKey);

    try {
      const res = await api.uploadSpecs(formData);
      setAgentLogs(prev => [...prev, `[Document Ingestion]: ${res.message}`]);
    } catch (err) {
      alert(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDemo = async () => {
    setLoading(true);
    try {
      const res = await api.loadDemoContract();
      setContract(res.contract);
      setAgentLogs(prev => [...prev, `[Demo Engine]: Loaded reference ${res.contract.module_name}`]);
    } finally {
      setLoading(false);
    }
  };

  const handleRunExtraction = async () => {
    if (!query) return;
    setLoading(true);
    setAgentLogs(prev => [...prev, `[Multi-Agent]: Starting extraction for '${query}'`]);

    try {
      const res = await api.runExtraction(query, apiKey);
      setContract(res.contract);
      setAgentLogs(prev => [
        ...prev,
        `[Spec Analyst]: Ports, FSMs, and clock crossings mined`,
        `[Synthesizer]: Pydantic contract verified`,
        `[DV Intelligence]: SystemVerilog Assertions compiled`
      ]);
    } catch (err) {
      alert(err.response?.data?.detail || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async () => {
    if (!chatInput) return;
    const userMsg = chatInput;
    setChatMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput('');

    try {
      const res = await api.chatCopilot(userMsg, apiKey);
      setChatMessages(prev => [...prev, { role: 'assistant', text: res.reply }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'assistant', text: 'Error contacting Spec Q&A agent.' }]);
    }
  };

  return (
    <div className="min-h-screen bg-obsidian-950 text-slate-100 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} activeModule={contract?.module_name} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="space-y-4">
          <div className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-4 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Settings & Ingestion</h2>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Groq API Key</label>
              <input
                type="password"
                placeholder="gsk_..."
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full bg-obsidian-950 border border-obsidian-800 rounded p-2 text-xs text-white outline-none focus:border-cyanAccent"
              />
            </div>

            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Upload Specification (.pdf, .txt, .docx)</label>
              <label className="border-2 border-dashed border-obsidian-800 hover:border-cyanAccent/50 rounded-lg p-4 flex flex-col items-center justify-center cursor-pointer transition">
                <UploadCloud className="h-6 w-6 text-cyanAccent mb-1 opacity-80" />
                <span className="text-[11px] text-slate-300">Choose Datasheet</span>
                <input type="file" multiple onChange={handleFileUpload} className="hidden" />
              </label>
            </div>

            <button
              onClick={handleLoadDemo}
              disabled={loading}
              className="w-full py-2 rounded bg-obsidian-800 hover:bg-obsidian-750 text-xs font-semibold text-slate-300 flex items-center justify-center space-x-1.5 transition"
            >
              <RefreshCw className="h-3.5 w-3.5 text-cyanAccent" />
              <span>Load AXI-FIFO Demo</span>
            </button>
          </div>

          <AgentTerminal logs={agentLogs} />
        </div>

        <div className="lg:col-span-3 space-y-4">
          <div className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-2.5 flex items-center space-x-2">
            <input
              type="text"
              placeholder="e.g. Extract the complete hardware contract for an AXI4-Stream FIFO..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1 bg-transparent px-3 py-1 text-xs text-white outline-none placeholder-slate-500 font-mono"
            />
            <button
              onClick={handleRunExtraction}
              disabled={loading}
              className="px-4 py-2 rounded-lg bg-cyanAccent text-obsidian-950 font-bold text-xs flex items-center space-x-1.5 hover:bg-cyan-300 transition"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>{loading ? 'Synthesizing...' : 'Synthesize'}</span>
            </button>
          </div>

          <MetricCards contract={contract} />

          {activeTab === 'overview' && (
            <div className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-5 space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-sm font-bold text-white">Micro-Architecture Executive Summary</h3>
                <button
                  onClick={() => setIsHitlOpen(true)}
                  className="px-2.5 py-1 bg-obsidian-800 text-cyanAccent text-xs rounded flex items-center space-x-1 hover:bg-obsidian-750"
                >
                  <Plus className="h-3.5 w-3.5" />
                  <span>Override Port</span>
                </button>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {contract?.description || 'No specification loaded. Upload a document or load the demo above.'}
              </p>

              <div className="pt-2 flex flex-wrap gap-2">
                <a
                  href={api.getDownloadUrl('json')}
                  download
                  className="px-3 py-1.5 bg-obsidian-950 border border-obsidian-800 text-cyanAccent text-xs rounded hover:border-cyanAccent transition flex items-center space-x-1.5"
                >
                  <Download className="h-3.5 w-3.5" />
                  <span>Download JSON Contract</span>
                </a>
                <a
                  href={api.getDownloadUrl('markdown')}
                  download
                  className="px-3 py-1.5 bg-obsidian-950 border border-obsidian-800 text-slate-300 text-xs rounded hover:border-slate-500 transition flex items-center space-x-1.5"
                >
                  <Download className="h-3.5 w-3.5" />
                  <span>Download MAS Doc (.md)</span>
                </a>
                <a
                  href={api.getDownloadUrl('sva')}
                  download
                  className="px-3 py-1.5 bg-obsidian-950 border border-obsidian-800 text-emerald-400 text-xs rounded hover:border-emerald-500 transition flex items-center space-x-1.5"
                >
                  <Download className="h-3.5 w-3.5" />
                  <span>Download SVA Bind (.sv)</span>
                </a>
              </div>
            </div>
          )}

          {activeTab === 'interfaces' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Interface Ports</h3>
                <button
                  onClick={() => setIsHitlOpen(true)}
                  className="px-2.5 py-1 bg-cyanAccent text-obsidian-950 font-bold text-xs rounded flex items-center space-x-1"
                >
                  <Plus className="h-3.5 w-3.5" />
                  <span>Add Port</span>
                </button>
              </div>
              <PortTable ports={contract?.ports} />
            </div>
          )}

          {activeTab === 'sva' && (
            <div className="space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Corner Cases & Assertions</h3>
              <SvaViewer cornerCases={contract?.corner_cases} />
            </div>
          )}

          {activeTab === 'copilot' && (
            <div className="bg-obsidian-900 border border-obsidian-800 rounded-xl p-4 flex flex-col h-[500px]">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Spec Q&A Interactive Copilot</h3>
              <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-3">
                {chatMessages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg text-xs leading-relaxed ${
                      m.role === 'user'
                        ? 'bg-obsidian-800 ml-8 text-white'
                        : 'bg-obsidian-950 mr-8 text-slate-300 border border-obsidian-800'
                    }`}
                  >
                    <span className="font-bold block mb-1 text-[10px] text-cyanAccent uppercase">
                      {m.role === 'user' ? 'Lead Designer' : 'Spec Co-Pilot'}
                    </span>
                    {m.text}
                  </div>
                ))}
              </div>
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Ask a technical question about the spec..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleChat()}
                  className="flex-1 bg-obsidian-950 border border-obsidian-800 rounded p-2 text-xs text-white outline-none focus:border-cyanAccent"
                />
                <button
                  onClick={handleChat}
                  className="px-3 bg-cyanAccent text-obsidian-950 rounded font-bold hover:bg-cyan-300 transition"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      <HitlModal
        isOpen={isHitlOpen}
        onClose={() => setIsHitlOpen(false)}
        onAddPort={async (newPort) => {
          const res = await api.addPort(newPort);
          setContract(res.contract);
        }}
      />
    </div>
  );
}
