'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const [passwordStrength, setPasswordStrength] = useState<'weak' | 'medium' | 'strong' | null>(null);
  const router = useRouter();

  const calculatePasswordStrength = (pwd: string) => {
    if (pwd.length < 8) return 'weak';
    if (pwd.length < 12) return 'medium';
    return 'strong';
  };

  const handlePasswordChange = (pwd: string) => {
    setPassword(pwd);
    if (pwd) {
      setPasswordStrength(calculatePasswordStrength(pwd));
    } else {
      setPasswordStrength(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          username: name,
          first_name: name.split(' ')[0] || name,
          last_name: name.split(' ').slice(1).join(' ') || '',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.detail || 'Signup failed. Please try again.');
        setIsLoading(false);
        return;
      }

      setIsLoading(false);
      router.push('/login');
    } catch (err: any) {
      setError(err.message || 'An error occurred during signup. Please try again.');
      setIsLoading(false);
    }
  };

  const strengthColors = {
    weak: 'bg-red-500',
    medium: 'bg-yellow-500',
    strong: 'bg-green-500',
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h1>
          <p className="text-gray-600">Join TaskMaster today and start managing tasks like a pro</p>
        </div>

        {/* Signup Card */}
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

            {/* Full Name Field */}
            <div className="form-group">
              <label htmlFor="name" className="form-label text-gray-800">
                Full Name
              </label>
              <div className={`relative transition-all duration-300 ${focusedField === 'name' ? 'ring-2 ring-accent-primary rounded-lg' : ''}`}>
                <input
                  id="name"
                  name="name"
                  type="text"
                  autoComplete="name"
                  required
                  className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                  placeholder="John Doe"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onFocus={() => setFocusedField('name')}
                  onBlur={() => setFocusedField(null)}
                />
              </div>
            </div>

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
              <div className="flex items-center justify-between mb-2">
                <label htmlFor="password" className="form-label text-gray-800 m-0">
                  Password
                </label>
                {passwordStrength && (
                  <span className={`text-xs font-medium ${
                    passwordStrength === 'weak' ? 'text-red-600' :
                    passwordStrength === 'medium' ? 'text-yellow-600' :
                    'text-green-600'
                  }`}>
                    {passwordStrength.charAt(0).toUpperCase() + passwordStrength.slice(1)} strength
                  </span>
                )}
              </div>
              <div className={`relative transition-all duration-300 ${focusedField === 'password' ? 'ring-2 ring-accent-primary rounded-lg' : ''}`}>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => handlePasswordChange(e.target.value)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
                />
              </div>
              {password && (
                <div className="mt-2 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-300 ${
                      passwordStrength === 'weak' ? 'w-1/3 bg-red-500' :
                      passwordStrength === 'medium' ? 'w-2/3 bg-yellow-500' :
                      'w-full bg-green-500'
                    }`}
                  />
                </div>
              )}
              <p className="text-xs text-gray-500 mt-2">
                At least 8 characters with a mix of letters, numbers, and symbols
              </p>
            </div>

            {/* Confirm Password Field */}
            <div className="form-group">
              <label htmlFor="confirm-password" className="form-label text-gray-800">
                Confirm Password
              </label>
              <div className={`relative transition-all duration-300 ${focusedField === 'confirm' ? 'ring-2 ring-accent-primary rounded-lg' : ''}`}>
                <input
                  id="confirm-password"
                  name="confirm-password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  onFocus={() => setFocusedField('confirm')}
                  onBlur={() => setFocusedField(null)}
                />
              </div>
              {password && confirmPassword && password === confirmPassword && (
                <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Passwords match
                </p>
              )}
            </div>

            {/* Terms */}
            <label className="flex items-start gap-2 cursor-pointer group">
              <input
                type="checkbox"
                className="w-4 h-4 rounded border-gray-300 text-accent-primary cursor-pointer mt-0.5"
                required
              />
              <span className="text-xs text-gray-700 group-hover:text-gray-900">
                I agree to the Terms of Service and Privacy Policy
              </span>
            </label>

            {/* Sign Up Button */}
            <button
              type="submit"
              disabled={isLoading || password !== confirmPassword}
              className="btn-primary w-full mt-6 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="spinner w-4 h-4" />
                  Creating Account...
                </>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="divider my-6">
            <span className="divider-text">Already have an account?</span>
          </div>

          {/* Sign In Link */}
          <Link
            href="/login"
            className="btn-secondary w-full text-center"
          >
            Sign In
          </Link>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-xs text-gray-600">
          <p>Build by Muhammad Asif using <span className="text-accent-primary font-medium">Next.js</span></p>
        </div>
      </div>
    </div>
  );
}