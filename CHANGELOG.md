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
- Configurable search depth for parent folder hierarchy

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

[Unreleased]: https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/releases/tag/v1.0.0
