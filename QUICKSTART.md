# Quick Start Guide

Get your Stash plugin up and running in 5 minutes!

## Prerequisites

- Stash installed and running
- Python 3.7+ installed
- pip (Python package manager)

## Installation

### Step 1: Install Dependencies

```bash
pip install stashapp-tools
```

### Step 2: Copy Plugin to Stash

**On Linux/Mac:**
```bash
# From the plugin directory
cp -r . ~/.stash/plugins/orphan-scenes-to-galleries/
```

**On Windows (PowerShell):**
```powershell
# From the plugin directory
Copy-Item -Recurse . "$env:USERPROFILE\.stash\plugins\orphan-scenes-to-galleries\"
```

**Or manually:**
1. Locate your Stash plugins directory:
   - Windows: `%USERPROFILE%\.stash\plugins\`
   - Linux/Mac: `~/.stash/plugins/`
2. Create a new folder named `orphan-scenes-to-galleries`
3. Copy all plugin files into that folder

### Step 3: Reload Plugins in Stash

1. Open Stash web interface (usually http://localhost:9999)
2. Go to **Settings** → **Plugins**
3. Click **Reload Plugins** button
4. Verify "Orphan Scenes to Galleries" appears in the plugins list

## First Run

### Configure the Plugin

1. In Stash, go to **Settings** → **Plugins**
2. Find **"Orphan Scenes to Galleries"**
3. Click to expand settings
4. **IMPORTANT: Enable "Dry Run"** for your first test!
5. Click **Save**

### Run the Task

1. Go to **Settings** → **Tasks**
2. Scroll down to **"Plugin Tasks"** section
3. Find **"Assign Orphan Scenes to Galleries"**
4. Click **Run** (▶️ button)
5. Wait for the task to complete

### Check Results

1. Go to **Settings** → **Logs** → **Plugins**
2. Review the log output:
   - How many orphan scenes were found
   - Which scenes matched to which galleries
   - Summary statistics
3. If the results look good, **disable Dry Run** and run again!

## Expected Results

After a successful run (with Dry Run disabled), you should see:

```
Starting orphan scene processing...
Found 42 orphan scenes
Processing 42 orphan scenes using folder hierarchy matching...
Matched scene 123 to gallery 456 ('My Gallery') via image 789 in same folder
Assigning scene 123 ('My Scene') to gallery 456 ('My Gallery')
...
==================================================
Processing complete!
Total orphan scenes: 42
Assigned: 30
Skipped: 12
Errors: 0
==================================================
```

## Troubleshooting

### Plugin doesn't appear

- ✅ Check file names match: `orphan_scenes_to_galleries.yml` and `.py`
- ✅ Verify Python is installed: `python --version` or `python3 --version`
- ✅ Check Stash logs for errors: **Settings** → **Logs** → **Stash**

### No orphan scenes found

This means all your scenes already have galleries! That's actually good news 🎉

### Scenes not being assigned

- Make sure **Dry Run is disabled** to actually perform assignments
- Check that images exist in the same or nearby folders as your scenes
- Verify images are properly assigned to galleries
- Review logs to understand why matches aren't found
- Ensure scene and gallery folders are in related directories

### Import errors

```bash
# Install missing dependencies
pip install stashapp-tools
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [TESTING.md](TESTING.md) for advanced testing options
- Adjust plugin settings based on your needs
- Run the task periodically to catch new orphan scenes

## Getting Help

- 🐛 Report issues: [GitHub Issues](https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/issues)
- 💬 Ask questions: [Stash Discord](https://discord.gg/2TsNFKt)
- 📖 Read docs: [Stash Documentation](https://docs.stashapp.cc/)

---

**Happy organizing! 🎬**
