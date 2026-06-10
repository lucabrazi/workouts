# AI Agent Working Memory

This file maintains the active state, goals, and history of the project to allow AI coding assistants to easily catch up on context across different sessions.

## AI Working Memory

Read this block first when starting a new AI/session, and update it before ending a session.

- **Project goal:** Weekly Workout Routine Tracker (Vanilla HTML/CSS/JS) with LocalStorage persistence, multi-round tracking, video embeds, and clean UI.
- **Current repo shape:** Flat root directory. Primary entry point: [index.html](file:///c:/Repos/workouts/index.html).
- **Production/live relationship:** Local development. Changes can be pushed to GitHub repository remote.
- **Active phase:** Phase 8: Feature/Workflow Buildout
- **Active step:** Wait for user instructions.
- **Last completed step:** Added verified embeddable YouTube videos featuring male-led instruction for all 21 Saturday/Sunday exercises.
- **Current non-negotiables:**
  - Keep layout simple, responsive, and readable.
  - Maintain LocalStorage state index mapping for all checkboxes in [index.html](file:///c:/Repos/workouts/index.html).
  - Do not introduce build steps or bundlers unless explicitly requested.
  - **Do not run `git push`; only stage and commit changes locally. The user will push manually.**
- **Current risks/concerns:** None at this stage.
- **Protected areas:** [index.html](file:///c:/Repos/workouts/index.html) logic.
- **Current scratch/local-only files:** None.
- **Current verification commands:** None (manual browser checks of [index.html](file:///c:/Repos/workouts/index.html)).
- **Current commit/push status:** Local main has uncommitted changes. Ready to be staged and committed.
- **Next task:** Wait for user instructions on upcoming workout features or UI tweaks.

---

## Detailed Chat History Log

### Session 1
* **User & Agent:** Initial setup, reviewed `index.html`, added `localStorage` persistence, URL state management bug fix, and accessibility improvements. Created this `WORKING_MEMORY.md` file.
* **User & Agent:** Converted layout to a tabular format, implemented dynamic round generation using Javascript, and added "Reset Week/Day" functionality.
* **User & Agent:** Changed navigation to a hidden modal overlay with a hamburger menu.
* **User & Agent:** Added an "Info" modal for each exercise, displaying descriptions and dynamically loading YouTube videos in a fullscreen modal if a `data-video` link is provided.
* **User & Agent:** Cleaned up duplicate exercises and removed video links that blocked embedding (Error 153). 

### Session 2
* **User & Agent:** Stabilized repository by creating `README.md`, `.gitignore`, and structured `WORKING_MEMORY.md` matching `PROJECT_STARTER.md` guidelines.
* **User & Agent:** Doubled the top margin of `h2` elements to 40px, keeping it at 20px for the first `h2` in a parent container using CSS `:first-of-type`.
* **User & Agent:** Set the "Start" (Overview) view as default active in the HTML markup (adding `active` class to `#overview` and the corresponding nav button) and updated router comments.
* **User & Agent:** Implemented Workout Intensity Modes (Moderate vs. Extreme), adding a select dropdown in the Options section, mapping rep differences using data attributes, and updating URL query strings to include `m=y`.
* **User & Agent:** Polished workout intensity mode: removed parentheses details from select labels, placed `m` query parameter before `day` in URL query strings, and added a custom red-tinted CSS theme switch for Extreme mode. 
