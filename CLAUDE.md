# Workout Tracker: Rules for AI Agents

Read this before changing anything. Then read [WORKING_MEMORY.md](WORKING_MEMORY.md) for the current state and next task, and update it before you finish.

## Ground rules

1. **Never run `git push`.** The user pushes manually.
2. **Commit your own work** without asking. Use one commit per logical change, and don't bundle unrelated changes. End messages with the attribution line your harness asks for.
3. **No build steps, bundlers, frameworks or npm.** Plain HTML, CSS and JS that open straight from disk (`file://`) and work on a static host.
4. **Leave `greece.html`, `greeceV1.html` and `greeceV2.html` alone.** They are an unrelated trip planner that happens to live in this repo.
5. **Don't break anyone's saved progress.** See [Saved progress](#saved-progress-read-before-touching-checkboxes). This is the easiest thing to break by accident.
6. **Don't hand-edit `toolkit-week.html`.** It is generated. See [Mobility & Strength](#mobility--strength-generated-page).
7. **Verify in a real browser before committing.** See [Verifying changes](#verifying-changes).
8. Keep the layout simple and readable on a phone. Most use is on an iPhone.

## Repo map

| File | What it is |
|---|---|
| `index.html` | Home page: one card per routine. Also forwards old bookmarks (see below). |
| `bodyweight-rope.html` | Routine "Bodyweight + Jump Rope". Hand-written. Has Moderate/Extreme modes. |
| `toolkit-week.html` | Routine "Mobility & Strength" (listed first on the home page): 28-day Mobility Toolkit + Strength + Cardio. **Generated**; don't edit. The filename predates the rename; keep it so links and saved progress keep working. |
| `scripts/build_toolkit_week.py` | Builds `toolkit-week.html`. Edit the Toolkit plan here. |
| `styles.css` | Shared styles for every page. |
| `app.js` | Shared behaviour for every routine page (views, rounds, modes, popups, saving, reset). |
| `WORKING_MEMORY.md` | Current state, history, TODOs. Update it at the end of a session. |
| `PROJECT_STARTER.md` | The user's general process template. |
| `docs/video_addition_workflow.md` | How to pick and check embeddable YouTube videos. |

## How a routine page works

Each routine is one HTML page that links `styles.css` and loads `app.js` at the **end of `<body>`** (app.js reads `document.body` immediately).

**Views.** Each day is a `<div id="monday" class="workout-day">`; the overview is `<div id="overview" class="workout-day active">`. `setDay(id)` shows one. Valid `?day=` values come from whatever `.workout-day` ids exist on the page, so day ids must be unique, lowercase and URL-safe.

**Menu.** Buttons in `#navModal` call `setDay('monday')`. The active button is found by matching `'monday'` *with the quotes* inside its `onclick`, so keep that exact form. Links in the menu (like "All Routines") are `<a class="nav-btn nav-link">` with no onclick.

**URL.** `?day=<id>` picks the view; `?m=y` turns on Extreme mode. `updateUrl()` writes both.

**Exercise row.** Copy this shape exactly; the CSS, popups and saving all depend on it:

```html
<li><label class="exercise-label"><input type="checkbox"><span class="exercise-name">Pushups</span><span
        class="exercise-reps">14</span></label><button class="info-icon" data-name="Pushups"
    data-desc="One-sentence how-to."
    data-video="https://www.youtube.com/watch?v=VIDEO_ID"
    onclick="openInfoModal(event, this)">i</button></li>
```

**Rounds.** Put `<span class="rounds">3 Rounds</span>` inside an `<h2>`, and the `<ul>` of exercises right after that `<h2>`. `initRounds()` copies the list once per round and adds Prev/Next buttons right before it. Only `<div class="note">` elements may sit between the `<h2>` and the `<ul>`; they stay between the heading and the Prev/Next buttons (e.g. the rest-times note under "Circuit"). Anything else stops rounds from building. A range like "2–3 Rounds" builds the larger number.

Per-round text uses pipe-separated attributes on elements inside the list: `data-round-text` (visible name), `data-round-name` / `data-round-desc` (info popup), `data-round-reps-moderate` / `data-round-reps-extreme`. Round 1 uses the first value; missing values repeat the last one.

**Moderate / Extreme mode** (only on pages with a `#modeSelect` dropdown). Each `.exercise-reps` carries `data-reps-moderate` and `data-reps-extreme`; `setMode()` swaps the text and adds `body.theme-extreme` (red tint). Pages without `#modeSelect` ignore `?m=y`.

**Videos.** `data-video` on the info button:
- A single video (`youtube.com/watch?v=` or `youtu.be/`) plays inside the app. Check it's embeddable first, using [docs/video_addition_workflow.md](docs/video_addition_workflow.md).
- Anything else (e.g. a YouTube search URL) shows "Find Videos on YouTube" and opens in a new tab.

**Popups.** `openConfirmModal(message, onConfirm, title = 'Confirm Reset', buttonLabel = 'Reset')`. Every routine page must include the info, video and confirm modal markup with the same ids (`infoModal`, `videoModal`, `confirmModal`, `confirmModalTitle`, `confirmModalMsg`, `confirmActionBtn`). Copy it from `bodyweight-rope.html`.

**Reset.** `resetDay(id)` and `resetWeek()` ask first; `clearWeekProgress()` clears without asking (used by Mobility & Strength's "Start next week").

## Saved progress (read before touching checkboxes)

Ticks are saved in `localStorage`. All pages share one origin, so every routine needs its own prefix: set `data-storage-prefix` on `<body>`. `checkboxKey()` in `app.js` builds each key in one of two ways:

| Scheme | Used by | Key | What breaks it |
|---|---|---|---|
| **By position** (checkbox has no `data-key`) | `bodyweight-rope.html` (prefix defaults to `workout-cb-`) | `workout-cb-<n>`, where n is the checkbox's position on the page *after* rounds are built | Adding, removing or reordering **any** checkbox shifts every tick after it onto the wrong exercise. |
| **By name** (checkbox has `data-key`) | `toolkit-week.html` (prefix `toolkit-cb-`) | `toolkit-cb-<data-key>-r<round>` | Renaming a `data-key`. Ticks under the old key are just lost. |

Rules:
- **New routines must use `data-key` on every checkbox** (unique per page, e.g. `monday-core-dead-bug`). Don't add new position-based pages.
- **In `bodyweight-rope.html`, changing the list of checkboxes moves the user's saved ticks.** Tell the user before you do it. Editing text, reps or descriptions is safe.
- Don't change an existing page's `data-storage-prefix`. That wipes its saved progress.
- Migrating `bodyweight-rope.html` to `data-key` is a reasonable future task, but it orphans existing ticks unless you also convert the old keys. Ask the user first.
- Mobility & Strength also saves the chosen week under `toolkit-week`.

## Mobility & Strength (generated page)

`toolkit-week.html` is built by `scripts/build_toolkit_week.py`. To change it:

1. Edit the script.
2. Run `python scripts/build_toolkit_week.py` (works from any folder). It prints the checkbox count and fails if two checkboxes on the page share a `data-key`.
3. Check it in the browser, then commit the script and the HTML together.

What's in the script:
- `TOOLKIT`: Skool lesson title and `md=` id for each week (1–4) and Toolkit day (1–6). The links go to the user's Skool "Moves Method" classroom. Skool needs a login, so the app can only link to lessons, not show them.
- `EX`: exercise library (description and YouTube search query), shared across all weeks.
- `W23`: per-week numbers for Weeks 2–3 (rounds, bike minutes, rope intervals).
- `build(day, week)`: what each day looks like in each week. Week 1 is Toolkit only, Weeks 2–3 share a layout, and Week 4 has its own reordered layout.

How the page works: each day contains four `<div class="week-variant" data-week="N">` blocks. The week picker adds `.active` to the matching block (CSS hides the others) and saves the choice. Every checkbox's `data-key` is `<day>-w<week>-<exercise-slug>`, so **renaming an exercise in the script resets its saved ticks**. That's acceptable, but mention it to the user.

The user's plan is the source of truth. If the plan's daily text and its progression table disagree, ask the user. Don't guess.

## Adding a new routine

1. Copy `bodyweight-rope.html`'s `<head>`, header, menu and modal markup into a new page with a short, descriptive filename.
2. Give `<body>` a new `data-storage-prefix` (e.g. `data-storage-prefix="newname-cb-"`) and a `data-key` on every checkbox.
3. Add a `‹ Routines` back link and an "All Routines" menu link, as the existing pages have.
4. Add a card for it to `index.html`.
5. If the content is long or varies by week, write a build script in `scripts/` like `build_toolkit_week.py` instead of hand-writing repeated HTML.
6. Update `README.md` (routine list) and `WORKING_MEMORY.md`.

## Old links

Before the app had multiple routines, `index.html` *was* the Bodyweight + Jump Rope routine. A script in `index.html`'s `<head>` forwards any `?day=` or `?m=` link to `bodyweight-rope.html` with the same parameters. Keep this working.

## Verifying changes

There are no automated tests. Before committing:

- Run `node --check app.js` after editing app.js.
- Open the changed page(s) in a browser. On this machine, headless Edge works from PowerShell (Git Bash gets no output from it):

  ```powershell
  $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
  $sp = "<scratch folder>"   # a throwaway browser profile goes here
  # Rendered page after scripts run:
  & $edge --headless=new --disable-gpu --no-first-run "--user-data-dir=$sp\edge" --virtual-time-budget=3000 --dump-dom "file:///C:/Repos/workouts/toolkit-week.html?day=monday" | Out-String
  # Screenshot (renders a bit wider than --window-size, so the right edge gets cut off; that's not a layout bug):
  & $edge --headless=new --disable-gpu --no-first-run "--user-data-dir=$sp\edge" --hide-scrollbars --window-size=400,1000 --virtual-time-budget=3000 "--screenshot=$sp\shot.png" "file:///C:/Repos/workouts/index.html"
  ```

  To test clicks, saving and reloads, write a scratch HTML page that loads the routine in an `<iframe>`, drives it with JS, and writes results into its own `<pre>`. Then `--dump-dom` that page with `--allow-file-access-from-files --disable-web-security`. Keep test pages out of the repo.

- Things worth checking after most changes:
  - Rounds still build ("Round 1 / N").
  - `?day=` opens the right view.
  - A tick survives a reload.
  - Reset clears it.
  - `index.html?day=friday&m=y` still lands on Bodyweight + Jump Rope, Friday, Extreme.

## Keeping docs current

- Update `WORKING_MEMORY.md` (Last completed step, commit/push status, Next task, TODO) at the end of every session.
- Update `README.md` when routines or files change.
- Change this file when you change any rule or behaviour described here.
