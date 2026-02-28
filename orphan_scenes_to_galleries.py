import stashapi.log as log
from stashapi.stashapp import StashInterface
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# Import the matching logic
from matching_logic import should_match_folder


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

    def get_scene_identifier(self, scene: Dict) -> str:
        """Get a human-readable identifier for a scene."""
        title = scene.get('title', '').strip()
        if title:
            return f"'{title}'"

        # Fall back to filename if no title
        files = scene.get('files', [])
        if files:
            file_path = files[0].get('path', '')
            if file_path:
                filename = Path(file_path).name
                return f"file:{filename}"

        return f"ID:{scene['id']}"

    def get_gallery_identifier(self, gallery: Dict) -> str:
        """Get a human-readable identifier for a gallery."""
        title = gallery.get('title', '').strip()
        if title:
            return f"'{title}'"

        # Fall back to folder path if no title
        folder = gallery.get('folder', {})
        if folder:
            folder_path = folder.get('path', '')
            if folder_path:
                folder_name = Path(folder_path).name
                return f"folder:{folder_name}"

        return f"ID:{gallery['id']}"

    def get_orphan_scenes(self) -> List[Dict]:
        """Find all scenes without galleries."""
        # Get all scenes and filter for those without galleries
        log.info("Fetching all scenes to find orphans...")

        all_scenes = []
        page = 1
        per_page = 100

        while True:
            scenes = self.stash.find_scenes(
                f={},  # Empty filter to get all scenes
                filter={"page": page, "per_page": per_page},
                fragment='id title date organized files { path } galleries { id }'
            )

            if not scenes:
                break

            all_scenes.extend(scenes)
            page += 1

            # Show progress
            log.progress(page * per_page / 1000)  # Rough progress estimate

        # Filter for scenes without galleries
        orphan_scenes = []
        for scene in all_scenes:
            galleries = scene.get('galleries', [])

            # Skip if scene has galleries
            if galleries and len(galleries) > 0:
                continue

            # Skip organized scenes if configured
            if self.settings.get('excludeOrganized', False) and scene.get('organized', False):
                continue

            orphan_scenes.append(scene)

        log.info(f"Found {len(orphan_scenes)} orphan scenes out of {len(all_scenes)} total scenes")
        self.stats['total_orphans'] = len(orphan_scenes)

        return orphan_scenes

    def get_images_in_folder(self, folder_path: str) -> List[Dict]:
        """Find all images in a specific folder path."""
        # Query for images where the path starts with the folder path
        # Use INCLUDES modifier to find images whose path contains the folder
        query = {
            "path": {
                "modifier": "INCLUDES",
                "value": folder_path
            }
        }

        try:
            images = self.stash.find_images(
                f=query,
                filter={"per_page": -1},
                fragment='id title visual_files { ... on ImageFile { path } } galleries { id title folder { path } }'
            )

            if not images:
                return []

            # Filter to only images actually in this specific folder (not subfolders)
            folder_images = []
            for image in images:
                # Images have visual_files array (union of VideoFile | ImageFile)
                visual_files = image.get('visual_files', [])
                if visual_files and len(visual_files) > 0:
                    # Get path from the first file
                    image_path = visual_files[0].get('path', '')
                    if image_path:
                        image_folder = str(Path(image_path).parent)
                        if image_folder == folder_path:
                            folder_images.append(image)

            return folder_images
        except Exception as e:
            log.debug(f"Error finding images in folder {folder_path}: {str(e)}")
            return []

    def get_images_in_parent_folders(self, parent_path: str, scene_folder: str) -> Dict[str, List[Dict]]:
        """
        Find images in:
        1. Child/subfolders of scene_folder (e.g., /scene/pics/)
        2. Direct parent folder only (e.g., /parent/ when scene is in /parent/video/)

        Does NOT match sibling folders at the same level.
        """
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
                fragment='id title visual_files { ... on ImageFile { path } } galleries { id title folder { path } }'
            )

            if not images:
                return {}

            # Group images by their folder path
            folder_images = {}
            for image in images:
                # Images have visual_files array (union of VideoFile | ImageFile)
                visual_files = image.get('visual_files', [])
                if visual_files and len(visual_files) > 0:
                    # Get path from the first file
                    image_path = visual_files[0].get('path', '')
                    if not image_path:
                        continue

                    image_folder = str(Path(image_path).parent)

                    # Use the extracted matching logic function
                    if not should_match_folder(image_folder, scene_folder, parent_path):
                        # Skip siblings and other unrelated folders
                        continue

                    if image_folder not in folder_images:
                        folder_images[image_folder] = []
                    folder_images[image_folder].append(image)

            return folder_images
        except Exception as e:
            log.debug(f"Error finding images in related folders: {str(e)}")
            return {}

    def match_by_folder_hierarchy(self, scene: Dict) -> Optional[Dict]:
        """
        Match scene to gallery using hierarchical folder-based approach:
        1. Search for images in the same folder as the scene
        2. If no images found, search in:
           - Child/subfolders of the scene folder (e.g., /scene/pics/)
           - Direct parent folder (e.g., /parent/ when scene is in /parent/video/)
        3. Return the gallery of the first image found

        NOTE: Does NOT match sibling folders at the same level.
        Example: Scene in /media/2024/april/ will NOT match /media/2024/march/ (siblings)
        But: Scene in /media/session/video/ WILL match /media/session/ (direct parent)
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

                scene_name = self.get_scene_identifier(scene)
                gallery_name = self.get_gallery_identifier(gallery)

                log.info(f"Matched scene {scene['id']} {scene_name} to gallery {gallery['id']} {gallery_name} "
                        f"via image {first_image['id']} in same folder")
                log.debug(f"  Scene folder: {scene_folder}")
                log.debug(f"  Gallery folder: {gallery_folder}")
                return gallery
            else:
                log.debug(f"First image {first_image['id']} has no galleries")
        else:
            log.debug(f"No images found in same folder: {scene_folder}")

        # Step 2: Search in related folders:
        # - Child/subfolders of scene folder (e.g., /scene/pics/)
        # - Direct parent folder (e.g., /parent/ when scene is in /parent/video/)
        # Does NOT search sibling folders (e.g., /parent/other/ when scene is in /parent/video/)
        parent_path = str(Path(scene_folder).parent)

        if not parent_path or parent_path == scene_folder:
            log.debug(f"No valid parent path for scene {scene['id']}")
            return None

        log.debug(f"Searching for images in child folders and direct parent: {parent_path}")

        folder_images = self.get_images_in_parent_folders(parent_path, scene_folder)

        if folder_images:
            log.debug(f"Found images in {len(folder_images)} related folders")

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

                    scene_name = self.get_scene_identifier(scene)
                    gallery_name = self.get_gallery_identifier(gallery)

                    log.info(f"Matched scene {scene['id']} {scene_name} to gallery {gallery['id']} {gallery_name} "
                            f"via image {first_image['id']} in related folder: {folder_path}")
                    log.debug(f"  Scene folder: {scene_folder}")
                    log.debug(f"  Gallery folder: {gallery_folder}")
                    return gallery
                else:
                    log.debug(f"  First image {first_image['id']} in {folder_path} has no galleries")
        else:
            log.debug(f"No related folders with images found for: {scene_folder}")

        return None

    def assign_scene_to_gallery(self, scene: Dict, gallery: Dict):
        """Assign a scene to a gallery."""
        dry_run = self.settings.get('dryRun', False)

        scene_name = self.get_scene_identifier(scene)
        gallery_name = self.get_gallery_identifier(gallery)

        log.info(f"{'[DRY RUN] ' if dry_run else ''}Assigning scene {scene['id']} {scene_name} to gallery {gallery['id']} {gallery_name}")

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
                scene_name = self.get_scene_identifier(scene)
                gallery_name = self.get_gallery_identifier(gallery)
                log.error(f"Error assigning scene {scene['id']} {scene_name} to gallery {gallery['id']} {gallery_name}: {str(e)}")
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
            scene_name = self.get_scene_identifier(scene)
            log.debug(f"No matching gallery found for scene {scene['id']} {scene_name}")
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
