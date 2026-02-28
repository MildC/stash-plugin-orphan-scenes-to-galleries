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

[Unreleased]: https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries/releases/tag/v1.0.0
