import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000
});

export const api = {
  uploadSpecs: async (formData) => {
    const res = await client.post('/api/spec/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },

  loadDemoContract: async () => {
    const res = await client.post('/api/spec/demo');
    return res.data;
  },

  runExtraction: async (query, groqApiKey) => {
    const res = await client.post('/api/spec/extract', {
      query,
      groq_api_key: groqApiKey
    });
    return res.data;
  },

  getActiveContract: async () => {
    const res = await client.get('/api/contract');
    return res.data;
  },

  addPort: async (portData) => {
    const res = await client.post('/api/contract/port', portData);
    return res.data;
  },

  addCornerCase: async (cornerData) => {
    const res = await client.post('/api/contract/corner-case', cornerData);
    return res.data;
  },

  chatCopilot: async (query, groqApiKey) => {
    const res = await client.post('/api/copilot/chat', {
      query,
      groq_api_key: groqApiKey
    });
    return res.data;
  },

  getDownloadUrl: (endpoint) => `${API_BASE}/api/export/${endpoint}`
};
