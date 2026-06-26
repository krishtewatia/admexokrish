import { useState } from 'react';
import LeadForm from './components/LeadForm';
import Dashboard from './components/Dashboard';
import { LayoutDashboard, UserPlus } from 'lucide-react';

function App() {
  const [page, setPage] = useState('dashboard');

  return (
    <div className="min-h-screen bg-[#0f0f1a]">
      {/* Navbar */}
      <nav className="border-b border-white/10 bg-[#161625] sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Lead Manager
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setPage('dashboard')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  page === 'dashboard'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <LayoutDashboard size={16} /> Dashboard
              </button>
              <button
                onClick={() => setPage('form')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  page === 'form'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <UserPlus size={16} /> Add Lead
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {page === 'dashboard' ? (
          <Dashboard />
        ) : (
          <LeadForm onSuccess={() => setPage('dashboard')} />
        )}
      </main>
    </div>
  );
}

export default App;
