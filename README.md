# Orphan Scenes to Galleries - Stash Plugin

A [Stash](https://github.com/stashapp/stash) plugin that automatically assigns orphan scenes (scenes without galleries) to matching galleries based on configurable matching criteria.

## Features

- 🔍 **Multiple Matching Strategies**:
  - **Path Matching**: Assigns scenes to galleries in the same directory (most reliable)
  - **Performer Matching**: Matches scenes and galleries that share performers
  - **Date Matching**: Matches scenes and galleries with similar dates (with configurable tolerance)

- ⚙️ **Configurable Settings**:
  - Enable/disable each matching strategy independently
  - Set minimum performer matches required
  - Configure date tolerance (in days)
  - Exclude organized scenes from processing
  - Dry run mode for safe testing

- 📊 **Progress Tracking & Logging**:
  - Real-time progress bar during processing
  - Detailed logging of matches and assignments
  - Summary statistics at completion

## Installation

### Option 1: Manual Installation

1. Download or clone this repository
2. Copy the entire `stash-plugin-orphan-scenes-to-galleries` folder to your Stash plugins directory:
   - **Windows**: `%USERPROFILE%\.stash\plugins\`
   - **Linux/Mac**: `~/.stash/plugins/`

3. Install Python dependencies:
   ```bash
   pip install stashapp-tools
   ```

4. In Stash, go to **Settings > Plugins** and click **Reload Plugins**

### Option 2: Using Git (Recommended)

Navigate to your Stash plugins directory and clone:

```bash
cd ~/.stash/plugins/  # or %USERPROFILE%\.stash\plugins\ on Windows
git clone https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries.git
pip install -r stash-plugin-orphan-scenes-to-galleries/requirements.txt
```

Then reload plugins in Stash.

## Usage

### Configuration

Go to **Settings > Plugins > Orphan Scenes to Galleries** and configure the matching options:

#### Matching Options

- **Match by Path** (default: enabled)
  - Assigns scenes to galleries if they're in the same directory
  - Most reliable matching method
  - Example: Scene at `/videos/shoot1/scene.mp4` → Gallery at `/videos/shoot1/`

- **Match by Date** (default: disabled)
  - Matches scenes and galleries with similar dates
  - **Date Tolerance**: Number of days difference allowed (default: 1)
  - Example: Scene from 2024-03-15 → Gallery from 2024-03-14 (within 1 day)

- **Match by Performers** (default: disabled)
  - Matches scenes and galleries that share performers
  - **Minimum Performer Matches**: How many shared performers required (default: 1)
  - Example: Scene with [Performer A, Performer B] → Gallery with [Performer A, Performer C]

#### Other Options

- **Exclude Organized Scenes** (default: disabled)
  - Skip scenes marked as "organized"

- **Dry Run** (default: disabled)
  - **Always enable this first!** Test the plugin without making changes
  - Review the logs to see what would be assigned
  - Disable to actually perform assignments

### Running the Plugin

1. Go to **Settings > Tasks**
2. Find **"Assign Orphan Scenes to Galleries"** in the plugin tasks list
3. Click **Run** (or the play button)
4. Monitor progress in the **Logs** tab

### Recommended Workflow

1. **Enable Dry Run mode** in plugin settings
2. **Run the task** and review the logs
3. Check which scenes would be assigned to which galleries
4. **Disable Dry Run mode** if the results look correct
5. **Run again** to actually perform the assignments

## How It Works

The plugin processes orphan scenes in the following order:

1. **Finds all orphan scenes** (scenes with `galleries_count = 0`)
2. **Fetches all galleries** in your database
3. **For each orphan scene**, tries matching strategies in priority order:
   - First: Path matching (if enabled)
   - Second: Performer matching (if enabled)
   - Third: Date matching (if enabled)
4. **Assigns the scene** to the first matching gallery found
5. **Logs the results** with detailed statistics

## Examples

### Example 1: Simple Path Matching

**Setup:**
- Scene: `/media/photoshoots/2024-03-15/video.mp4`
- Gallery: Folder at `/media/photoshoots/2024-03-15/`

**Result:** Scene automatically assigned to gallery ✓

### Example 2: Performer Matching

**Setup:**
- Scene: Has performers [Alice, Bob]
- Gallery A: Has performers [Alice]
- Gallery B: Has performers [Alice, Bob]
- Minimum Performer Matches: 2

**Result:** Scene assigned to Gallery B (2 matches) ✓

### Example 3: Date Tolerance

**Setup:**
- Scene: Date 2024-03-15
- Gallery A: Date 2024-03-14
- Gallery B: Date 2024-03-10
- Date Tolerance: 1 day

**Result:** Scene assigned to Gallery A (within tolerance) ✓

## Troubleshooting

### Plugin doesn't appear after installation

- Check that the plugin files are in the correct directory
- Ensure `orphan_scenes_to_galleries.yml` and `.py` files have the same base name
- Click **Reload Plugins** in Stash settings
- Check Stash logs for errors

### "No orphan scenes found"

- All your scenes already have galleries assigned
- Check if "Exclude Organized Scenes" is enabled - this may filter out scenes

### Scenes not being assigned

- Enable **Dry Run** and check the logs to see why matches aren't found
- Try enabling different matching strategies
- For path matching: ensure scene and gallery paths actually match
- For performer matching: verify scenes and galleries share performers
- For date matching: increase the date tolerance

### Permission errors

- Ensure Python has permission to read your Stash configuration
- On Linux/Mac, check file permissions: `chmod +x orphan_scenes_to_galleries.py`

### Dependencies not found

```bash
pip install stashapp-tools
```

## Development

### Requirements

- Python 3.7+
- `stashapp-tools` package

### Testing

Always test with **Dry Run mode enabled** first:

```python
# In plugin settings
dryRun: True
```

### Logging

The plugin uses the `stashapi.log` module. Logs appear in:
- Stash UI: **Settings > Logs > Plugins**
- Log level can be configured in Stash settings

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with dry run mode
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/issues)
- **Stash Community**: [Discourse Forum](https://discourse.stashapp.cc/)
- **Discord**: [Stash Discord Server](https://discord.gg/2TsNFKt)

## Acknowledgments

- Built for [Stash](https://github.com/stashapp/stash)
- Uses [stashapp-tools](https://github.com/stashapp/stashapp-tools) Python library
- Inspired by other community plugins in [CommunityScripts](https://github.com/stashapp/CommunityScripts)

## Changelog

### v1.0.0 (2026-02-27)
- Initial release
- Path-based matching
- Performer-based matching
- Date-based matching with tolerance
- Dry run mode
- Progress tracking and detailed logging
