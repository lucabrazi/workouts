# AI Agent Working Memory

This file maintains the active state, goals, and history of the project to allow AI coding assistants to easily catch up on context across different sessions.

## AI Working Memory

Read this block first when starting a new AI/session, and update it before ending a session.

- **Project goal:** Weekly Workout Routine Tracker (Vanilla HTML/CSS/JS) with LocalStorage persistence, multi-round tracking, video embeds, and clean UI.
- **Current repo shape:** Flat root directory. Primary entry point: [index.html](file:///c:/Repos/workouts/index.html).
- **Production/live relationship:** Local development. Changes can be pushed to GitHub repository remote.
- **Active phase:** Phase 0: Repo Stabilization
- **Active step:** Wait for user instructions.
- **Last completed step:** Created [README.md](file:///c:/Repos/workouts/README.md), updated [WORKING_MEMORY.md](file:///c:/Repos/workouts/WORKING_MEMORY.md) structure, created [.gitignore](file:///c:/Repos/workouts/.gitignore), and pushed stabilization commit to remote.
- **Current non-negotiables:**
  - Keep layout simple, responsive, and readable.
  - Maintain LocalStorage state index mapping for all checkboxes in [index.html](file:///c:/Repos/workouts/index.html).
  - Do not introduce build steps or bundlers unless explicitly requested.
- **Current risks/concerns:** None at this stage.
- **Protected areas:** [index.html](file:///c:/Repos/workouts/index.html) logic.
- **Current scratch/local-only files:** None.
- **Current verification commands:** None (manual browser checks of [index.html](file:///c:/Repos/workouts/index.html)).
- **Current commit/push status:** All changes pushed. Local `main` is up-to-date with `origin/main` on `https://github.com/lucabrazi/workouts.git`.
- **Next task:** Wait for user instructions on upcoming workout features or UI tweaks.

---

## Detailed Chat History Log

### Session 1
* **User & Agent:** Initial setup, reviewed `index.html`, added `localStorage` persistence, URL state management bug fix, and accessibility improvements. Created this `WORKING_MEMORY.md` file.
* **User & Agent:** Converted layout to a tabular format, implemented dynamic round generation using Javascript, and added "Reset Week/Day" functionality.
* **User & Agent:** Changed navigation to a hidden modal overlay with a hamburger menu.
* **User & Agent:** Added an "Info" modal for each exercise, displaying descriptions and dynamically loading YouTube videos in a fullscreen modal if a `data-video` link is provided.
* **User & Agent:** Cleaned up duplicate exercises and removed video links that blocked embedding (Error 153). 
