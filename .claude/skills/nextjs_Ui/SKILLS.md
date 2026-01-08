# Next.js UI Expert Skill

## Overview
This skill provides expert-level guidance and implementation support for building modern, performant, and accessible user interfaces with Next.js. It covers component architecture, styling, state management, and best practices.

## Core Competencies

### 1. Component Architecture
- **Functional Components**: Modern React functional components with hooks
- **Server vs Client Components**: Understanding Server Components (RSC) and Client Components
- **Component Composition**: Building reusable, composable component hierarchies
- **Props & TypeScript**: Strong typing for component interfaces
- **Code Splitting**: Lazy loading components with `React.lazy()` and `next/dynamic`

### 2. Styling Strategies
- **CSS Modules**: Scoped styling to prevent conflicts
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **CSS-in-JS**: Styled-components, Emotion alternatives
- **Dark Mode**: Implementing theme switching and persistence
- **Responsive Design**: Mobile-first approach with breakpoints
- **Performance**: Minimizing CSS bundle size and avoiding layout shifts

### 3. Next.js Features
- **App Router**: File-based routing with nested layouts
- **Pages Router**: Legacy routing patterns (if needed)
- **Image Optimization**: Using `next/image` for performance
- **Font Optimization**: Web fonts with `next/font`
- **Metadata API**: SEO optimization with dynamic metadata
- **Middleware**: Request/response interceptors
- **Vercel Deployment**: Optimization for Vercel hosting

### 4. State Management
- **React Context API**: For simple to moderate state needs
- **Hooks**: `useState`, `useReducer`, `useCallback`, `useMemo`
- **URL State**: Query parameters for shareable UI state
- **Form Libraries**: React Hook Form, Formik
- **Data Fetching**: SWR, React Query (TanStack Query), fetch API

### 5. Performance Optimization
- **Code Splitting**: Route-based and component-based splitting
- **Image Optimization**: WebP formats, responsive images, lazy loading
- **Font Loading**: System fonts, variable fonts, preloading
- **JavaScript Reduction**: Minimizing client-side JavaScript
- **Caching Strategies**: Static generation, ISR, dynamic rendering
- **Web Vitals**: LCP, FID, CLS optimization
- **Bundle Analysis**: Identifying and removing bloat

### 6. Accessibility (a11y)
- **ARIA Labels**: Semantic HTML and ARIA attributes
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: Proper heading structure and alt text
- **Color Contrast**: WCAG compliance
- **Focus Management**: Visible focus indicators
- **Form Accessibility**: Labels, error messages, validation feedback

### 7. Authentication & Authorization
- **Auth Integration**: NextAuth.js, Clerk, Auth0
- **Protected Routes**: Middleware-based protection
- **Session Management**: Cookies, tokens, refresh flows
- **OAuth Integration**: Social login providers
- **User Context**: Global user state across app

### 8. Forms & Validation
- **Form Handling**: Controlled and uncontrolled components
- **Client-Side Validation**: Real-time feedback
- **Server-Side Validation**: Data integrity checks
- **Error Handling**: User-friendly error messages
- **Submission States**: Loading, success, error states
- **Accessibility**: Proper labels and ARIA

### 9. API Integration
- **Route Handlers**: API routes in App Router
- **REST Integration**: Fetch, Axios patterns
- **Error Handling**: Graceful degradation
- **Loading States**: Skeletons, spinners
- **Optimistic Updates**: UX improvements
- **Polling & WebSockets**: Real-time data

### 10. Testing & Quality
- **Unit Tests**: Jest with React Testing Library
- **Integration Tests**: Full feature testing
- **E2E Tests**: Playwright, Cypress
- **Visual Regression**: Percy, Chromatic
- **Accessibility Testing**: axe-core, Wave
- **Performance Testing**: Lighthouse CI

## Best Practices

### Component Development
- Keep components small and focused (single responsibility)
- Use composition over inheritance
- Prop drilling minimization (Context API or custom hooks)
- Memoization for expensive renders
- Error boundaries for error handling

### Styling
- Use Tailwind CSS utility classes for consistency
- Create component-level styles with CSS Modules
- Maintain design system tokens
- Dark mode support from the start
- Avoid inline styles

### Performance
- Prioritize Core Web Vitals
- Use Next.js Image component for all images
- Implement next/font for web fonts
- Code split at route and component level
- Monitor bundle size regularly

### Accessibility
- Start with semantic HTML
- Test with keyboard navigation
- Validate with accessibility tools
- Include alt text for images
- Maintain sufficient color contrast

### State Management
- Use URL for shareable state
- Context API for app-level state (theme, user)
- Local component state for UI state
- Keep state as close to usage as possible
- Avoid prop drilling

## Common Patterns

### Protected Routes
```typescript
// middleware.ts for route protection
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

### Loading States
```typescript
// Skeleton component
export function TaskSkeleton() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-200 rounded" />
      <div className="h-4 bg-gray-200 rounded w-5/6" />
    </div>
  )
}

// Suspense boundary
<Suspense fallback={<TaskSkeleton />}>
  <TaskList />
</Suspense>
```

### Form Handling
```typescript
// Form component with validation
'use client'

export default function TaskForm() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      // API call
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="text-red-500">{error}</div>}
      {/* form fields */}
    </form>
  )
}
```

## Tools & Libraries

### Recommended Stack
- **Styling**: Tailwind CSS + CSS Modules
- **Forms**: React Hook Form
- **Data Fetching**: TanStack Query (React Query)
- **UI Components**: shadcn/ui, Radix UI
- **Icons**: Lucide React
- **Auth**: NextAuth.js or Clerk
- **State**: Zustand or Context API
- **Testing**: Jest + React Testing Library

### Development Tools
- **Linting**: ESLint with Next.js config
- **Formatting**: Prettier
- **Type Checking**: TypeScript
- **Bundle Analysis**: next/bundle-analyzer
- **Performance**: Lighthouse CI
- **Accessibility**: axe DevTools

## Common Challenges & Solutions

### Challenge: Layout Shift with Dynamic Content
**Solution**: Use skeleton loaders and reserve space for dynamic content

### Challenge: Component Hydration Mismatch
**Solution**: Use `suppressHydrationWarning` or `useEffect` for client-only rendering

### Challenge: Props Drilling
**Solution**: Use Context API or custom hooks for shared state

### Challenge: Image Optimization
**Solution**: Always use `next/image` with proper sizing and formats

### Challenge: Bundle Size Growth
**Solution**: Regular monitoring, lazy loading, code splitting by route

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Web.dev Performance Guide](https://web.dev/performance/)
- [WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## When to Use This Skill

Use this skill when you need to:
- Build or optimize Next.js UI components
- Improve page performance and Core Web Vitals
- Implement responsive, accessible designs
- Integrate forms and state management
- Handle authentication and protected routes
- Troubleshoot styling and layout issues
- Refactor components for better maintainability
- Implement best practices and patterns
