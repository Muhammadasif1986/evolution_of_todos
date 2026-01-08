'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    setTimeout(() => {
      router.push('/login');
    }, 200);
  };

  const isAuthPage = pathname === '/login' || pathname === '/signup' || pathname === '/';

  if (isAuthPage) {
    return null;
  }

  return (
    <header className="sticky top-0 z-40 backdrop-blur-md bg-white/40 border-b border-white/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo & Navigation */}
          <div className="flex items-center gap-8">
            <Link href="/tasks" className="text-2xl font-bold text-gradient hover:opacity-80 transition-opacity">
              TaskMaster
            </Link>

            <nav className="hidden md:flex items-center gap-1">
              <Link
                href="/tasks"
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                  pathname === '/tasks'
                    ? 'bg-accent-primary/10 text-accent-primary font-semibold'
                    : 'text-gray-700 hover:bg-gray-100/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 1 1 0 000-2H6a6 6 0 100 12h.002a2 2 0 01-1.999-2V7a4 4 0 018 0v2.5a2.5 2.5 0 01-5 0V7a1 1 0 012 0v2.5a.5.5 0 001 0V7a2 2 0 00-2-2h-.5a1 1 0 000 2H6a1 1 0 100-2H4z" clipRule="evenodd" />
                  </svg>
                  Tasks
                </div>
              </Link>
            </nav>
          </div>

          {/* Right Side - User Menu */}
          <div className="flex items-center gap-4">
            {/* User Info */}
            <div className="hidden sm:flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-accent-primary/10">
                <svg className="w-5 h-5 text-accent-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                </svg>
              </div>
            </div>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              disabled={isLoggingOut}
              className="px-4 py-2 rounded-lg text-sm font-medium bg-red-50/50 text-red-700 hover:bg-red-100/50 transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed border border-red-200/50"
            >
              {isLoggingOut ? (
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full border-2 border-red-400 border-t-red-700 animate-spin" />
                  Logout
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                  </svg>
                  Logout
                </span>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-white/20 px-4 py-2 bg-white/20">
        <Link
          href="/tasks"
          className={`block px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
            pathname === '/tasks'
              ? 'bg-accent-primary/10 text-accent-primary font-semibold'
              : 'text-gray-700 hover:bg-gray-100/50'
          }`}
        >
          Tasks
        </Link>
      </div>
    </header>
  );
}