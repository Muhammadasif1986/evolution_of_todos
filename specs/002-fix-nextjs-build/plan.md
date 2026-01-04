# Implementation Plan: Fix Next.js Build Errors

**Branch**: `002-fix-nextjs-build` | **Date**: 2025-12-31 | **Spec**: [/specs/002-fix-nextjs-build/spec.md](spec.md)

## Summary
The goal is to resolve production build failures in the Next.js frontend project. Research identified three primary blockers: a `backup/` directory being included in the build with incorrect paths, a missing `User` type export, and missing environment configuration. The plan involves updating TypeScript configuration, defining missing types, and setting up environment defaults.

## Technical Context

**Language/Version**: TypeScript 5.6.3, Next.js 14.0.4
**Primary Dependencies**: React 18, Axios, React Query
**Storage**: N/A (Frontend types only)
**Testing**: `npm run build` (Production build verification)
**Target Platform**: Linux server (Standalone output)
**Project Type**: Web application (Next.js)
**Performance Goals**: N/A (Build fix focus)
**Constraints**: Build must exit with code 0.
**Scale/Scope**: Fixes targeted at `tsconfig.json` and `src/types/todo.ts`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Development**: FOLLOWED. Spec defined in `002-fix-nextjs-build/spec.md`.
- **Principle IV: Full-Stack Integration**: FOLLOWED. Types being added to match FastAPI backend (`User`).

## Project Structure

### Documentation (this feature)

```text
specs/002-fix-nextjs-build/
├── plan.md              # This file
├── research.md          # Identified build blockers and fix strategy
├── data-model.md        # Added User interface definition
├── quickstart.md        # Steps to verify the build fix
├── contracts/
│   └── auth.md          # Auth API contracts for verification
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
frontend/
├── tsconfig.json        # MODIFIED: to exclude backup/
├── .env.local           # CREATED: for environment defaults
└── src/
    └── types/
        └── todo.ts      # MODIFIED: to export User interface
```

**Structure Decision**: Standard Next.js project structure with root-level configuration.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
