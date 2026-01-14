# Quickstart: Fix Next.js Build Errors

## Setup

1. **Environmental Configuration**:
   Create a `.env.local` file in the `frontend/` directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. **Clean Install**:
   ```bash
   cd frontend
   npm install
   ```

3. **Verify Fixes**:
   Run the production build command:
   ```bash
   npm run build
   ```

## Troubleshooting
- If build fails with module resolution errors, ensure `tsconfig.json` excludes the `backup/` directory.
- If `User` type is missing, verify it is exported from `src/types/todo.ts`.
