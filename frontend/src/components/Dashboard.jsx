import { useState, useEffect } from 'react';
import { getDashboard } from '../api';
import { Users, Mail, Eye, MousePointerClick, TrendingUp, Loader2, AlertCircle } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd'];

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await getDashboard();
      setData(res.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 size={32} className="text-indigo-400 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-lg mx-auto mt-12">
        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-xl">
          <AlertCircle size={16} /> {error}
        </div>
        <button onClick={fetchData} className="mt-4 text-indigo-400 hover:underline text-sm">Retry</button>
      </div>
    );
  }

  if (!data) return null;

  const stats = [
    { label: 'Total Leads', value: data.total_leads, icon: Users, color: 'from-indigo-500 to-indigo-600' },
    { label: 'Emails Sent', value: data.emails_sent, icon: Mail, color: 'from-purple-500 to-purple-600' },
    { label: 'Emails Opened', value: `${data.emails_opened} (${data.open_rate}%)`, icon: Eye, color: 'from-blue-500 to-blue-600' },
    { label: 'Links Clicked', value: `${data.links_clicked} (${data.click_rate}%)`, icon: MousePointerClick, color: 'from-emerald-500 to-emerald-600' },
  ];

  const pieData = [
    { name: 'Opened', value: data.emails_opened },
    { name: 'Unopened', value: Math.max(0, data.emails_sent - data.emails_opened) },
  ];

  const barData = [
    { name: 'Leads', value: data.total_leads },
    { name: 'Sent', value: data.emails_sent },
    { name: 'Opened', value: data.emails_opened },
    { name: 'Clicked', value: data.links_clicked },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Analytics Dashboard</h2>
        <button onClick={fetchData} className="text-sm text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
          <TrendingUp size={14} /> Refresh
        </button>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s) => (
          <div key={s.label} className="bg-[#161625] border border-white/10 rounded-2xl p-5 hover:border-indigo-500/30 transition">
            <div className="flex items-center gap-3 mb-3">
              <div className={`p-2 rounded-xl bg-gradient-to-br ${s.color}`}>
                <s.icon size={18} className="text-white" />
              </div>
              <span className="text-sm text-gray-400">{s.label}</span>
            </div>
            <p className="text-2xl font-bold text-white">{s.value}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Pie Chart */}
        <div className="bg-[#161625] border border-white/10 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Open Rate</h3>
          {data.emails_sent > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} dataKey="value" stroke="none">
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: '#1e1e30', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', color: '#fff' }} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-16">No email data yet</p>
          )}
          <div className="flex justify-center gap-6 mt-2">
            <span className="flex items-center gap-2 text-sm text-gray-400"><span className="w-3 h-3 rounded-full bg-indigo-500 inline-block" /> Opened</span>
            <span className="flex items-center gap-2 text-sm text-gray-400"><span className="w-3 h-3 rounded-full bg-purple-500 inline-block" /> Unopened</span>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="bg-[#161625] border border-white/10 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Funnel Overview</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={barData}>
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 12 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 12 }} />
              <Tooltip contentStyle={{ background: '#1e1e30', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', color: '#fff' }} />
              <Bar dataKey="value" fill="#6366f1" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Leads Table */}
      <div className="bg-[#161625] border border-white/10 rounded-2xl overflow-hidden">
        <div className="px-6 py-4 border-b border-white/10">
          <h3 className="text-lg font-semibold text-white">Recent Leads</h3>
        </div>
        {data.recent_leads.length === 0 ? (
          <p className="text-gray-500 text-center py-12">No leads yet — add one to get started!</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-400 border-b border-white/5">
                  <th className="px-6 py-3 font-medium">Name</th>
                  <th className="px-6 py-3 font-medium">Email</th>
                  <th className="px-6 py-3 font-medium">Company</th>
                  <th className="px-6 py-3 font-medium">Email Sent</th>
                  <th className="px-6 py-3 font-medium">Opened</th>
                  <th className="px-6 py-3 font-medium">Clicked</th>
                  <th className="px-6 py-3 font-medium">Category</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_leads.map((lead) => (
                  <tr key={lead.id} className="border-b border-white/5 hover:bg-white/[0.02] transition">
                    <td className="px-6 py-3 text-white font-medium">{lead.name}</td>
                    <td className="px-6 py-3 text-gray-400">{lead.email}</td>
                    <td className="px-6 py-3 text-gray-400">{lead.company || '—'}</td>
                    <td className="px-6 py-3">{lead.emailSent ? <span className="text-green-400">✓</span> : <span className="text-gray-600">✗</span>}</td>
                    <td className="px-6 py-3">{lead.opened ? <span className="text-green-400">✓</span> : <span className="text-gray-600">✗</span>}</td>
                    <td className="px-6 py-3">{lead.clicked ? <span className="text-green-400">✓</span> : <span className="text-gray-600">✗</span>}</td>
                    <td className="px-6 py-3">
                      {lead.category ? (
                        <span className={`px-2 py-1 rounded-lg text-xs font-medium ${
                          lead.category === 'Hot' ? 'bg-red-500/20 text-red-300' :
                          lead.category === 'Warm' ? 'bg-yellow-500/20 text-yellow-300' :
                          'bg-blue-500/20 text-blue-300'
                        }`}>{lead.category}</span>
                      ) : <span className="text-gray-600">—</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
