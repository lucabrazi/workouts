# Project Starter

Use this as the first document in any new repo. Paste it in as `PROJECT_STARTER.md`, `PROJECT_PLAN.md`, or `README.md`, then keep it updated as the project's working memory and process guide.

## AI Working Memory

Read this block first when starting a new AI/session, and update it before ending a session.

- Project goal:
- Current repo shape:
- Production/live relationship:
- Active phase:
- Active step:
- Last completed step:
- Current non-negotiables:
- Current risks/concerns:
- Protected areas:
- Current scratch/local-only files:
- Current verification commands:
- Current commit/push status:
- Next task:

## Purpose

This repo exists to solve a real problem deliberately, with enough structure that work can pause, resume, and be reviewed without losing the thread.

The first job is not to rush into implementation. The first job is to understand the goal, define constraints, identify risks, and create a process that keeps future work safe and reversible.

## Ground Rules

1. Keep working memory current.
2. Separate discovery, planning, implementation, verification, and release.
3. Do not mix unrelated changes in the same step.
4. Do not delete or rewrite important existing work without understanding it first.
5. Do not commit secrets, logs, generated output, or local scratch files.
6. Prefer small checkpoints and clear commits.
7. Build repeatable checks for risky behavior.
8. Record decisions before implementing them.
9. Preserve what already works until a replacement proves better.
10. End every session with a clear next pickup point.

## What We Learned From A Long Real Project

- Working memory matters. A short, honest status block saves enormous time after pauses, context switches, or new sessions.
- A repo can contain production code, experiments, generated files, archives, local configs, assets, scripts, and old scratch work. Classify before deleting.
- The main entry point is a good starting graph, but it rarely proves all usage. Direct links, emails, reports, tools, scheduled jobs, PDFs, APIs, and external users can bypass it.
- Deletions are safest when incremental, confirmed, and documented.
- Sensitive outputs need special protection. Email, payments, reports, legal content, auth, generated documents, and client-facing exports may need golden comparisons.
- Large files and generated artifacts can quietly ruin a repo. Decide early what belongs in source control and what belongs in external storage.
- A phase that starts as polish can reveal architecture work. Split phases when the scope grows.
- "How will the user edit/update this later?" is not a side question. It is core architecture.
- Compatibility paths, old URLs, and old files may matter long after the app changes. Preserve first, monitor, retire later.
- Good process is not bureaucracy. It is how you keep momentum without making dangerous guesses.

## Recommended Repo Shape

Adjust to fit the project:

```text
/
  docs/
    PROJECT_PLAN.md
    USAGE_AUDIT.md
    DECISIONS.md
  src/
  scripts/
  tests/
  migration/
  assets/
  temp/        # gitignored scratch files
  dist/        # gitignored generated output
```

The important thing is separation:

- `docs/`: working memory, decisions, plans, audits.
- `src/`: source code or source content.
- `scripts/`: repeatable tooling.
- `tests/`: verification.
- `migration/`: baselines, manifests, conversion scripts.
- `assets/`: tracked source assets only if appropriate.
- `temp/`: scratch/local-only work.
- `dist/`: generated output.

## Initial `.gitignore` Ideas

```gitignore
/temp/
/dist/
/build/
/node_modules/
.env
.env.*
*.log
**/.DS_Store
**/.vscode/
```

Add project-specific generated files, caches, secrets, and local-only folders after inventory.

## Phase Roadmap Template

### Phase 0: Repo Stabilization

- Decide what the repo is for.
- Add `.gitignore`.
- Establish folder structure.
- Create working-memory docs.
- Commit the baseline.

Deliverable: stable repo shape and first documented checkpoint.

### Phase 1: Discovery And Inventory

- Identify entry points.
- Identify important workflows.
- Identify users and stakeholders.
- Classify files, systems, data, dependencies, and risks.
- Record open questions.

Deliverable: usage/inventory audit and risk list.

### Phase 2: Behavior Capture Or Requirements Capture

Choose based on project type:

- For existing systems: capture current behavior, outputs, screenshots, API responses, data shapes, and workflows.
- For new systems: capture requirements, acceptance criteria, sample data, design expectations, and success metrics.

Deliverable: baselines or requirements that future work can verify against.

### Phase 3: Architecture And Strategy

- Choose stack or target architecture.
- Decide hosting/deployment.
- Decide data/storage strategy.
- Decide security/auth strategy.
- Decide cost and operational boundaries.
- Decide rollback path.

Deliverable: architecture plan and route/data/workflow map.

### Phase 4: Core Implementation

- Build the smallest useful version.
- Preserve or satisfy required behavior.
- Keep changes scoped.
- Add checks where risk is meaningful.

Deliverable: working core system.

### Phase 5: Sensitive/Shared Workflow Protection

Use this for areas where mistakes are expensive:

- email output;
- payment/receipts;
- legal documents;
- reports;
- public APIs;
- auth/session flows;
- client deliverables;
- generated files.

Deliverable: compatibility checks, golden outputs, fixtures, or approval gates.

### Phase 6: Admin/Data/Operations

- Decide what admin or data tooling is actually needed.
- Avoid rebuilding unused old tools.
- Add auth, validation, authorization, audit logs, backups, and secrets handling where needed.
- Decide who can edit/update what.

Deliverable: maintainable operations/admin workflow.

### Phase 7: Discovery And Decisions For Remaining Work

- Ask remaining design/workflow/product questions.
- Decide what belongs now, later, or never.
- Split large work into new phases if needed.

Deliverable: completed decision record.

### Phase 8: Feature/Workflow Buildout

- Implement the major workflow or feature set defined in Phase 7.
- Build source models, editors, generators, APIs, or user-facing tools as needed.
- Verify against requirements/baselines.

Deliverable: complete functional workflow.

### Phase 9: Polish And Readiness

- Performance.
- Accessibility.
- SEO/discovery if relevant.
- Analytics/monitoring.
- Error handling.
- Documentation.
- Security headers/caching/deployment checks.
- Broken-link/missing-file checks where relevant.

Deliverable: release-ready project.

### Phase 10: Release/Cutover

- Final preview/staging verification.
- Deployment configuration.
- Rollback plan.
- Release.
- Post-release monitoring.
- Closeout docs.

Deliverable: production release with rollback and monitoring.

## Questions To Ask Early

Ask one at a time when useful.

1. What problem are we solving?
2. Who uses this?
3. What must not change?
4. What is currently working well?
5. What is painful today?
6. What outputs are sensitive or trusted?
7. What needs to be editable later, and by whom?
8. What should be tracked in git?
9. What should stay out of git?
10. What data, files, or links must survive?
11. What is the deployment target?
12. What would make this project fail?
13. What is good enough for first release?
14. What can wait?

## Decision Patterns

### Working Memory

Keep a short active-status section in a doc. Update it before stopping.

### Source Of Truth

Decide whether source of truth is:

- files in git;
- a database;
- external storage;
- an API;
- a CMS/editor;
- generated output.

Do not let generated output accidentally become the editing surface unless that is intentional.

### Draft/Preview/Publish

For content or workflows that change over time, prefer:

- draft;
- preview;
- publish;
- rollback.

### Compatibility

For old links, old outputs, or old workflows:

- preserve important ones first;
- monitor usage;
- retire later only with evidence.

### Assets

For images, files, PDFs, datasets, generated artifacts, or downloads:

- decide tracked vs external;
- use stable references;
- avoid auto-delete;
- report stale candidates;
- keep manual protect lists for important assets.

### Naming

Prefer concise semantic names. Avoid preserving old names that no longer describe the thing.

### Verification

Use the smallest reliable checks:

- unit tests;
- smoke tests;
- screenshot checks;
- output hashes;
- schema validation;
- link checks;
- generated file checks;
- manual review gates.

## Verification Checklist

- Git status checked.
- Important files inventoried.
- Decisions documented.
- Risks recorded.
- Commands/scripts are repeatable.
- Sensitive outputs protected.
- Generated output not accidentally committed.
- Deployment exclusions defined.
- Tests/checks run or explicitly skipped with reason.
- Next pickup point documented.

## Commit Pattern

Use small, meaningful commits.

Example:

```text
Add project working memory

Create the initial project plan, working-memory block, phase roadmap, and session closeout process so future work can resume cleanly.
```

Example:

```text
Record discovery decisions

Document the key workflow, data, editing, verification, and release decisions before implementation begins.
```

## Session Closeout Checklist

Before ending a working session:

- Update working memory.
- Note current phase and step.
- Note files changed.
- Run relevant checks or state what was not run.
- Commit if the work reached a clean checkpoint.
- Tell the user whether the repo is clean/ahead/needs push.
- State the exact next pickup point.
