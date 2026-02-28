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

    def get_images_in_folder(self, folder_path: str) -> List[Dict]:
        """Find all images in a specific folder path."""
        query = {
            "path": {
                "modifier": "EQUALS",
                "value": folder_path
            }
        }

        try:
            images = self.stash.find_images(
                f=query,
                filter={"per_page": -1},
                fragment='id title galleries { id title folder { path } }'
            )
            return images if images else []
        except Exception as e:
            log.debug(f"Error finding images in folder {folder_path}: {str(e)}")
            return []

    def get_images_in_parent_folders(self, parent_path: str, exclude_path: str) -> Dict[str, List[Dict]]:
        """Find all images in folders that start with parent_path prefix, excluding the original path."""
        # Query for images where path starts with parent_path
        query = {
            "path": {
                "modifier": "INCLUDES",
                "value": parent_path
            }
        }

        try:
            images = self.stash.find_images(
                f=query,
                filter={"per_page": -1},
                fragment='id title path galleries { id title folder { path } }'
            )

            if not images:
                return {}

            # Group images by their folder path, excluding the original folder
            folder_images = {}
            for image in images:
                image_path = image.get('path', '')
                if not image_path:
                    continue

                image_folder = str(Path(image_path).parent)

                # Skip the original folder
                if image_folder == exclude_path:
                    continue

                if image_folder not in folder_images:
                    folder_images[image_folder] = []
                folder_images[image_folder].append(image)

            return folder_images
        except Exception as e:
            log.debug(f"Error finding images in parent folders: {str(e)}")
            return {}

    def match_by_folder_hierarchy(self, scene: Dict) -> Optional[Dict]:
        """
        Match scene to gallery using hierarchical folder-based approach:
        1. Search for images in the same folder as the scene
        2. If no images found, search in sibling/child folders (parent path prefix)
        3. Return the gallery of the first image found
        """
        scene_files = scene.get('files', [])
        if not scene_files:
            log.debug(f"Scene {scene['id']} has no files")
            return None

        scene_path = scene_files[0]['path']
        scene_folder = str(Path(scene_path).parent)

        log.debug(f"Scene {scene['id']} folder: {scene_folder}")

        # Step 1: Search for images in the same folder
        images = self.get_images_in_folder(scene_folder)

        if images:
            log.debug(f"Found {len(images)} images in same folder: {scene_folder}")
            # Get the first image's gallery
            first_image = images[0]
            galleries = first_image.get('galleries', [])

            if galleries:
                gallery = galleries[0]  # Use first gallery
                gallery_folder = gallery.get('folder', {}).get('path', 'No folder assigned')
                log.info(f"Matched scene {scene['id']} to gallery {gallery['id']} ('{gallery.get('title', 'Untitled')}') "
                        f"via image {first_image['id']} in same folder")
                log.debug(f"  Gallery folder: {gallery_folder}")
                return gallery
            else:
                log.debug(f"First image {first_image['id']} has no galleries")
        else:
            log.debug(f"No images found in same folder: {scene_folder}")

        # Step 2: Search in parent folders (sibling/child folders)
        parent_path = str(Path(scene_folder).parent)

        if not parent_path or parent_path == scene_folder:
            log.debug(f"No valid parent path for scene {scene['id']}")
            return None

        log.debug(f"Searching for images in folders with parent path prefix: {parent_path}")

        folder_images = self.get_images_in_parent_folders(parent_path, scene_folder)

        if folder_images:
            log.debug(f"Found images in {len(folder_images)} folders with parent path prefix")

            # Sort folders by path for consistent ordering
            for folder_path in sorted(folder_images.keys()):
                images_in_folder = folder_images[folder_path]
                log.debug(f"  {folder_path}: {len(images_in_folder)} images")

                # Get first image's gallery from this folder
                first_image = images_in_folder[0]
                galleries = first_image.get('galleries', [])

                if galleries:
                    gallery = galleries[0]
                    gallery_folder = gallery.get('folder', {}).get('path', 'No folder assigned')
                    log.info(f"Matched scene {scene['id']} to gallery {gallery['id']} ('{gallery.get('title', 'Untitled')}') "
                            f"via image {first_image['id']} in related folder: {folder_path}")
                    log.debug(f"  Gallery folder: {gallery_folder}")
                    return gallery
                else:
                    log.debug(f"  First image {first_image['id']} in {folder_path} has no galleries")
        else:
            log.debug(f"No folders found with parent path prefix: {parent_path}")

        return None

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

    def process_scene(self, scene: Dict):
        """Process a single orphan scene and try to assign it to a gallery."""
        # Use hierarchical folder-based matching
        matched_gallery = self.match_by_folder_hierarchy(scene)

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

        # Process each orphan scene
        log.info(f"Processing {len(orphan_scenes)} orphan scenes using folder hierarchy matching...")

        for i, scene in enumerate(orphan_scenes):
            log.progress((i + 1) / len(orphan_scenes))
            self.process_scene(scene)

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
