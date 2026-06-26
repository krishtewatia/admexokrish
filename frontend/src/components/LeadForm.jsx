import { useState } from 'react';
import { createLead } from '../api';
import { Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

export default function LeadForm({ onSuccess }) {
  const [form, setForm] = useState({ name: '', email: '', phone: '', company: '', requirement: '' });
  const [status, setStatus] = useState('idle'); // idle | loading | success | error
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.email) {
      setError('Name and Email are required');
      setStatus('error');
      return;
    }
    setStatus('loading');
    setError('');
    try {
      await createLead(form);
      setStatus('success');
      setForm({ name: '', email: '', phone: '', company: '', requirement: '' });
      setTimeout(() => onSuccess?.(), 2000);
    } catch (err) {
      setStatus('error');
      const msg = err.response?.data?.detail || err.message || 'Network error';
      setError(msg);
    }
  };

  if (status === 'success') {
    return (
      <div className="max-w-lg mx-auto mt-12 text-center">
        <div className="bg-[#161625] border border-green-500/30 rounded-2xl p-12">
          <CheckCircle size={48} className="text-green-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Lead Submitted!</h2>
          <p className="text-gray-400">Welcome email has been sent. Redirecting to dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6">Capture New Lead</h2>

      {status === 'error' && (
        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-xl mb-4">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-[#161625] border border-white/10 rounded-2xl p-6 space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Name *</label>
          <input name="name" value={form.name} onChange={handleChange} required
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500 transition" placeholder="John Doe" />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Email *</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500 transition" placeholder="john@company.com" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Phone</label>
            <input name="phone" value={form.phone} onChange={handleChange}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500 transition" placeholder="+1-555-0100" />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Company</label>
            <input name="company" value={form.company} onChange={handleChange}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500 transition" placeholder="Acme Corp" />
          </div>
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Requirement</label>
          <textarea name="requirement" value={form.requirement} onChange={handleChange} rows={4}
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500 transition resize-none" placeholder="Describe your requirement..." />
        </div>
        <button type="submit" disabled={status === 'loading'}
          className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold py-3 rounded-xl hover:opacity-90 transition disabled:opacity-50">
          {status === 'loading' ? <><Loader2 size={18} className="animate-spin" /> Submitting...</> : <><Send size={18} /> Submit Lead</>}
        </button>
      </form>
    </div>
  );
}
