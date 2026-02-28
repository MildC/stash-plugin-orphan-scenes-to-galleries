# Changelog

All notable changes to the Orphan Scenes to Galleries plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Option to match by studio
- Option to match by tags
- Batch processing with configurable batch size
- Export/import of match rules
- Duplicate detection and handling
- Configurable search depth for folder hierarchy

## [1.2.0] - 2026-02-28

### Fixed
- **Critical**: Fixed GraphQL schema bug - now uses `visual_files` instead of incorrect `paths` field
- **Critical**: Sibling folder prevention - scenes no longer incorrectly match galleries in unrelated sibling directories
- Fixed query to work with Stash API by fetching all scenes and filtering client-side

### Added
- Support for direct parent folder matching (scene in `/parent/video/` can match images in `/parent/`)
- Child/subfolder matching (scene can match images in subfolders)
- Human-readable logging - shows filenames and folder names instead of empty titles
- Comprehensive test suite covering all 4 README examples plus edge cases
- Extracted `gallery_matcher.py` module with testable matching logic
- Unit tests that run independently without Stash dependencies

### Changed
- Improved matching algorithm: searches same folder → child folders → direct parent
- Better logging with file names when titles are missing
- Updated to Python 3.9+ (removed 3.7, 3.8 from CI)
- Cleaner error messages and debug output

### Technical Details
- Matching now uses `should_match_folder()` function with clear rules:
  - ✓ Same folder
  - ✓ Child/subfolders (descendants)
  - ✓ Direct parent only
  - ✗ Sibling folders (prevented)
  - ✗ Grandparent folders (prevented)

## [1.1.0] - 2026-02-27

### Changed
- **BREAKING**: Replaced multiple matching strategies with hierarchical folder-based matching
- More efficient image queries (on-demand instead of loading all galleries)
- Better performance for large libraries

### Added
- Same folder search: finds images in the scene's folder
- Parent folder search: finds images in sibling/child folders
- Detailed logging showing which images are used for matching
- Folder path information in match logs

### Removed
- Path-based matching (replaced by folder hierarchy search)
- Performer-based matching (removed)
- Date-based matching with tolerance (removed)
- Related configuration options: `matchByPath`, `matchByDate`, `dateTolerance`, `matchByPerformers`, `minPerformerMatch`

## [1.0.0] - 2026-02-27

### Added
- Initial release of the plugin
- Path-based scene-to-gallery matching
- Performer-based matching with configurable minimum matches
- Date-based matching with configurable tolerance (in days)
- Dry run mode for safe testing
- Configurable option to exclude organized scenes
- Real-time progress tracking during processing
- Detailed logging of matches and assignments
- Summary statistics after processing
- Comprehensive documentation (README, QUICKSTART, TESTING, CONTRIBUTING)
- Plugin validation script
- GitHub Actions CI workflow

### Features
- **Three matching strategies**: Path, Performers, and Date
- **Flexible configuration**: Enable/disable each strategy independently
- **Safe testing**: Dry run mode to preview changes
- **Progress tracking**: Real-time progress bar in Stash UI
- **Detailed logging**: See exactly what the plugin is doing
- **Statistics**: Summary of orphan scenes, assignments, and skips

[Unreleased]: https://github.com/MildC/stash-plugin-orphan-scenes-to-galleries/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/MildC/stash-plugin-orphan-scenes-to-galleries/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/MildC/stash-plugin-orphan-scenes-to-galleries/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/MildC/stash-plugin-orphan-scenes-to-galleries/releases/tag/v1.0.0
