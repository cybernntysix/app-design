# README for AI-Powered Financial Empowerment App

## Purpose
A privacy-first, modular app for music creators to track streams, royalties, and performance across all major platforms. Designed for dark mode with futuristic, violet, and neon accents.

## Features
- Onboarding: Role, goal, PIN, and theme selection
- PIN lock for security
- Dashboard: Streams, revenue, top tracks, AI suggestions
- Data ingestion: Public metrics, optional CSV upload
- Royalty splits: Custom per-song percentages
- Song detail: Edit info, splits, notes
- Platform coverage: Spotify, Apple, YouTube, SoundCloud, more
- Expansion: Followers, SEO, beat protection, and more

## Structure
```
app/
  main.py
  screens/
    onboarding.py
  assets/
    icons/
    themes/
      futuristic_violet.py
  data/
  utils/
    model.py
  config/
```

## Theme
- Dark mode base
- Violet, neon blue, magenta accents
- Modern, minimal, high-vibrational look

---
Expand as needed for new features and modules.

## Dashboard Preview
To jump directly into the dashboard render (instead of onboarding), start the app with:

```bash
APP_START_SCREEN=dashboard python -m app.main
```

If you omit `APP_START_SCREEN`, the app still starts on onboarding by default.

If your environment cannot install Kivy, you can still preview the dashboard structure in terminal:

```bash
python -m app.terminal_preview --artist "Demo Artist" --platform Spotify --query dream
```

## VSCode Sanity Check (copy/paste)
Use this in your VSCode terminal to confirm you are on the same repo state that includes the dashboard preview updates:

```bash
git rev-parse --show-toplevel
git branch --show-current
git log --oneline -n 5
git status --short
python -m py_compile app/main.py app/screens/dashboard.py app/terminal_preview.py
APP_START_SCREEN=dashboard python -m app.main
```

Expected behavior:
- `git status --short` returns empty output when there are no uncommitted changes.
- `py_compile` exits without errors.
- The final command opens the app directly to the dashboard when Kivy is installed.

## If `git pull` says up to date but changes are still missing
If your output shows only:
- `ba28474 Resolve merge conflict in README.md`
- `a31acb4 Initial commit`

then your `origin/main` does **not** contain the newer dashboard-preview commits yet.

Run this to confirm whether `terminal_preview.py` ever existed in remote history:

```bash
git log --oneline --all -- app/terminal_preview.py
```

- If this prints nothing, the updates were never pushed to your remote branch.
- In that case, apply the changes locally (or from a patch/PR), then commit and push.

Quick local recovery commands:

```bash
mkdir -p app
printf '"""Terminal fallback preview for dashboard sections when Kivy UI cannot launch."""\n\n\ndef main():\n    print("Dashboard terminal preview placeholder")\n\n\nif __name__ == "__main__":\n    main()\n' > app/terminal_preview.py

git add app/terminal_preview.py
git commit -m "Add missing terminal preview helper"
git push origin main
```
