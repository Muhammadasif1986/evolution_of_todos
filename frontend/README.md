# Task Management Frontend

This is the Next.js 16 frontend for the task management application using the App Router.

## Structure

```
frontend/
├── app/                    # Next.js 16 App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page (redirects to login)
│   ├── login/page.tsx      # Login page
│   ├── signup/page.tsx     # Signup page
│   └── tasks/page.tsx      # Tasks dashboard
├── components/             # Reusable React components
│   ├── ui/                 # General UI components
│   │   └── Header.tsx      # Navigation header
│   └── tasks/              # Task-specific components
│       └── TaskList.tsx    # Task list component
├── public/                 # Static assets
├── styles/                 # Global styles
├── globals.css             # Tailwind CSS globals
├── package.json            # Dependencies
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS configuration
└── tsconfig.json           # TypeScript configuration
```

## Features

- **Authentication Flow**: Login and signup pages with form validation
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Client Components**: Interactive UI with React state management
- **Component Architecture**: Modular and reusable components

## Pages

- `/` - Home page (redirects to login)
- `/login` - User login
- `/signup` - User registration
- `/tasks` - Main task dashboard

## Setup

1. Install dependencies: `npm install`
2. Run development server: `npm run dev`

## API Integration

The frontend is designed to connect with the backend API:
- Authentication: `/api/auth/login`, `/api/auth/signup`
- Tasks: `/api/{user_id}/tasks` (CRUD operations)

The API integration is prepared with TODO comments for implementation.