# Testing Guide

## Local Testing Without Stash

You can test the plugin logic locally without a running Stash instance by simulating the JSON input.

### Example Test Input

Create a file `test_input.json`:

```json
{
  "server_connection": {
    "Scheme": "http",
    "Host": "localhost",
    "Port": 9999,
    "SessionCookie": {
      "Name": "session",
      "Value": "your-session-cookie",
      "Path": "/",
      "Domain": "",
      "Expires": "0001-01-01T00:00:00Z",
      "RawExpires": "",
      "MaxAge": 0,
      "Secure": false,
      "HttpOnly": false,
      "SameSite": 0,
      "Raw": "",
      "Unparsed": null
    }
  },
  "args": {
    "mode": "processAll"
  }
}
```

### Run Test

```bash
cat test_input.json | python orphan_scenes_to_galleries.py
```

## Testing in Stash

### 1. Install the Plugin

Copy the plugin folder to your Stash plugins directory:

```bash
# Linux/Mac
cp -r stash-plugin-orphan-scenes-to-galleries ~/.stash/plugins/

# Windows (PowerShell)
Copy-Item -Recurse stash-plugin-orphan-scenes-to-galleries "$env:USERPROFILE\.stash\plugins\"
```

### 2. Install Dependencies

```bash
pip install stashapp-tools
```

### 3. Reload Plugins in Stash

1. Open Stash web interface
2. Go to **Settings > Plugins**
3. Click **Reload Plugins**
4. Verify "Orphan Scenes to Galleries" appears in the list

### 4. Configure Settings

1. Go to **Settings > Plugins > Orphan Scenes to Galleries**
2. **IMPORTANT**: Enable **Dry Run** for initial testing
3. Save settings

### 5. Run the Task

1. Go to **Settings > Tasks**
2. Scroll to "Plugin Tasks" section
3. Find **"Assign Orphan Scenes to Galleries"**
4. Click the **Run** button
5. Monitor progress in **Settings > Logs > Plugins**

### 6. Review Results

Check the logs for:
- Number of orphan scenes found
- Matched scenes and their galleries
- Which images were used for matching
- Summary statistics

### 7. Actual Run

If dry run results look good:
1. Disable **Dry Run** in plugin settings
2. Run the task again to actually assign scenes

## Debugging

### Enable Verbose Logging

Add debug statements in the Python code:

```python
log.debug(f"Debug info: {variable}")
log.info(f"Info message: {status}")
log.warning(f"Warning: {issue}")
log.error(f"Error: {error}")
```

### Check Stash Logs

Logs are available at:
- UI: **Settings > Logs > Plugins**
- File: Check your Stash data directory for log files

### Common Issues

1. **Plugin not appearing**
   - Verify file names match (base name must be identical)
   - Check Python is in PATH
   - Review Stash logs for errors

2. **Import errors**
   - Install dependencies: `pip install stashapp-tools`
   - Check Python version (3.7+ required)

3. **No matches found**
   - Check that images exist in same or nearby folders as scenes
   - Verify images are properly assigned to galleries
   - Review dry run logs to see what's being searched

## Unit Testing (Advanced)

Create `test_plugin.py` for unit tests:

```python
import unittest
from unittest.mock import Mock, MagicMock
from orphan_scenes_to_galleries import OrphanSceneProcessor

class TestOrphanSceneProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_stash = Mock()
        self.settings = {
            'excludeOrganized': False,
            'dryRun': True
        }
        self.processor = OrphanSceneProcessor(self.mock_stash, self.settings)

    def test_match_by_folder_hierarchy(self):
        scene = {
            'id': '1',
            'files': [{'path': '/videos/shoot1/scene.mp4'}]
        }

        # Mock the image query to return images with galleries
        self.mock_stash.find_images.return_value = [
            {
                'id': 'img1',
                'galleries': [
                    {'id': 'g1', 'title': 'Gallery 1', 'folder': {'path': '/videos/shoot1'}}
                ]
            }
        ]

        result = self.processor.match_by_folder_hierarchy(scene)
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 'g1')

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python test_plugin.py
```
