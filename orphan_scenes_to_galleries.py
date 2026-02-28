import stashapi.log as log
from stashapi.stashapp import StashInterface
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set


class OrphanSceneProcessor:
    def __init__(self, stash: StashInterface, settings: Dict):
        self.stash = stash
        self.settings = settings
        self.stats = {
            'total_orphans': 0,
            'assigned': 0,
            'skipped': 0,
            'errors': 0
        }

    def get_orphan_scenes(self) -> List[Dict]:
        """Find all scenes without galleries."""
        query = {
            "galleries_count": {
                "modifier": "EQUALS",
                "value": 0
            }
        }

        # Optionally exclude organized scenes
        if self.settings.get('excludeOrganized', False):
            query["organized"] = False

        # Get total count
        total_count = self.stash.find_scenes(
            f=query,
            filter={"page": 0, "per_page": 0},
            get_count=True
        )[0]

        log.info(f"Found {total_count} orphan scenes")
        self.stats['total_orphans'] = total_count

        # Fetch all orphan scenes
        orphan_scenes = []
        page = 1
        per_page = 100

        while len(orphan_scenes) < total_count:
            log.progress(len(orphan_scenes) / total_count)

            scenes = self.stash.find_scenes(
                f=query,
                filter={"page": page, "per_page": per_page},
                fragment='id title date organized files { path } performers { id name }'
            )

            if not scenes:
                break

            orphan_scenes.extend(scenes)
            page += 1

        return orphan_scenes

    def get_all_galleries(self) -> List[Dict]:
        """Fetch all galleries for matching."""
        query = {}

        # Get total count
        total_count = self.stash.find_galleries(
            f=query,
            filter={"page": 0, "per_page": 0},
            get_count=True
        )[0]

        log.info(f"Found {total_count} galleries")

        # Fetch all galleries
        galleries = []
        page = 1
        per_page = 100

        while len(galleries) < total_count:
            gallery_batch = self.stash.find_galleries(
                f=query,
                filter={"page": page, "per_page": per_page},
                fragment='id title date folder { path } performers { id name }'
            )

            if not gallery_batch:
                break

            galleries.extend(gallery_batch)
            page += 1

        return galleries

    def match_by_path(self, scene: Dict, galleries: List[Dict]) -> Optional[Dict]:
        """Match scene to gallery by directory path."""
        if not self.settings.get('matchByPath', True):
            return None

        scene_files = scene.get('files', [])
        if not scene_files:
            return None

        scene_path = Path(scene_files[0]['path']).parent

        for gallery in galleries:
            folder = gallery.get('folder')
            if folder and folder.get('path'):
                gallery_path = Path(folder['path'])
                if scene_path == gallery_path:
                    log.debug(f"Matched scene {scene['id']} to gallery {gallery['id']} by path: {scene_path}")
                    return gallery

        return None

    def match_by_date(self, scene: Dict, galleries: List[Dict]) -> Optional[Dict]:
        """Match scene to gallery by date with tolerance."""
        if not self.settings.get('matchByDate', False):
            return None

        scene_date_str = scene.get('date')
        if not scene_date_str:
            return None

        try:
            scene_date = datetime.strptime(scene_date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None

        tolerance_days = self.settings.get('dateTolerance', 1)
        tolerance = timedelta(days=tolerance_days)

        for gallery in galleries:
            gallery_date_str = gallery.get('date')
            if not gallery_date_str:
                continue

            try:
                gallery_date = datetime.strptime(gallery_date_str, '%Y-%m-%d')
                if abs((scene_date - gallery_date).days) <= tolerance_days:
                    log.debug(f"Matched scene {scene['id']} to gallery {gallery['id']} by date: {scene_date_str} ~ {gallery_date_str}")
                    return gallery
            except (ValueError, TypeError):
                continue

        return None

    def match_by_performers(self, scene: Dict, galleries: List[Dict]) -> Optional[Dict]:
        """Match scene to gallery by shared performers."""
        if not self.settings.get('matchByPerformers', False):
            return None

        scene_performers = scene.get('performers', [])
        if not scene_performers:
            return None

        scene_performer_ids = {p['id'] for p in scene_performers}
        min_matches = self.settings.get('minPerformerMatch', 1)

        best_match = None
        best_match_count = 0

        for gallery in galleries:
            gallery_performers = gallery.get('performers', [])
            if not gallery_performers:
                continue

            gallery_performer_ids = {p['id'] for p in gallery_performers}
            match_count = len(scene_performer_ids & gallery_performer_ids)

            if match_count >= min_matches and match_count > best_match_count:
                best_match = gallery
                best_match_count = match_count

        if best_match:
            log.debug(f"Matched scene {scene['id']} to gallery {best_match['id']} by {best_match_count} performers")

        return best_match

    def assign_scene_to_gallery(self, scene: Dict, gallery: Dict):
        """Assign a scene to a gallery."""
        dry_run = self.settings.get('dryRun', False)

        scene_title = scene.get('title', 'Untitled')
        gallery_title = gallery.get('title', 'Untitled')

        log.info(f"{'[DRY RUN] ' if dry_run else ''}Assigning scene {scene['id']} ('{scene_title}') to gallery {gallery['id']} ('{gallery_title}')")

        if not dry_run:
            try:
                # Update the scene to add the gallery
                self.stash.update_scenes({
                    "ids": [scene['id']],
                    "gallery_ids": {
                        "mode": "ADD",
                        "ids": [gallery['id']]
                    }
                })
                self.stats['assigned'] += 1
            except Exception as e:
                log.error(f"Error assigning scene {scene['id']} to gallery {gallery['id']}: {str(e)}")
                self.stats['errors'] += 1
        else:
            self.stats['assigned'] += 1

    def process_scene(self, scene: Dict, galleries: List[Dict]):
        """Process a single orphan scene and try to assign it to a gallery."""
        # Try different matching strategies in order of preference
        matched_gallery = None

        # 1. Try path matching first (most reliable)
        matched_gallery = self.match_by_path(scene, galleries)

        # 2. Try performer matching if path didn't work
        if not matched_gallery:
            matched_gallery = self.match_by_performers(scene, galleries)

        # 3. Try date matching as last resort
        if not matched_gallery:
            matched_gallery = self.match_by_date(scene, galleries)

        # Assign if we found a match
        if matched_gallery:
            self.assign_scene_to_gallery(scene, matched_gallery)
        else:
            log.debug(f"No matching gallery found for scene {scene['id']}")
            self.stats['skipped'] += 1

    def process_all(self):
        """Main processing function."""
        log.info("Starting orphan scene processing...")
        log.info(f"Settings: {self.settings}")

        # Fetch orphan scenes
        orphan_scenes = self.get_orphan_scenes()

        if not orphan_scenes:
            log.info("No orphan scenes found!")
            return

        # Fetch all galleries
        galleries = self.get_all_galleries()

        if not galleries:
            log.warning("No galleries found! Cannot assign scenes.")
            return

        # Process each orphan scene
        log.info(f"Processing {len(orphan_scenes)} orphan scenes against {len(galleries)} galleries...")

        for i, scene in enumerate(orphan_scenes):
            log.progress((i + 1) / len(orphan_scenes))
            self.process_scene(scene, galleries)

        # Print summary
        log.info("=" * 50)
        log.info("Processing complete!")
        log.info(f"Total orphan scenes: {self.stats['total_orphans']}")
        log.info(f"Assigned: {self.stats['assigned']}")
        log.info(f"Skipped: {self.stats['skipped']}")
        log.info(f"Errors: {self.stats['errors']}")
        log.info("=" * 50)


def main():
    # Parse input from Stash
    json_input = json.loads(sys.stdin.read())

    # Initialize Stash interface
    FRAGMENT_SERVER = json_input["server_connection"]
    stash = StashInterface(FRAGMENT_SERVER)

    # Get plugin configuration
    config = stash.get_configuration()

    # Default settings
    settings = {
        "matchByPath": True,
        "matchByDate": False,
        "dateTolerance": 1,
        "matchByPerformers": False,
        "minPerformerMatch": 1,
        "excludeOrganized": False,
        "dryRun": False
    }

    # Override with user settings
    plugin_config = config.get("plugins", {}).get("orphanScenesToGalleries", {})
    settings.update(plugin_config)

    # Create processor
    processor = OrphanSceneProcessor(stash, settings)

    # Handle different modes
    args = json_input.get("args", {})
    mode = args.get("mode")

    if mode == "processAll":
        processor.process_all()
    else:
        log.error(f"Unknown mode: {mode}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(f"Fatal error: {str(e)}")
        import traceback
        log.error(traceback.format_exc())
        sys.exit(1)
