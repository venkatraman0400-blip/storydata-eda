# GitHub setup — step by step

A complete guide to getting this project onto GitHub correctly.
Follow these steps in order. Do not skip any.

---

## Step 1 — Create the repo on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name:** `storydata-eda`
   - **Description:** `Narrative-driven EDA using Plotly and Seaborn`
   - **Visibility:** Public (so it appears on your portfolio)
   - **Do NOT** tick "Add a README" — you already have one
4. Click **Create repository**
5. Copy the URL shown — it will look like:
   `https://github.com/YOUR_USERNAME/storydata-eda.git`

---

## Step 2 — Open your terminal

Navigate to your project folder:

```bash
cd path/to/storydata-eda
```

Confirm you're in the right place:

```bash
ls
# Should show: README.md, requirements.txt, notebooks/, src/, data/, etc.
```

---

## Step 3 — Initialize git

```bash
git init
```

You only run this once. It creates a hidden `.git/` folder that tracks your changes.

---

## Step 4 — Stage your files

```bash
git add .
```

The `.` means "add everything". Your `.gitignore` will automatically exclude the files
you told it to ignore (virtual environment, CSV files, etc).

Check what's staged:

```bash
git status
```

You should see green text for all your project files.
You should NOT see `venv/`, `data/raw/*.csv`, or `kaggle.json`.

---

## Step 5 — Your first commit

```bash
git commit -m "initial commit: project structure, utils, act 1 notebook"
```

A commit is a saved snapshot. The message describes what changed.

---

## Step 6 — Connect to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/storydata-eda.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 7 — Push to GitHub

```bash
git branch -M main
git push -u origin main
```

Your project is now live on GitHub.

---

## Step 8 — Set up your repo's About section

On your GitHub repo page:
1. Click the gear icon next to **About** (right side)
2. Add a **Description:** `Narrative-driven EDA — communicating statistical insights through visual storytelling`
3. Add **Topics** (tags): `python`, `eda`, `plotly`, `seaborn`, `data-visualization`, `pandas`, `jupyter`
4. Click **Save changes**

Topics make your repo discoverable. Always add them.

---

## Your daily git workflow (after setup)

Every time you finish work on an act:

```bash
# 1. See what changed
git status

# 2. Stage your changes
git add .

# 3. Commit with a clear message
git commit -m "complete act 2 distribution plots with violin charts"

# 4. Push to GitHub
git push
```

That's it. Four commands every time.

---

## Good commit message examples

| Situation | Message |
|---|---|
| Finish an act | `complete act 3 correlation heatmap` |
| Fix a bug | `fix null handling in missing value plot` |
| Add a feature | `add IQR outlier detection to act 5` |
| Update README | `update README with dataset link and findings` |
| Minor cleanup | `clean up notebook 02 markdown and comments` |

**Rule:** present tense, lowercase, specific. Never just "update" or "fix stuff".

---

## Common errors and fixes

**Error:** `fatal: remote origin already exists`
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/storydata-eda.git
```

**Error:** `rejected — failed to push`
```bash
git pull origin main --rebase
git push
```

**Error:** `src refspec main does not match any`
```bash
git checkout -b main
git push -u origin main
```

**Accidentally committed your CSV?**
```bash
git rm --cached data/raw/your_dataset.csv
git commit -m "remove accidentally tracked data file"
git push
```
Then make sure `data/raw/*.csv` is in your `.gitignore`.
