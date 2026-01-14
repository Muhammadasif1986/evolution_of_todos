# Component Patterns & Usage Guide

This guide demonstrates how to use the modern design system components and patterns in your code.

## Quick Start

### Import Global Styles
Global styles are automatically included via `app/layout.tsx`:
```tsx
import '@/globals.css';
```

### Use Tailwind Classes
All examples use Tailwind CSS with custom extensions:
```tsx
<div className="btn-primary">Button</div>
```

---

## Button Patterns

### Primary Button
Used for main actions and CTAs.

```tsx
<button className="btn-primary">
  Get Started
</button>

// With icon
<button className="btn-primary flex items-center gap-2">
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="..." />
  </svg>
  Create Task
</button>

// Disabled state
<button className="btn-primary" disabled>
  Saving...
</button>
```

**Classes**: `px-4 py-2.5 rounded-lg font-medium bg-gradient-primary text-white shadow-lg hover:shadow-glow-lg`

### Secondary Button
For alternative actions and less emphasis.

```tsx
<button className="btn-secondary">
  Sign In
</button>

// With loading state
<button className="btn-secondary" disabled>
  <span className="flex items-center gap-2">
    <div className="spinner w-4 h-4" />
    Loading...
  </span>
</button>
```

**Classes**: `px-4 py-2.5 rounded-lg font-medium bg-white text-accent-primary border-2 border-accent-primary`

### Outline Button
For tertiary actions and cancellations.

```tsx
<button className="btn-outline">
  Cancel
</button>

// Full width
<button className="btn-outline w-full">
  Cancel
</button>
```

**Classes**: `px-4 py-2.5 rounded-lg font-medium bg-transparent border-2 border-gray-300 text-gray-700`

### Icon-Only Buttons
For compact toolbars and action menus.

```tsx
<button className="p-2 hover:bg-blue-100/50 rounded-lg transition-colors text-blue-600">
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="..." />
  </svg>
</button>

// Red variant for delete
<button className="p-2 hover:bg-red-100/50 rounded-lg transition-colors text-red-600">
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="..." />
  </svg>
</button>
```

---

## Form Patterns

### Basic Input
```tsx
<div className="form-group">
  <label htmlFor="email" className="form-label">
    Email Address
  </label>
  <input
    id="email"
    type="email"
    className="input-base"
    placeholder="you@example.com"
  />
</div>
```

### Input with Focus Ring
```tsx
<div className={`transition-all duration-300 ${
  focusedField === 'email' ? 'ring-2 ring-accent-primary rounded-lg' : ''
}`}>
  <input
    className="input-base"
    onFocus={() => setFocusedField('email')}
    onBlur={() => setFocusedField(null)}
  />
</div>
```

### Input with Error
```tsx
<div className="form-group">
  <label htmlFor="password" className="form-label">
    Password
  </label>
  <input
    id="password"
    type="password"
    className="input-base input-error"
    placeholder="••••••••"
  />
  {error && (
    <p className="text-error text-sm mt-1">{error}</p>
  )}
</div>
```

### Password Strength Indicator
```tsx
const [password, setPassword] = useState('');
const [strength, setStrength] = useState<'weak' | 'medium' | 'strong' | null>(null);

const calculateStrength = (pwd: string) => {
  if (pwd.length < 8) return 'weak';
  if (pwd.length < 12) return 'medium';
  return 'strong';
};

<div className="form-group">
  <div className="flex items-center justify-between mb-2">
    <label htmlFor="password" className="form-label m-0">
      Password
    </label>
    {strength && (
      <span className={`text-xs font-medium ${
        strength === 'weak' ? 'text-red-600' :
        strength === 'medium' ? 'text-yellow-600' :
        'text-green-600'
      }`}>
        {strength.charAt(0).toUpperCase() + strength.slice(1)} strength
      </span>
    )}
  </div>
  <input
    id="password"
    type="password"
    className="input-base"
    onChange={(e) => {
      setPassword(e.target.value);
      setStrength(calculateStrength(e.target.value));
    }}
  />
  {password && (
    <div className="mt-2 h-1.5 bg-gray-200 rounded-full overflow-hidden">
      <div
        className={`h-full transition-all duration-300 ${
          strength === 'weak' ? 'w-1/3 bg-red-500' :
          strength === 'medium' ? 'w-2/3 bg-yellow-500' :
          'w-full bg-green-500'
        }`}
      />
    </div>
  )}
</div>
```

### Checkbox
```tsx
<label className="flex items-center gap-2 cursor-pointer">
  <input
    type="checkbox"
    className="w-4 h-4 rounded border-gray-300 text-accent-primary cursor-pointer"
  />
  <span className="text-sm text-gray-700">Remember me</span>
</label>
```

### Textarea
```tsx
<div className="form-group">
  <label htmlFor="description" className="form-label">
    Description
  </label>
  <textarea
    id="description"
    rows={3}
    className="input-base resize-none"
    placeholder="Add details..."
  />
</div>
```

---

## Card Patterns

### Standard Card
```tsx
<div className="card">
  <h3 className="text-lg font-semibold text-gray-900 mb-2">
    Card Title
  </h3>
  <p className="text-gray-600">
    Card content goes here.
  </p>
</div>
```

### Glassmorphic Card
```tsx
<div className="card-glass backdrop-blur-xl border border-white/20">
  <h3 className="text-lg font-semibold text-gray-900 mb-2">
    Glass Card Title
  </h3>
  <p className="text-gray-600">
    Card content with glassmorphism effect.
  </p>
</div>
```

### Card with Hover Effect
```tsx
<div className="card glass-dark backdrop-blur-xl border border-white/20 hover:shadow-glow-lg transition-all duration-300">
  <h3 className="text-lg font-semibold mb-2">
    Interactive Card
  </h3>
  <p className="text-gray-600">
    Hovers with glow effect.
  </p>
</div>
```

### Task Item Card
```tsx
<div className="card glass-dark backdrop-blur-xl border border-white/20 hover:shadow-glow-lg">
  <div className="flex items-start gap-4">
    <input
      type="checkbox"
      className="w-5 h-5 text-accent-primary border-gray-300 rounded-lg cursor-pointer mt-1 accent-accent-primary"
    />
    <div className="flex-1">
      <p className="text-base font-semibold text-gray-900">
        Task Title
      </p>
      <p className="text-sm text-gray-600 mt-1">
        Task description
      </p>
    </div>
    <div className="flex items-center gap-2 flex-shrink-0">
      <span className="badge-success">
        Completed
      </span>
      <button className="p-2 hover:bg-blue-100/50 rounded-lg transition-colors text-blue-600">
        Edit
      </button>
      <button className="p-2 hover:bg-red-100/50 rounded-lg transition-colors text-red-600">
        Delete
      </button>
    </div>
  </div>
</div>
```

---

## Alert & Status Patterns

### Error Alert
```tsx
<div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg flex items-start gap-3">
  <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
  </svg>
  <span className="text-sm font-medium text-red-800">
    Error message here
  </span>
</div>
```

### Success Alert
```tsx
<div className="p-4 bg-green-50 border-2 border-green-200 rounded-lg flex items-start gap-3">
  <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
  </svg>
  <span className="text-sm font-medium text-green-800">
    Success message here
  </span>
</div>
```

### Badge Components
```tsx
// Success badge
<span className="badge-success">
  Completed
</span>

// Warning badge
<span className="badge-warning">
  Pending
</span>

// Error badge
<span className="badge-error">
  Failed
</span>
```

---

## Loading & Empty States

### Spinner
```tsx
<div className="spinner" />

// In button
<button className="btn-primary flex items-center justify-center gap-2">
  <div className="spinner w-4 h-4" />
  Loading...
</button>
```

### Skeleton Loader
```tsx
<div className="space-y-4">
  <div className="skeleton h-4 w-3/4" />
  <div className="skeleton h-4 w-full" />
  <div className="skeleton h-4 w-2/3" />
</div>
```

### Empty State
```tsx
<div className="card glass-dark backdrop-blur-xl border border-white/20 text-center py-16">
  <div className="flex justify-center mb-4">
    <div className="w-16 h-16 rounded-full bg-accent-primary/10 flex items-center justify-center">
      <svg className="w-8 h-8 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
    </div>
  </div>
  <p className="text-lg font-medium text-gray-700 mb-2">No tasks yet</p>
  <p className="text-gray-500 mb-6">Create your first task to get started</p>
  <button className="btn-primary inline-flex">
    Create Task
  </button>
</div>
```

---

## Typography Patterns

### Page Title
```tsx
<h1 className="text-4xl font-bold mb-2">
  <span className="text-gray-900">My Tasks</span>
</h1>
<p className="text-gray-600 text-lg">
  You have 5 tasks • 3 completed
</p>
```

### Gradient Text
```tsx
<h1 className="text-3xl font-bold text-gradient">
  TaskMaster
</h1>
```

### Muted Text
```tsx
<p className="text-muted">
  This is secondary text
</p>
```

### Error Text
```tsx
<p className="text-error">
  An error occurred
</p>
```

---

## Layout Patterns

### Hero Section
```tsx
<div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-purple-50 flex items-center">
  <div className="max-w-5xl mx-auto px-4 py-12">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
      {/* Content */}
      {/* Stats/Image */}
    </div>
  </div>
</div>
```

### Two-Column Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div className="card">Column 1</div>
  <div className="card">Column 2</div>
</div>
```

### Three-Column Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div className="card">Column 1</div>
  <div className="card">Column 2</div>
  <div className="card">Column 3</div>
</div>
```

### Centered Container
```tsx
<div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
  Content
</div>
```

---

## Animation Patterns

### Fade In on Load
```tsx
<div className="animate-fade-in-up">
  Content appears with fade and slide effect
</div>
```

### Staggered List Items
```tsx
{items.map((item, index) => (
  <div
    key={item.id}
    className="card animate-slide-up"
    style={{ animationDelay: `${index * 50}ms` }}
  >
    {item.name}
  </div>
))}
```

### Error Animation
```tsx
{error && (
  <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg animate-slide-down">
    {error}
  </div>
)}
```

### Scale In Effect
```tsx
<form className="card animate-scale-in">
  Form content
</form>
```

---

## Responsive Patterns

### Mobile-First
```tsx
<div className="text-sm md:text-base lg:text-lg">
  Text scales with screen size
</div>
```

### Hidden on Mobile
```tsx
<div className="hidden md:block">
  Only visible on desktop
</div>
```

### Mobile Navigation
```tsx
<nav className="hidden md:flex items-center gap-4">
  Desktop navigation
</nav>

<nav className="md:hidden">
  Mobile navigation
</nav>
```

### Responsive Grid
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  Grid items
</div>
```

---

## Accessibility Patterns

### Form with Proper Labels
```tsx
<div className="form-group">
  <label htmlFor="email" className="form-label">
    Email Address
  </label>
  <input
    id="email"
    type="email"
    className="input-base"
    required
  />
</div>
```

### Link Styling
```tsx
<a href="/login" className="link">
  Sign in to your account
</a>
```

### Icon with Label
```tsx
<button
  title="Edit task"
  className="p-2 text-blue-600"
>
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="..." />
  </svg>
</button>
```

### Screen Reader Only Text
```tsx
<label className="sr-only">
  Search tasks
</label>
<input
  type="search"
  placeholder="Search tasks..."
  className="input-base"
/>
```

---

## Complete Example: Task Form

```tsx
export default function TaskForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Submit task
      await submitTask({ title, description });
      setTitle('');
      setDescription('');
    } catch (err) {
      setError('Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card glass-dark backdrop-blur-xl">
      {error && (
        <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg mb-4 animate-slide-down">
          <span className="text-sm font-medium text-red-800">{error}</span>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="title" className="form-label">
          Task Title
        </label>
        <input
          id="title"
          type="text"
          className="input-base"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description" className="form-label">
          Description (Optional)
        </label>
        <textarea
          id="description"
          rows={3}
          className="input-base resize-none"
          placeholder="Add details..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <div className="spinner w-4 h-4" />
            Creating...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            Create Task
          </>
        )}
      </button>
    </form>
  );
}
```

---

## Tips & Best Practices

1. **Use Semantic HTML**: Always use proper heading levels and form elements
2. **Group Related Elements**: Use `.form-group` for form fields
3. **Provide Feedback**: Show loading, error, and success states
4. **Maintain Contrast**: Ensure text is readable on all backgrounds
5. **Test Responsiveness**: Check mobile, tablet, and desktop views
6. **Animate Purposefully**: Use animations to guide attention
7. **Keep It Accessible**: Always include labels, titles, and alt text
8. **Mobile First**: Design for mobile, enhance for larger screens
9. **Consistent Spacing**: Use Tailwind spacing scale throughout
10. **Use Icons Meaningfully**: Pair icons with text labels

---

**Last Updated**: January 8, 2025
**Status**: Production Ready
