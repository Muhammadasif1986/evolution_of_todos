# Quick Reference - Modern UI Components

## Quick Copy-Paste Components

### Buttons

```tsx
// Primary Button
<button className="btn-primary">Click me</button>

// Secondary Button
<button className="btn-secondary">Click me</button>

// Outline Button
<button className="btn-outline">Click me</button>

// Full Width
<button className="btn-primary w-full">Full Width</button>

// With Icon
<button className="btn-primary flex items-center gap-2">
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
  </svg>
  Create
</button>

// Disabled/Loading
<button className="btn-primary" disabled>
  <span className="flex items-center gap-2">
    <div className="spinner w-4 h-4" />
    Loading...
  </span>
</button>
```

### Forms

```tsx
// Form Group
<div className="form-group">
  <label htmlFor="name" className="form-label">
    Full Name
  </label>
  <input
    id="name"
    type="text"
    className="input-base"
    placeholder="John Doe"
  />
</div>

// With Error
<div className="form-group">
  <label htmlFor="email" className="form-label">
    Email
  </label>
  <input
    id="email"
    type="email"
    className="input-base input-error"
  />
  <p className="text-error text-sm mt-1">Invalid email</p>
</div>

// Textarea
<div className="form-group">
  <label htmlFor="message" className="form-label">
    Message
  </label>
  <textarea
    id="message"
    rows={3}
    className="input-base resize-none"
    placeholder="Type message..."
  />
</div>

// Checkbox
<label className="flex items-center gap-2 cursor-pointer">
  <input
    type="checkbox"
    className="w-4 h-4 rounded border-gray-300 text-accent-primary cursor-pointer"
  />
  <span className="text-sm text-gray-700">Remember me</span>
</label>
```

### Alerts

```tsx
// Error Alert
<div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg flex items-start gap-3">
  <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
  </svg>
  <span className="text-sm font-medium text-red-800">Something went wrong</span>
</div>

// Success Alert
<div className="p-4 bg-green-50 border-2 border-green-200 rounded-lg flex items-start gap-3">
  <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
  </svg>
  <span className="text-sm font-medium text-green-800">Success!</span>
</div>
```

### Cards

```tsx
// Standard Card
<div className="card">
  <h3 className="text-lg font-semibold mb-2">Title</h3>
  <p className="text-gray-600">Content here</p>
</div>

// Glass Card
<div className="card-glass backdrop-blur-xl border border-white/20">
  <h3 className="text-lg font-semibold mb-2">Title</h3>
  <p className="text-gray-600">Content here</p>
</div>

// Card with Hover
<div className="card glass-dark backdrop-blur-xl border border-white/20 hover:shadow-glow-lg transition-all duration-300">
  Content
</div>
```

### Badges

```tsx
// Success
<span className="badge-success">Completed</span>

// Warning
<span className="badge-warning">Pending</span>

// Error
<span className="badge-error">Failed</span>
```

### Loading States

```tsx
// Spinner
<div className="spinner" />

// Skeleton
<div className="skeleton h-4 w-3/4" />

// Multiple Skeletons
<div className="space-y-4">
  <div className="skeleton h-4 w-full" />
  <div className="skeleton h-4 w-5/6" />
  <div className="skeleton h-4 w-4/6" />
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
  <p className="text-lg font-medium text-gray-700 mb-2">No items</p>
  <p className="text-gray-500 mb-6">Create your first item to get started</p>
  <button className="btn-primary inline-flex">Create Item</button>
</div>
```

## CSS Classes Cheat Sheet

### Buttons
- `btn-primary` - Main action button
- `btn-secondary` - Alternative action
- `btn-outline` - Tertiary action

### Forms
- `input-base` - Input field
- `input-error` - Error state
- `form-group` - Form field wrapper
- `form-label` - Form label

### Cards
- `card` - Standard card
- `card-glass` - Glassmorphic card
- `glass` - Glass effect
- `glass-dark` - Dark glass effect

### Text
- `text-gradient` - Gradient text
- `text-muted` - Secondary text
- `text-error` - Error text
- `link` - Link styling

### Status
- `badge-success` - Success badge
- `badge-warning` - Warning badge
- `badge-error` - Error badge

### Loading
- `spinner` - Loading spinner
- `skeleton` - Placeholder skeleton

### Animations
- `animate-fade-in-up` - Fade in from bottom
- `animate-slide-up` - Slide from bottom
- `animate-slide-down` - Slide from top
- `animate-scale-in` - Scale from center

## Tailwind Utilities Quick Guide

### Colors
```tsx
// Text
className="text-accent-primary"
className="text-accent-secondary"
className="text-gray-600"

// Background
className="bg-accent-primary/10"
className="bg-white/30"
className="bg-gray-50"

// Border
className="border-2 border-accent-primary"
className="border-white/20"
```

### Spacing
```tsx
// Padding
className="p-4"     // Padding all
className="px-4"    // Padding left/right
className="py-2"    // Padding top/bottom

// Margin
className="m-4"     // Margin all
className="mb-2"    // Margin bottom
className="mt-4"    // Margin top

// Gap (in grids/flex)
className="gap-2"
className="gap-4"
```

### Layout
```tsx
// Flexbox
className="flex items-center justify-between gap-4"
className="flex flex-col space-y-4"

// Grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"

// Container
className="max-w-5xl mx-auto px-4"
```

### Typography
```tsx
// Font Size
className="text-sm"   // Small
className="text-base" // Normal
className="text-lg"   // Large
className="text-2xl"  // XL
className="text-3xl"  // 2XL

// Font Weight
className="font-medium"  // 500
className="font-semibold" // 600
className="font-bold"    // 700
```

### Responsive
```tsx
// Mobile First
className="w-full md:w-1/2 lg:w-1/3"
className="text-sm md:text-base lg:text-lg"
className="hidden md:block" // Hide on mobile, show on desktop
```

### Effects
```tsx
// Shadow
className="shadow-md"
className="shadow-glow-lg"

// Blur
className="backdrop-blur-md"

// Opacity
className="opacity-50"
className="hover:opacity-80"

// Rounded
className="rounded-lg"
className="rounded-full"
```

## Common Patterns

### Loading State with Button
```tsx
<button
  className="btn-primary flex items-center justify-center gap-2"
  disabled={isLoading}
>
  {isLoading ? (
    <>
      <div className="spinner w-4 h-4" />
      Loading...
    </>
  ) : (
    'Submit'
  )}
</button>
```

### Form with Validation
```tsx
<div className="form-group">
  <label htmlFor="email" className="form-label">Email</label>
  <input
    id="email"
    type="email"
    className={`input-base ${error ? 'input-error' : ''}`}
  />
  {error && <p className="text-error text-sm mt-1">{error}</p>}
</div>
```

### Staggered List
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

### Responsive Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <div key={item.id} className="card">
      {item.name}
    </div>
  ))}
</div>
```

### Mobile Menu (Hidden/Shown)
```tsx
<nav className="hidden md:flex items-center gap-4">
  Desktop Menu
</nav>

<nav className="md:hidden">
  Mobile Menu
</nav>
```

## Color Reference

### Primary Gradient
- From: `#667eea` (Indigo)
- To: `#764ba2` (Purple)

### Semantic Colors
- Success: Green (green-100, green-800)
- Warning: Amber (amber-100, amber-800)
- Error: Red (red-100, red-800)

### Backgrounds
- Primary: `from-white via-blue-50 to-purple-50`
- Secondary: `from-white via-blue-50`

## Responsive Breakpoints

| Device | Class | Width |
|--------|-------|-------|
| Mobile | None | 0-640px |
| Tablet | `md:` | 640-1024px |
| Desktop | `lg:` | 1024px+ |

## Font Sizes

| Size | Value | Class |
|------|-------|-------|
| XS | 0.75rem | `text-xs` |
| SM | 0.875rem | `text-sm` |
| Base | 1rem | `text-base` |
| LG | 1.125rem | `text-lg` |
| XL | 1.25rem | `text-xl` |
| 2XL | 1.5rem | `text-2xl` |
| 3XL | 1.875rem | `text-3xl` |
| 4XL | 2.25rem | `text-4xl` |
| 5XL | 3rem | `text-5xl` |

## Spacing Scale

| Value | Pixels |
|-------|--------|
| 1 | 4px |
| 2 | 8px |
| 3 | 12px |
| 4 | 16px |
| 6 | 24px |
| 8 | 32px |
| 12 | 48px |
| 16 | 64px |

## File Locations

- **Styles**: `/frontend/globals.css`
- **Theme**: `/frontend/tailwind.config.js`
- **Components**: `/frontend/components/`
- **Pages**: `/frontend/app/`

## Getting Help

- See **UI_UPGRADE_GUIDE.md** for detailed component documentation
- See **COMPONENT_PATTERNS.md** for practical examples
- See **MODERNIZATION_SUMMARY.md** for overview of changes

---

**Last Updated**: January 8, 2025
**Status**: Production Ready
