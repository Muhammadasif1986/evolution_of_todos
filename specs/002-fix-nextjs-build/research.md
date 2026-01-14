# Research: Fix Next.js Build Errors

## Technical Context Research

### Decision: Correct TypeScript Config and Module Resolution
**Rationale**: The primary build blockers are due to the TypeScript compiler attempting to process a `backup/` directory with incorrect import paths and a missing interface export in the active source tree.

### Findings

#### 1. Build Blockers
- **Issue**: `tsconfig.json` includes the `backup/` directory via a wildcard pattern (`**/*.ts`, `**/*.tsx`).
- **Impact**: Files in `backup/pages/` have outdated import paths (e.g., `../../components/Auth/LoginForm`) that don't match the current structure (`../src/components/...`).
- **Fix**: Exclude `backup/` in `tsconfig.json` or remove the directory.

#### 2. Missing Type Definitions
- **Issue**: `User` interface is referenced in `src/context/AuthContext.tsx` and `src/services/authService.ts` but is not exported from `src/types/todo.ts`.
- **Impact**: Compilation fails with "User is not exported".
- **Fix**: Define and export the `User` interface in `src/types/todo.ts`.

#### 3. Project Structure Conflict
- **Issue**: Root-level `pages/` directory exists for Next.js, while `src/` contains components and services, but `backup/` also contains a `pages/` directory which confuses the compiler under current `tsconfig` rules.
- **Fix**: Consolidate source code and ensure `tsconfig` only target active directories.

#### 4. Environment Variables
- **Issue**: No `.env` or `.env.local` files exist.
- **Impact**: Backend URL defaults to `http://localhost:8000` which might lead to runtime failures.
- **Fix**: Create `.env.local` with `NEXT_PUBLIC_API_URL`.

## Constraints & Invariants
- MUST NOT introduce regressions in the active `src/` or `pages/` directories.
- MUST ensure `next build` exits with code 0.
- MUST maintain compatibility with the existing FastAPI backend.

## Alternatives Considered
- **Alternative**: Update import paths in `backup/`.
  - **Rejected**: The `backup/` directory is legacy/duplicate code and should not be part of the build. It's cleaner to exclude or remove it.
- **Alternative**: Move `pages/` into `src/`.
  - **Rejected**: Next.js supports both root `pages/` and `src/pages/`. Moving it is a larger structural change that is not strictly necessary to fix the build errors.
