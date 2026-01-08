'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed. Please try again.');
        setIsLoading(false);
        return;
      }

      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }
      router.push('/tasks');
    } catch (err: any) {
      setError(err.message || 'Invalid credentials. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-purple-50 flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent-primary/10 rounded-full blur-3xl -z-10" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-accent-secondary/10 rounded-full blur-3xl -z-10" />

      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in-up">
          <Link href="/" className="inline-block mb-6">
            <div className="text-3xl font-bold text-gradient">TaskMaster</div>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
          <p className="text-gray-600">Sign in to access your tasks</p>
        </div>

        {/* Login Card */}
        <div className="card glass-dark p-8 backdrop-blur-xl border border-white/20 animate-slide-up">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Error Alert */}
            {error && (
              <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg flex items-start gap-3 animate-slide-down">
                <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium text-red-800">{error}</span>
              </div>
            )}

            {/* Email Field */}
            <div className="form-group">
              <label htmlFor="email" className="form-label text-gray-800">
                Email Address
              </label>
              <div className={`relative transition-all duration-300 ${focusedField === 'email' ? 'ring-2 ring-accent-primary rounded-lg' : ''}`}>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onFocus={() => setFocusedField('email')}
                  onBlur={() => setFocusedField(null)}
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="form-group">
              <label htmlFor="password" className="form-label text-gray-800">
                Password
              </label>
              <div className={`relative transition-all duration-300 ${focusedField === 'password' ? 'ring-2 ring-accent-primary rounded-lg' : ''}`}>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
                />
              </div>
            </div>

            {/* Remember & Forgot */}
            <div className="flex items-center justify-between pt-2">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input
                  type="checkbox"
                  className="w-4 h-4 rounded border-gray-300 text-accent-primary cursor-pointer"
                  defaultChecked
                />
                <span className="text-sm text-gray-700 group-hover:text-gray-900">Remember me</span>
              </label>
              <Link href="/signup" className="link text-sm">
                Need an account?
              </Link>
            </div>

            {/* Sign In Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full mt-6 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="spinner w-4 h-4" />
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="divider my-6">
            <span className="divider-text">Don't have an account?</span>
          </div>

          {/* Sign Up Link */}
          <Link
            href="/signup"
            className="btn-secondary w-full text-center"
          >
            Create Account
          </Link>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-600">
          <p>Build by Muhammad Asif using <span className="text-accent-primary font-medium">Next.js</span></p>
        </div>
      </div>
    </div>
  );
}