# Project Summary: Stash Orphan Scenes to Galleries Plugin

## Overview
This is a complete Stash plugin that automatically assigns orphan scenes (scenes without galleries) to matching galleries.

## Repository Structure

```
stash-plugin-orphan-scenes-to-galleries/
├── .github/workflows/
│   └── validate.yml              # CI/CD with GitHub Actions
├── .git/                         # Git repository
├── .gitignore                    # Git ignore rules
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── README.md                     # Main documentation (comprehensive)
├── QUICKSTART.md                 # 5-minute quick start guide
├── TESTING.md                    # Testing guide for developers
├── orphan_scenes_to_galleries.yml   # Plugin configuration (Stash format)
├── orphan_scenes_to_galleries.py    # Main plugin logic (Python)
├── requirements.txt              # Python dependencies
└── validate.py                   # Plugin validation script
```

## Key Files

### Plugin Files (Required by Stash)
- **orphan_scenes_to_galleries.yml**: Plugin configuration with settings, tasks, and metadata
- **orphan_scenes_to_galleries.py**: Main plugin logic implementing matching algorithms
- **requirements.txt**: Python dependencies (stashapp-tools)

### Documentation
- **README.md**: Comprehensive documentation with features, installation, usage, and troubleshooting
- **QUICKSTART.md**: Simple 5-minute installation and usage guide
- **TESTING.md**: Testing guide for developers and contributors
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **CHANGELOG.md**: Version history and planned features

### Development Tools
- **validate.py**: Validates plugin structure and configuration
- **.github/workflows/validate.yml**: GitHub Actions CI for automated testing

## Features

### Three Matching Strategies
1. **Path Matching** (most reliable)
   - Matches scenes and galleries in the same directory
   - Example: `/videos/shoot1/scene.mp4` → Gallery at `/videos/shoot1/`

2. **Performer Matching**
   - Matches scenes and galleries that share performers
   - Configurable minimum number of matching performers

3. **Date Matching**
   - Matches scenes and galleries with similar dates
   - Configurable date tolerance (in days)

### Configuration Options
- Enable/disable each matching strategy independently
- Set minimum performer matches required
- Configure date tolerance
- Exclude organized scenes from processing
- **Dry run mode** for safe testing without making changes

### User Experience
- Real-time progress bar during processing
- Detailed logging of all matches and assignments
- Summary statistics: total orphans, assigned, skipped, errors
- Task can be triggered from Stash UI

## Installation for Users

1. Install dependencies:
   ```bash
   pip install stashapp-tools
   ```

2. Copy plugin to Stash plugins directory:
   - Windows: `%USERPROFILE%\.stash\plugins\orphan-scenes-to-galleries\`
   - Linux/Mac: `~/.stash/plugins/orphan-scenes-to-galleries/`

3. Reload plugins in Stash (Settings → Plugins → Reload Plugins)

4. Configure and run from Settings → Tasks

## Development Setup

1. Clone repository
2. Install dependencies: `pip install stashapp-tools pyyaml flake8`
3. Make changes
4. Validate: `python validate.py`
5. Test in Stash with dry run enabled
6. Commit and push

## Technical Details

### Technology Stack
- **Language**: Python 3.7+
- **Dependencies**: stashapp-tools (for Stash API integration)
- **API**: Uses Stash GraphQL API via StashInterface
- **Configuration**: YAML format (Stash plugin standard)

### Plugin Architecture
1. **Configuration Loading**: Reads settings from Stash configuration
2. **Data Fetching**: Queries Stash for orphan scenes and all galleries
3. **Matching Pipeline**: Tries each matching strategy in order
4. **Assignment**: Updates scenes with matched galleries via GraphQL
5. **Reporting**: Logs progress and statistics

### Key Functions
- `get_orphan_scenes()`: Finds scenes with galleries_count = 0
- `get_all_galleries()`: Fetches all galleries for matching
- `match_by_path()`: Compares scene and gallery directory paths
- `match_by_performers()`: Finds galleries sharing performers
- `match_by_date()`: Finds galleries with similar dates
- `assign_scene_to_gallery()`: Updates scene via GraphQL API

## Testing

### Manual Testing
1. Enable dry run mode
2. Run task in Stash
3. Review logs
4. Disable dry run and run again

### Automated Testing
- GitHub Actions CI runs on push/PR
- Validates YAML syntax
- Checks Python syntax
- Runs linting (flake8)
- Tests on Python 3.7-3.11

### Validation
Run `python validate.py` to check:
- Required files exist
- YAML structure is valid
- Python syntax is correct
- Settings are properly configured

## Next Steps

### For Users
1. Install the plugin following QUICKSTART.md
2. Configure matching strategies
3. Run with dry run first
4. Review results and run for real

### For Publishing
1. Create GitHub repository
2. Update URLs in documentation (replace `yourusername`)
3. Create first release (v1.0.0)
4. Submit to Stash CommunityScripts
5. Share on Stash Discord/Discourse

### For Development
1. Test with real Stash instance
2. Gather user feedback
3. Implement planned features from CHANGELOG
4. Add unit tests
5. Improve performance for large databases

## Resources

- **Stash**: https://github.com/stashapp/stash
- **Stash Docs**: https://docs.stashapp.cc/
- **CommunityScripts**: https://github.com/stashapp/CommunityScripts
- **Stash Discord**: https://discord.gg/2TsNFKt
- **stashapp-tools**: https://github.com/stashapp/stashapp-tools

## License
MIT License - See LICENSE file

## Status
✅ **Ready for use and testing!**

The plugin is fully implemented with:
- Complete functionality
- Comprehensive documentation
- Testing tools
- CI/CD setup
- Contributing guidelines

Ready to:
1. Test with real Stash instance
2. Publish to GitHub
3. Share with Stash community
