# Tasks: Fix Next.js Build Errors

**Input**: Design documents from `/specs/002-fix-nextjs-build/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Build verification using `npm run build` is required to validate each level of fix.

**Organization**: Tasks are grouped by setup, foundation, and user story phases.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (US1, US2)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Create `.env.local` in `frontend/` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [x] T002 [P] Configure `.gitignore` in `frontend/` to include `.env.local`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 Update `frontend/tsconfig.json` to exclude the `backup/` directory
- [x] T004 Add and export `User` interface in `frontend/src/types/todo.ts`

**Checkpoint**: Foundation ready - build failure causes addressed.

---

## Phase 3: User Story 1 - Resolve Build Blockers (Priority: P1) 🎯 MVP

**Goal**: Fix the errors preventing the Next.js application from building successfully.

**Independent Test**: Run `next build` in `frontend/` and verify success.

### Implementation for User Story 1

- [x] T005 Remove or properly move legacy `frontend/backup/` files to ensure zero interference
- [x] T006 [P] [US1] Verify import paths in `frontend/src/context/AuthContext.tsx`
- [x] T007 [P] [US1] Verify import paths in `frontend/src/services/authService.ts`
- [ ] T008 [US1] Run `npm run build` in `frontend/` and capture output
- [ ] T009 [US1] Resolve any remaining TypeScript/Lint errors found in T008

**Checkpoint**: User Story 1 (Production Build) succeeds.

---

## Phase 4: User Story 2 - Build Verification (Priority: P2)

**Goal**: Verify fixes resolve reported issues and don't introduce regressions.

**Independent Test**: Clean build verification.

### Implementation for User Story 2

- [ ] T010 [US2] Run `rm -rf frontend/.next` to clear build cache
- [ ] T011 [US2] Run a final verification build: `cd frontend && npm run build`
- [ ] T012 [US2] Document build success in a validation log or final report

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T013 [P] Remove any temporary debug logs created during the fix process
- [ ] T014 Run validation on `quickstart.md` steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion.
- **User Story 2 (Phase 4)**: Depends on US1 completion.
- **Polish (Final Phase)**: Depends on all user stories completion.

### Parallel Opportunities

- T001 and T002 can run in parallel.
- T006 and T007 can run in parallel.
- Checks marked [P] can run together if affecting different files.
