# Deployment Guide

## Deploying to Vercel

This project is ready for deployment to Vercel. Follow these steps:

### Frontend (Next.js App)

1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the Next.js app and build it
3. Set the following environment variables in Vercel dashboard:
   - `BETTER_AUTH_SECRET`: A random secret string for authentication
   - `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., https://your-backend.vercel.app)

### Backend (FastAPI)

The backend is located in the `backend` directory. To deploy it:

1. Navigate to the `backend` directory
2. Deploy using Vercel, Railway, Heroku, or any Python-compatible hosting
3. Make sure to set the required environment variables in your backend deployment

### Environment Variables

For the frontend, you need to set:

```
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
BETTER_AUTH_SECRET=your-secret-string-here
```

### Build Information

- Framework: Next.js 16.1.1
- Language: TypeScript/JavaScript
- Package Manager: npm
- Build Command: `npm run build`
- Output Directory: `.next`
- Development Command: `npm run dev`

The build has been tested and confirmed to work successfully.