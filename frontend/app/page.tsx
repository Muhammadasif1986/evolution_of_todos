'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated and redirect accordingly
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          // Verify token is still valid by trying to fetch tasks
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          if (response.ok) {
            router.push('/tasks');
            return;
          }
        }
      } catch (err) {
        console.log('Not authenticated, showing landing page');
      }
    };

    checkAuth();
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-purple-50 flex flex-col">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-sm bg-white/40 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="text-2xl font-bold text-gradient">TaskMaster</div>
            <div className="flex gap-4">
              <Link
                href="/login"
                className="px-4 py-2 text-gray-700 hover:text-accent-primary transition-colors font-medium"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="btn-primary"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="flex-1 flex items-center justify-center px-4 pt-20 pb-12">
        <div className="max-w-5xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-center animate-fade-in-up">
          {/* Left Content */}
          <div className="flex flex-col justify-center">
            <div className="mb-6 inline-flex items-center px-3 py-1.5 bg-blue-100 text-accent-primary rounded-full text-sm font-medium w-fit">
              Welcome to TaskMaster
            </div>

            <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6">
              <span className="block text-gray-900">Manage Tasks</span>
              <span className="block text-gradient mt-2">With Style & Ease</span>
            </h1>

            <p className="text-xl text-gray-600 mb-8 leading-relaxed max-w-lg">
              Stay organized and productive. Muhammad Asif's modern task management application built with Next.js and React. Simple, fast, and beautifully designed.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <Link
                href="/signup"
                className="btn-primary text-center"
              >
                Get Started Free
              </Link>
              <Link
                href="/login"
                className="btn-secondary text-center"
              >
                Sign In
              </Link>
            </div>

            {/* Features List */}
            <div className="space-y-3">
              {[
                'Create and manage unlimited tasks',
                'Real-time synchronization',
                'Beautiful, intuitive interface',
              ].map((feature, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-accent-primary/20 flex items-center justify-center">
                    <svg className="w-4 h-4 text-accent-primary" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 font-medium">{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right - Illustration/Stats */}
          <div className="hidden md:flex flex-col items-center justify-center">
            <div className="relative w-full h-96">
              {/* Glass card with gradient */}
              <div className="absolute inset-0 glass rounded-3xl overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-primary/10 to-accent-secondary/10" />

                {/* Animated elements */}
                <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-accent-primary/20 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-accent-secondary/20 rounded-full blur-3xl animate-pulse animation-delay-2" />

                {/* Content */}
                <div className="relative h-full flex flex-col items-center justify-center p-8">
                  <div className="text-center">
                    <div className="text-5xl font-bold text-gradient mb-2">100+</div>
                    <div className="text-gray-600 font-medium mb-8">Tasks Created</div>

                    <div className="space-y-3">
                      {[
                        { label: 'Active Users', value: '5K+' },
                        { label: 'Completed Tasks', value: '50K+' },
                        { label: 'Uptime', value: '99.9%' },
                      ].map((stat, idx) => (
                        <div key={idx} className="text-sm text-gray-600">
                          <div className="font-semibold text-accent-primary">{stat.value}</div>
                          <div>{stat.label}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-white/20 bg-white/30 backdrop-blur-sm py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-600">
          <p>Built by Muhammad Asif using Next.js, React, and TypeScript</p>
        </div>
      </div>
    </div>
  );
}