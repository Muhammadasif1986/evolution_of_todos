'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    // Remove token from localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    // Redirect to login after logout
    router.push('/login');
  };

  // Determine if we're on an auth page (login/signup)
  const isAuthPage = pathname === '/login' || pathname === '/signup';

  if (isAuthPage) {
    return null; // Don't show header on auth pages
  }

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/tasks" className="text-xl font-bold text-indigo-600">
              TaskMaster
            </Link>
            <nav className="ml-6 flex space-x-4">
              <Link
                href="/tasks"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/tasks'
                    ? 'bg-indigo-100 text-indigo-700'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Tasks
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            <button
              onClick={handleLogout}
              className="text-sm font-medium text-gray-500 hover:text-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}