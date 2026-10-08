# Weekly Workout Routine Tracker

A lightweight, clean, and responsive web application to track weekly workout progress, rounds, and exercises across multiple routines. Built using vanilla HTML, CSS, and JavaScript with zero external dependencies.

## Routines

- **[index.html](index.html):** Home page listing all routines.
- **[bodyweight-rope.html](bodyweight-rope.html):** Bodyweight + Jump Rope week (Moderate/Extreme modes).
- **[toolkit-week.html](toolkit-week.html):** Mobility & Strength, a 28-day Mobility Toolkit + Strength + Cardio plan. ‹ Week › and ‹ Day › steppers at the top move between weeks 1–4 and days; each week shows its own version of each day and links to that week's Skool lessons. This page is generated: edit [scripts/build_toolkit_week.py](scripts/build_toolkit_week.py) and run `python scripts/build_toolkit_week.py`.

Shared styles live in [styles.css](styles.css) and shared behavior in [app.js](app.js). Each routine page sets `data-storage-prefix` on `<body>` so saved progress stays separate per routine.

## Features

- **Tabular Navigation:** Switch between weekly overview, daily workout logs, and recovery/flex days.
- **Multi-Round Tracking:** Dynamic round replication with custom text variants per round (e.g., jump rope variations).
- **Progress Persistence:** Automatic saving of completed exercises in local storage so your progress is preserved across browser refreshes.
- **Reset Options:** Reset progress for individual days or the entire week with a single click.
- **Exercise Info & Video Modals:** Detailed exercise descriptions and direct inline YouTube video overlays for quick guidance.

## Getting Started

Since this is a vanilla web application, there are no build steps or dependencies:
1. Open the [index.html](file:///c:/Repos/workouts/index.html) file directly in any modern web browser and pick a routine.
2. Bookmark the page or host it on a service like GitHub Pages for easy access on mobile devices.

---

## Repository Documentation

We follow a structured workflow to keep development safe, clean, and organized:
- **[CLAUDE.md](CLAUDE.md):** Rules for AI agents and developers: how the pages work, how saved progress is keyed, how to edit the generated Mobility & Strength page, and how to verify changes. Read this first.
- **[PROJECT_STARTER.md](file:///c:/Repos/workouts/PROJECT_STARTER.md):** Process guide, ground rules, phase roadmap, and coding standards.
- **[WORKING_MEMORY.md](file:///c:/Repos/workouts/WORKING_MEMORY.md):** Current state, active task tracking, and chat session history for AI assistants.
- **[video_addition_workflow.md](file:///c:/Repos/workouts/docs/video_addition_workflow.md):** The step-by-step developer workflow for adding and verifying exercise video embeds.
