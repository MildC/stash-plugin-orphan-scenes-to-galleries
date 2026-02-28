# Orphan Scenes to Galleries - Stash Plugin

A [Stash](https://github.com/stashapp/stash) plugin that automatically assigns orphan scenes (scenes without galleries) to matching galleries based on configurable matching criteria.

## Features

- 🔍 **Hierarchical Folder-Based Matching**:
  - **Same Folder Search**: First searches for images in the scene's folder and uses the first image's gallery
  - **Parent Folder Search**: If no images found, searches sibling/child folders under the same parent directory
  - **Automatic Assignment**: Uses the gallery of the first image found in the folder hierarchy

- ⚙️ **Configurable Settings**:
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

Go to **Settings > Plugins > Orphan Scenes to Galleries** and configure the options:

#### Options

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

The plugin uses a hierarchical folder-based matching approach:

1. **Finds all orphan scenes** (scenes with `galleries_count = 0`)
2. **For each orphan scene**:
   - **Step 1**: Searches for images in the same folder as the scene
     - If images are found, uses the first image's gallery
   - **Step 2**: If no images in same folder, searches for images in related folders (sibling/child folders under the same parent)
     - Queries images where the folder path starts with the parent path
     - Groups images by their folder paths
     - Uses the first image's gallery from the first matching folder
3. **Assigns the scene** to the matched gallery
4. **Logs the results** with detailed statistics

This "nearest neighbor" approach assumes that scenes and their related image galleries are stored in the same or nearby folders in the filesystem hierarchy.

## Examples

### Example 1: Same Folder Match

**Setup:**
- Scene: `/media/photoshoots/2024-03-15/video.mp4`
- Images in same folder: `/media/photoshoots/2024-03-15/image1.jpg`, `image2.jpg`
- Gallery: "March 15 Shoot" (contains the images)

**Result:** Scene automatically assigned to "March 15 Shoot" gallery ✓

### Example 2: Direct Parent Folder Search

**Setup:**
- Scene: `/media/shoots/session1/video/scene.mp4` (no images in this folder)
- Images in direct parent folder: `/media/shoots/session1/image1.jpg`, `image2.jpg`
- Gallery: "Session 1 Photos" (contains the images)

**Result:** Scene assigned to "Session 1 Photos" gallery via parent folder search ✓

The plugin searches the direct parent folder, making it easy to organize scenes in subfolders while keeping images at the parent level.

### Example 3: Multi-Level Hierarchy

**Setup:**
- Scene: `/media/studio/2024/march/scene.mp4` (no images here)
- Images in related folder: `/media/studio/2024/march/gallery/image1.jpg`
- Gallery: "March Gallery" (contains the images)

**Result:** Scene assigned to "March Gallery" via hierarchical search ✓

### Example 4: Multi-Level Hierarchy

**Setup:**
- Scene: `/media/studio/2024/april/scene.mp4` (no images here)
- There is no images in related folder. The closest match is in `/media/studio/2024/march/image1.jpg`

**Result:** Scene is left unassigned since no images found in same or related folders ✗

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
